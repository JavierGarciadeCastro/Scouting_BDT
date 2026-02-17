// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/Scouting/interface/Run3ScoutingMuon.h"
#include "DataFormats/Scouting/interface/Run3ScoutingVertex.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackBase.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/GeometryVector/interface/GlobalPoint.h"
#include "DataFormats/Math/interface/LorentzVector.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "TTree.h"

#include "RecoVertex/KalmanVertexFit/interface/KalmanVertexFitter.h"
#include "RecoVertex/VertexPrimitives/interface/TransientVertex.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "TMath.h"
#include "TH1D.h"
#include "TCanvas.h"
#include "TFile.h"
#include "TLegend.h"
#include "TStyle.h"


//Header
class BDT_ntuplizer : public edm::one::EDAnalyzer<> {
  public:
    explicit BDT_ntuplizer(const edm::ParameterSet&);
    ~BDT_ntuplizer() override;
    void beginJob() override;
    void endJob() override;
    void analyze(const edm::Event&, const edm::EventSetup&) override;

  private:
    unsigned int run, lumi, evtn;
    edm::EDGetTokenT<std::vector<Run3ScoutingMuon>> muTokenScoutingVtx_;
    edm::EDGetTokenT<std::vector<Run3ScoutingMuon>> muTokenScoutingNoVtx_;
    edm::EDGetTokenT<std::vector<Run3ScoutingVertex>> svTokenScouting_;
    edm::ESGetToken<TransientTrackBuilder, TransientTrackRecord> theTransientTrackBuilderToken_;

    TFile* fout;
    TTree* tout;
    
    //Scouting SV variables
    std::vector<unsigned int> SV_ndof_NoVtx, SV_ndof_Vtx;
    std::vector<float> SV_chi2_NoVtx, SV_prob_NoVtx, SV_chi2Ndof_NoVtx, SV_lxy_NoVtx, SV_chi2_Vtx, SV_prob_Vtx, SV_chi2Ndof_Vtx, SV_lxy_Vtx;
    std::vector<bool> SV_global_Vtx, SV_tracker_Vtx, SV_global_NoVtx, SV_tracker_NoVtx;
    
    //Scouting muon variables
    std::vector<int> nmu_NoVtx, nmu_Vtx;
    std::vector<bool> mu_isGlobal_NoVtx, mu_isTracker_NoVtx, mu_isGlobal_Vtx, mu_isTracker_Vtx;
    std::vector<float> mu_pt_NoVtx, mu_eta_NoVtx, mu_phi_NoVtx, mu_chi2Ndof_NoVtx, mu_pt_Vtx, mu_eta_Vtx, mu_phi_Vtx, mu_chi2Ndof_Vtx;
    std::vector<std::vector<int>> mu_vtxIdx_NoVtx, mu_vtxIdx_Vtx;

    float min_Pt, max_eta;

};

//Constructor
BDT_ntuplizer::BDT_ntuplizer(const edm::ParameterSet& iConfig) :
  muTokenScoutingVtx_{consumes<std::vector<Run3ScoutingMuon>>(iConfig.getParameter<edm::InputTag>("ScoutingmuonsVtx"))},
  muTokenScoutingNoVtx_{consumes<std::vector<Run3ScoutingMuon>>(iConfig.getParameter<edm::InputTag>("ScoutingmuonsNoVtx"))},
  svTokenScouting_{consumes<std::vector<Run3ScoutingVertex>>(iConfig.getParameter<edm::InputTag>("hltScoutingMuonPacker_displacedVtx"))},
  theTransientTrackBuilderToken_{esConsumes(edm::ESInputTag("", "TransientTrackBuilder"))}
  {}

//Destructor
BDT_ntuplizer::~BDT_ntuplizer() = default;

void BDT_ntuplizer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
  run = iEvent.id().run();
  lumi = iEvent.id().luminosityBlock();
  evtn = iEvent.id().event();

  min_Pt = 3;
  max_eta = 2.5;
  float minVtxProb = 0.001;


  const auto& theTransientTrackBuilder = iSetup.getData(theTransientTrackBuilderToken_);
  edm::Handle<std::vector<Run3ScoutingMuon>> ScoutingmuonsVtx;
  edm::Handle<std::vector<Run3ScoutingMuon>> ScoutingmuonsNoVtx;
  edm::Handle<std::vector<Run3ScoutingVertex>> ScoutingdisplacedVertices;


  iEvent.getByToken(muTokenScoutingVtx_, ScoutingmuonsVtx);
  iEvent.getByToken(muTokenScoutingNoVtx_, ScoutingmuonsNoVtx);
  iEvent.getByToken(svTokenScouting_, ScoutingdisplacedVertices);

  struct TaggedTT {
    reco::TransientTrack tt;
    bool isGlobal;
    bool isTracker;
    float px;
    float py;
  };

  std::vector<TaggedTT> allTracksTT_NoVtx;
  std::vector<TaggedTT> gen_matched_tt_NoVtx;
  std::vector<TaggedTT> allTracksTT_Vtx;
  std::vector<TaggedTT> gen_matched_tt_Vtx;

  SV_ndof_NoVtx.clear(); SV_ndof_Vtx.clear();
  SV_chi2_NoVtx.clear(); SV_prob_NoVtx.clear(); SV_lxy_NoVtx.clear(); SV_chi2_Vtx.clear(); SV_prob_Vtx.clear(); SV_lxy_Vtx.clear();
  SV_global_NoVtx.clear(); SV_tracker_NoVtx.clear(); SV_global_Vtx.clear(); SV_tracker_Vtx.clear(); 
  
  nmu_NoVtx.clear(); nmu_Vtx.clear();
  mu_isGlobal_NoVtx.clear(); mu_isTracker_NoVtx.clear(); mu_isGlobal_Vtx.clear(); mu_isTracker_Vtx.clear();
  mu_pt_NoVtx.clear(); mu_eta_NoVtx.clear(); mu_phi_NoVtx.clear(); mu_chi2Ndof_NoVtx.clear(); mu_pt_Vtx.clear(); mu_eta_Vtx.clear(); mu_phi_Vtx.clear(); mu_chi2Ndof_Vtx.clear();
  mu_vtxIdx_NoVtx.clear(); mu_vtxIdx_Vtx.clear();

  const auto& muonCollectionVtx = *ScoutingmuonsVtx;
  const auto& muonCollectionNoVtx = *ScoutingmuonsNoVtx;
  unsigned int nMus_Vtx = muonCollectionVtx.size();
  unsigned int nMus_NoVtx = muonCollectionNoVtx.size();

  nmu_NoVtx.push_back(nMus_NoVtx);
  nmu_Vtx.push_back(nMus_Vtx);

  /////////////////////////////////////////////////////////////////////
  ////////////////////// VTX COLLECTION   /////////////////////////////
  /////////////////////////////////////////////////////////////////////

  for (unsigned int iMu1 = 0; iMu1 < nMus_Vtx; ++iMu1) {
    const auto& mu1 = muonCollectionVtx[iMu1];

    if (mu1.pt() < min_Pt) continue;
    if (std::abs(mu1.eta()) > max_eta) continue;

    mu_pt_Vtx.push_back(mu1.pt());
    mu_eta_Vtx.push_back(mu1.eta());
    mu_phi_Vtx.push_back(mu1.phi());
    mu_chi2Ndof_Vtx.push_back(mu1.normalizedChi2());
    mu_vtxIdx_Vtx.push_back(mu1.vtxIndx());

    int charge1 = mu1.charge();
    float chi2_1 = mu1.trk_chi2();
    float ndof1 = mu1.trk_ndof();

    float px1 = mu1.trk_pt() * std::cos(mu1.trk_phi());  
    float py1 = mu1.trk_pt() * std::sin(mu1.trk_phi());  
    float pz1 = mu1.trk_pt() * std::sinh(mu1.trk_eta()); 

    reco::TrackBase::Vector momentum1(px1, py1, pz1);

    reco::TrackBase::Point refPoint1(
      mu1.trk_vx(),
      mu1.trk_vy(),
      mu1.trk_vz()
    );

    reco::TrackBase::CovarianceMatrix cov1 = reco::TrackBase::CovarianceMatrix();
    cov1(0,0) = mu1.trk_qoverpError()*mu1.trk_qoverpError();
    cov1(1,1) = mu1.trk_lambdaError()*mu1.trk_lambdaError();
    cov1(2,2) = mu1.trk_phiError()*mu1.trk_phiError();
    cov1(3,3) = mu1.trk_dxyError()*mu1.trk_dxyError();
    cov1(4,4) = mu1.trk_dszError()*mu1.trk_dszError();

    cov1(0,1) = mu1.trk_qoverp_lambda_cov();
    cov1(1,0) = mu1.trk_qoverp_lambda_cov();
    cov1(0,2) = mu1.trk_qoverp_phi_cov();
    cov1(2,0) = mu1.trk_qoverp_phi_cov();
    cov1(0,3) = mu1.trk_qoverp_dxy_cov();
    cov1(3,0) = mu1.trk_qoverp_dxy_cov();
    cov1(0,4) = mu1.trk_qoverp_dsz_cov();
    cov1(4,0) = mu1.trk_qoverp_dsz_cov();

    cov1(1,2) = mu1.trk_lambda_phi_cov();
    cov1(2,1) = mu1.trk_lambda_phi_cov();
    cov1(1,3) = mu1.trk_lambda_dxy_cov();
    cov1(3,1) = mu1.trk_lambda_dxy_cov();
    cov1(1,4) = mu1.trk_lambda_dsz_cov();
    cov1(4,1) = mu1.trk_lambda_dsz_cov();

    cov1(2,3) = mu1.trk_phi_dxy_cov();
    cov1(3,2) = mu1.trk_phi_dxy_cov();
    cov1(2,4) = mu1.trk_phi_dsz_cov();
    cov1(4,2) = mu1.trk_phi_dsz_cov();

    cov1(3,4) = mu1.trk_dxy_dsz_cov();
    cov1(4,3) = mu1.trk_dxy_dsz_cov();

    reco::Track track1(chi2_1,
      ndof1,
      refPoint1,
      momentum1,
      charge1,
      cov1,
      reco::TrackBase::undefAlgorithm,
      reco::TrackBase::undefQuality
    );

    bool isGlobal = mu1.isGlobalMuon();
    mu_isGlobal_Vtx.push_back(isGlobal);

    bool isTracker = mu1.isTrackerMuon();
    mu_isTracker_Vtx.push_back(isTracker);

    allTracksTT_Vtx.push_back({theTransientTrackBuilder.build(track1), isGlobal, isTracker, px1, py1});
  }


  unsigned int nTracks_Vtx = allTracksTT_Vtx.size();
  for (unsigned int i1 = 0; i1 < nTracks_Vtx; ++i1) {
    for (unsigned int i2 = i1 + 1; i2 < nTracks_Vtx; ++i2) {
      const auto& t1 = allTracksTT_Vtx[i1];
      const auto& t2 = allTracksTT_Vtx[i2];

      if (t1.tt.impactPointState().charge() * t2.tt.impactPointState().charge() > 0) continue;

      std::vector<reco::TransientTrack> ttracks = {t1.tt, t2.tt};
      KalmanVertexFitter kvf(true);
      TransientVertex fittedVertex = kvf.vertex(ttracks);
        
      if (fittedVertex.isValid()) {
        float vtxProb = TMath::Prob(fittedVertex.totalChiSquared(), fittedVertex.degreesOfFreedom());
        if (vtxProb > minVtxProb) {
          bool globalVertex = (t1.isGlobal && t2.isGlobal);
          GlobalPoint vtxPos = fittedVertex.position();
          float lxy = std::hypot(vtxPos.x(), vtxPos.y());

          SV_lxy_Vtx.push_back(lxy);
          SV_prob_Vtx.push_back(vtxProb);
          SV_chi2_Vtx.push_back(fittedVertex.totalChiSquared()); 

          if (globalVertex) {
            SV_global_Vtx.push_back(true);
            SV_tracker_Vtx.push_back(false);
          }
          else {
            SV_global_Vtx.push_back(false);
            SV_tracker_Vtx.push_back(true);
          }
        }
      }
    }
  }

  /////////////////////////////////////////////////////////////////////
  ////////////////////  No VTX COLLECTION   ///////////////////////////
  /////////////////////////////////////////////////////////////////////

  for (unsigned int iMu1 = 0; iMu1 < nMus_NoVtx; ++iMu1) {
    const auto& mu1 = muonCollectionNoVtx[iMu1];
    if (mu1.pt() < min_Pt) continue;
    if (std::abs(mu1.eta()) > max_eta) continue;

    mu_pt_NoVtx.push_back(mu1.pt());
    mu_eta_NoVtx.push_back(mu1.eta());
    mu_phi_NoVtx.push_back(mu1.phi());
    mu_chi2Ndof_NoVtx.push_back(mu1.normalizedChi2());
    mu_vtxIdx_NoVtx.push_back(mu1.vtxIndx());

    int charge1 = mu1.charge();
    float chi2_1 = mu1.trk_chi2();
    float ndof1 = mu1.trk_ndof();

    float px1 = mu1.trk_pt() * std::cos(mu1.trk_phi());  
    float py1 = mu1.trk_pt() * std::sin(mu1.trk_phi());  
    float pz1 = mu1.trk_pt() * std::sinh(mu1.trk_eta()); 

    reco::TrackBase::Vector momentum1(px1, py1, pz1);

    reco::TrackBase::Point refPoint1(
      mu1.trk_vx(),
      mu1.trk_vy(),
      mu1.trk_vz()
    );

    reco::TrackBase::CovarianceMatrix cov1 = reco::TrackBase::CovarianceMatrix();
    cov1(0,0) = mu1.trk_qoverpError()*mu1.trk_qoverpError();
    cov1(1,1) = mu1.trk_lambdaError()*mu1.trk_lambdaError();
    cov1(2,2) = mu1.trk_phiError()*mu1.trk_phiError();
    cov1(3,3) = mu1.trk_dxyError()*mu1.trk_dxyError();
    cov1(4,4) = mu1.trk_dszError()*mu1.trk_dszError();

    cov1(0,1) = mu1.trk_qoverp_lambda_cov();
    cov1(1,0) = mu1.trk_qoverp_lambda_cov();
    cov1(0,2) = mu1.trk_qoverp_phi_cov();
    cov1(2,0) = mu1.trk_qoverp_phi_cov();
    cov1(0,3) = mu1.trk_qoverp_dxy_cov();
    cov1(3,0) = mu1.trk_qoverp_dxy_cov();
    cov1(0,4) = mu1.trk_qoverp_dsz_cov();
    cov1(4,0) = mu1.trk_qoverp_dsz_cov();

    cov1(1,2) = mu1.trk_lambda_phi_cov();
    cov1(2,1) = mu1.trk_lambda_phi_cov();
    cov1(1,3) = mu1.trk_lambda_dxy_cov();
    cov1(3,1) = mu1.trk_lambda_dxy_cov();
    cov1(1,4) = mu1.trk_lambda_dsz_cov();
    cov1(4,1) = mu1.trk_lambda_dsz_cov();

    cov1(2,3) = mu1.trk_phi_dxy_cov();
    cov1(3,2) = mu1.trk_phi_dxy_cov();
    cov1(2,4) = mu1.trk_phi_dsz_cov();
    cov1(4,2) = mu1.trk_phi_dsz_cov();

    cov1(3,4) = mu1.trk_dxy_dsz_cov();
    cov1(4,3) = mu1.trk_dxy_dsz_cov();

    reco::Track track1(chi2_1,
      ndof1,
      refPoint1,
      momentum1,
      charge1,
      cov1,
      reco::TrackBase::undefAlgorithm,
      reco::TrackBase::undefQuality
    );

    bool isGlobal = mu1.isGlobalMuon();
    mu_isGlobal_NoVtx.push_back(isGlobal);

    bool isTracker = mu1.isTrackerMuon();
    mu_isTracker_NoVtx.push_back(isTracker);
    allTracksTT_NoVtx.push_back({theTransientTrackBuilder.build(track1), isGlobal, isTracker, px1, py1});
  }


  unsigned int nTracks_NoVtx = allTracksTT_NoVtx.size();
  for (unsigned int i1 = 0; i1 < nTracks_NoVtx; ++i1) {
    for (unsigned int i2 = i1 + 1; i2 < nTracks_NoVtx; ++i2) {
      const auto& t1 = allTracksTT_NoVtx[i1];
      const auto& t2 = allTracksTT_NoVtx[i2];

      if (t1.tt.impactPointState().charge() * t2.tt.impactPointState().charge() > 0) continue;

      std::vector<reco::TransientTrack> ttracks = {t1.tt, t2.tt};
      KalmanVertexFitter kvf(true);
      TransientVertex fittedVertex = kvf.vertex(ttracks);
        
      if (fittedVertex.isValid()) {
        float vtxProb = TMath::Prob(fittedVertex.totalChiSquared(), fittedVertex.degreesOfFreedom());
        if (vtxProb > minVtxProb) {
          bool globalVertex = (t1.isGlobal && t2.isGlobal);
          GlobalPoint vtxPos = fittedVertex.position();
          float lxy = std::hypot(vtxPos.x(), vtxPos.y());

          SV_lxy_Vtx.push_back(lxy);
          SV_prob_Vtx.push_back(vtxProb);
          SV_chi2_Vtx.push_back(fittedVertex.totalChiSquared()); 

          if (globalVertex) {
            SV_global_Vtx.push_back(true);
            SV_tracker_Vtx.push_back(false);
          }
          else {
            SV_global_Vtx.push_back(false);
            SV_tracker_Vtx.push_back(true);
          }
        }
      }
    }
  }
  tout->Fill();
}


void BDT_ntuplizer::beginJob() {
  edm::Service<TFileService> fs;

  fout = new TFile("root_output/output.root", "RECREATE");
  tout = new TTree("tout","Run3ScoutingTree");

  tout->Branch("run", &run);
  tout->Branch("lumi", &lumi);
  tout->Branch("evtn", &evtn);
  
  //NoVtx
  tout->Branch("SV_chi2_NoVtx", &SV_chi2_NoVtx);
  tout->Branch("SV_prob_NoVtx", &SV_prob_NoVtx);
  tout->Branch("SV_lxy_NoVtx", &SV_lxy_NoVtx);
  tout->Branch("SV_global_NoVtx", &SV_global_NoVtx);
  tout->Branch("SV_tracker_NoVtx", &SV_tracker_NoVtx);

  tout->Branch("nmu_NoVtx", &nmu_NoVtx);
  tout->Branch("mu_isGlobal_NoVtx", &mu_isGlobal_NoVtx);
  tout->Branch("mu_isTracker_NoVtx", &mu_isTracker_NoVtx);
  tout->Branch("mu_pt_NoVtx", &mu_pt_NoVtx);
  tout->Branch("mu_eta_NoVtx", &mu_eta_NoVtx);
  tout->Branch("mu_phi_NoVtx", &mu_phi_NoVtx);
  tout->Branch("mu_chi2Ndof_NoVtx", &mu_chi2Ndof_NoVtx);
  tout->Branch("mu_vtxIdx_NoVtx", &mu_vtxIdx_NoVtx);

  //Vtx
  tout->Branch("SV_chi2_Vtx", &SV_chi2_Vtx);
  tout->Branch("SV_prob_Vtx", &SV_prob_Vtx);
  tout->Branch("SV_lxy_Vtx", &SV_lxy_Vtx);
  tout->Branch("SV_global_Vtx", &SV_global_Vtx);
  tout->Branch("SV_tracker_Vtx", &SV_tracker_Vtx);

  tout->Branch("nmu_Vtx", &nmu_Vtx);
  tout->Branch("mu_isGlobal_Vtx", &mu_isGlobal_Vtx);
  tout->Branch("mu_isTracker_Vtx", &mu_isTracker_Vtx);
  tout->Branch("mu_pt_Vtx", &mu_pt_Vtx);
  tout->Branch("mu_eta_Vtx", &mu_eta_Vtx);
  tout->Branch("mu_phi_Vtx", &mu_phi_Vtx);
  tout->Branch("mu_chi2Ndof_Vtx", &mu_chi2Ndof_Vtx);
  tout->Branch("mu_vtxIdx_Vtx", &mu_vtxIdx_Vtx);
}

void BDT_ntuplizer::endJob() {
  fout->Write();
  if (tout) {
    std::cout << "SctParLooper: total entries in tout = " << tout->GetEntries() << std::endl;
  } else {
    std::cout << "SctParLooper: tout is null!" << std::endl;
  }
  fout->Close();
}

DEFINE_FWK_MODULE(BDT_ntuplizer);
