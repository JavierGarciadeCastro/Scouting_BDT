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
    
    // ===================== SV variables =====================
    std::vector<unsigned int> SV1_ndof_NoVtx, SV1_ndof_Vtx;
    std::vector<unsigned int> SV2_ndof_NoVtx, SV2_ndof_Vtx;
    std::vector<float> SV1_chi2_NoVtx, SV1_prob_NoVtx, SV1_chi2Ndof_NoVtx, SV1_lxy_NoVtx;
    std::vector<float> SV1_chi2_Vtx,  SV1_prob_Vtx,  SV1_chi2Ndof_Vtx,  SV1_lxy_Vtx;
    std::vector<float> SV2_chi2_NoVtx, SV2_prob_NoVtx, SV2_chi2Ndof_NoVtx, SV2_lxy_NoVtx;
    std::vector<float> SV1_px_NoVtx, SV1_py_NoVtx, SV1_pt_NoVtx, SV1_dphi_NoVtx, SV1_px_Vtx, SV1_py_Vtx, SV1_pt_Vtx, SV1_dphi_Vtx;
    std::vector<float> SV2_px_NoVtx, SV2_py_NoVtx, SV2_pt_NoVtx, SV2_dphi_NoVtx, SV2_px_Vtx, SV2_py_Vtx, SV2_pt_Vtx, SV2_dphi_Vtx;
    std::vector<float> SV2_chi2_Vtx,  SV2_prob_Vtx,  SV2_chi2Ndof_Vtx,  SV2_lxy_Vtx;
    std::vector<bool> SV1_global_NoVtx, SV1_global_Vtx;
    std::vector<bool> SV2_global_NoVtx, SV2_global_Vtx;

    // ===================== Scouting muon variables =====================
    std::vector<int> nmu_NoVtx, nmu_Vtx;
    std::vector<bool> mu1_isGlobal_NoVtx, mu1_isTracker_NoVtx, mu1_isGlobal_Vtx, mu1_isTracker_Vtx;
    std::vector<bool> mu2_isGlobal_NoVtx, mu2_isTracker_NoVtx, mu2_isGlobal_Vtx, mu2_isTracker_Vtx;
    std::vector<bool> mu3_isGlobal_NoVtx, mu3_isTracker_NoVtx, mu3_isGlobal_Vtx, mu3_isTracker_Vtx;
    std::vector<bool> mu4_isGlobal_NoVtx, mu4_isTracker_NoVtx, mu4_isGlobal_Vtx, mu4_isTracker_Vtx;
    std::vector<float> mu1_pt_NoVtx, mu1_eta_NoVtx, mu1_phi_NoVtx, mu1_chi2Ndof_NoVtx;
    std::vector<float> mu1_pt_Vtx,  mu1_eta_Vtx,  mu1_phi_Vtx,  mu1_chi2Ndof_Vtx;
    std::vector<float> mu1_ecalIso_NoVtx,  mu1_hcalIso_NoVtx,  mu1_trackIso_NoVtx;
    std::vector<float> mu1_ecalIso_Vtx,  mu1_hcalIso_Vtx,  mu1_trackIso_Vtx;
    std::vector<float> mu2_pt_NoVtx, mu2_eta_NoVtx, mu2_phi_NoVtx, mu2_chi2Ndof_NoVtx;
    std::vector<float> mu2_pt_Vtx,  mu2_eta_Vtx,  mu2_phi_Vtx,  mu2_chi2Ndof_Vtx;
    std::vector<float> mu2_ecalIso_NoVtx,  mu2_hcalIso_NoVtx,  mu2_trackIso_NoVtx;
    std::vector<float> mu2_ecalIso_Vtx,  mu2_hcalIso_Vtx,  mu2_trackIso_Vtx;
    std::vector<float> mu3_pt_NoVtx, mu3_eta_NoVtx, mu3_phi_NoVtx, mu3_chi2Ndof_NoVtx;
    std::vector<float> mu3_pt_Vtx,  mu3_eta_Vtx,  mu3_phi_Vtx,  mu3_chi2Ndof_Vtx;
    std::vector<float> mu3_ecalIso_NoVtx,  mu3_hcalIso_NoVtx,  mu3_trackIso_NoVtx;
    std::vector<float> mu3_ecalIso_Vtx,  mu3_hcalIso_Vtx,  mu3_trackIso_Vtx;
    std::vector<float> mu4_pt_NoVtx, mu4_eta_NoVtx, mu4_phi_NoVtx, mu4_chi2Ndof_NoVtx;
    std::vector<float> mu4_pt_Vtx,  mu4_eta_Vtx,  mu4_phi_Vtx,  mu4_chi2Ndof_Vtx;
    std::vector<float> mu4_ecalIso_NoVtx,  mu4_hcalIso_NoVtx,  mu4_trackIso_NoVtx;
    std::vector<float> mu4_ecalIso_Vtx,  mu4_hcalIso_Vtx,  mu4_trackIso_Vtx;
    std::vector<std::vector<int>> mu1_vtxIdx_NoVtx, mu1_vtxIdx_Vtx;
    std::vector<std::vector<int>> mu2_vtxIdx_NoVtx, mu2_vtxIdx_Vtx;
    std::vector<std::vector<int>> mu3_vtxIdx_NoVtx, mu3_vtxIdx_Vtx;
    std::vector<std::vector<int>> mu4_vtxIdx_NoVtx, mu4_vtxIdx_Vtx;

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

  SV1_ndof_NoVtx.clear(); SV1_ndof_Vtx.clear();
  SV1_chi2_NoVtx.clear(); SV1_prob_NoVtx.clear(); SV1_lxy_NoVtx.clear();
  SV1_chi2_Vtx.clear();  SV1_prob_Vtx.clear();  SV1_lxy_Vtx.clear();
  SV1_global_NoVtx.clear(); SV1_global_Vtx.clear(); 
  SV2_ndof_NoVtx.clear(); SV2_ndof_Vtx.clear();
  SV2_chi2_NoVtx.clear(); SV2_prob_NoVtx.clear(); SV2_lxy_NoVtx.clear();
  SV2_chi2_Vtx.clear();  SV2_prob_Vtx.clear();  SV2_lxy_Vtx.clear();
  SV2_global_NoVtx.clear(); SV2_global_Vtx.clear(); 
  SV1_px_Vtx.clear(); SV1_py_Vtx.clear(); SV1_pt_Vtx.clear(); SV1_dphi_Vtx.clear();
  SV2_px_Vtx.clear(); SV2_py_Vtx.clear(); SV2_pt_Vtx.clear(); SV2_dphi_Vtx.clear();
  SV1_px_NoVtx.clear(); SV1_py_NoVtx.clear(); SV1_pt_NoVtx.clear(); SV1_dphi_NoVtx.clear();
  SV2_px_NoVtx.clear(); SV2_py_NoVtx.clear(); SV2_pt_NoVtx.clear(); SV2_dphi_NoVtx.clear();
  
  nmu_NoVtx.clear(); nmu_Vtx.clear();

  mu1_isGlobal_NoVtx.clear(); mu1_isTracker_NoVtx.clear(); mu1_isGlobal_Vtx.clear(); mu1_isTracker_Vtx.clear();
  mu1_pt_NoVtx.clear(); mu1_eta_NoVtx.clear(); mu1_phi_NoVtx.clear(); mu1_chi2Ndof_NoVtx.clear();
  mu1_pt_Vtx.clear(); mu1_eta_Vtx.clear(); mu1_phi_Vtx.clear(); mu1_chi2Ndof_Vtx.clear();
  mu1_vtxIdx_NoVtx.clear(); mu1_vtxIdx_Vtx.clear(); mu1_ecalIso_Vtx.clear(); mu1_hcalIso_Vtx.clear(); mu1_trackIso_Vtx.clear();
  mu2_ecalIso_Vtx.clear(); mu2_hcalIso_Vtx.clear(); mu2_trackIso_Vtx.clear();
  mu3_ecalIso_Vtx.clear(); mu3_hcalIso_Vtx.clear(); mu3_trackIso_Vtx.clear();
  mu4_ecalIso_Vtx.clear(); mu4_hcalIso_Vtx.clear(); mu4_trackIso_Vtx.clear();
  mu1_ecalIso_NoVtx.clear(); mu1_hcalIso_NoVtx.clear(); mu1_trackIso_NoVtx.clear();
  mu2_ecalIso_NoVtx.clear(); mu2_hcalIso_NoVtx.clear(); mu2_trackIso_NoVtx.clear();
  mu3_ecalIso_NoVtx.clear(); mu3_hcalIso_NoVtx.clear(); mu3_trackIso_NoVtx.clear();
  mu4_ecalIso_NoVtx.clear(); mu4_hcalIso_NoVtx.clear(); mu4_trackIso_NoVtx.clear();
  mu2_isGlobal_NoVtx.clear(); mu2_isTracker_NoVtx.clear(); mu2_isGlobal_Vtx.clear(); mu2_isTracker_Vtx.clear();
  mu2_pt_NoVtx.clear(); mu2_eta_NoVtx.clear(); mu2_phi_NoVtx.clear(); mu2_chi2Ndof_NoVtx.clear();
  mu2_pt_Vtx.clear(); mu2_eta_Vtx.clear(); mu2_phi_Vtx.clear(); mu2_chi2Ndof_Vtx.clear();
  mu2_vtxIdx_NoVtx.clear(); mu2_vtxIdx_Vtx.clear();
  mu3_isGlobal_NoVtx.clear(); mu3_isTracker_NoVtx.clear(); mu3_isGlobal_Vtx.clear(); mu3_isTracker_Vtx.clear();
  mu3_pt_NoVtx.clear(); mu3_eta_NoVtx.clear(); mu3_phi_NoVtx.clear(); mu3_chi2Ndof_NoVtx.clear();
  mu3_pt_Vtx.clear(); mu3_eta_Vtx.clear(); mu3_phi_Vtx.clear(); mu3_chi2Ndof_Vtx.clear();
  mu3_vtxIdx_NoVtx.clear(); mu3_vtxIdx_Vtx.clear();
  mu4_isGlobal_NoVtx.clear(); mu4_isTracker_NoVtx.clear(); mu4_isGlobal_Vtx.clear(); mu4_isTracker_Vtx.clear();
  mu4_pt_NoVtx.clear(); mu4_eta_NoVtx.clear(); mu4_phi_NoVtx.clear(); mu4_chi2Ndof_NoVtx.clear();
  mu4_pt_Vtx.clear(); mu4_eta_Vtx.clear(); mu4_phi_Vtx.clear(); mu4_chi2Ndof_Vtx.clear();
  mu4_vtxIdx_NoVtx.clear(); mu4_vtxIdx_Vtx.clear();

  const auto& muonCollectionVtx = *ScoutingmuonsVtx;
  const auto& muonCollectionNoVtx = *ScoutingmuonsNoVtx;
  unsigned int nMus_Vtx = muonCollectionVtx.size();
  unsigned int nMus_NoVtx = muonCollectionNoVtx.size();

  nmu_NoVtx.push_back(nMus_NoVtx);
  nmu_Vtx.push_back(nMus_Vtx);

  /////////////////////////////////////////////////////////////////////
  ////////////////////// VTX COLLECTION   /////////////////////////////
  /////////////////////////////////////////////////////////////////////

  for (unsigned int iMu = 0; iMu < nMus_Vtx; ++iMu) {
    const auto& mu = muonCollectionVtx[iMu];

    if (mu.pt() < min_Pt) continue;
    if (std::abs(mu.eta()) > max_eta) continue;

    if (iMu == 0){
      mu1_pt_Vtx.push_back(mu.pt());
      mu1_eta_Vtx.push_back(mu.eta());
      mu1_phi_Vtx.push_back(mu.phi());
      mu1_chi2Ndof_Vtx.push_back(mu.normalizedChi2());
      mu1_vtxIdx_Vtx.push_back(mu.vtxIndx());
      mu1_isGlobal_Vtx.push_back(mu.isGlobalMuon());
      mu1_isTracker_Vtx.push_back(mu.isTrackerMuon());
      mu1_ecalIso_Vtx.push_back(mu.ecalIso());
      mu1_hcalIso_Vtx.push_back(mu.hcalIso());
      mu1_trackIso_Vtx.push_back(mu.trackIso());
    }
    if (iMu == 1){
      mu2_pt_Vtx.push_back(mu.pt());
      mu2_eta_Vtx.push_back(mu.eta());
      mu2_phi_Vtx.push_back(mu.phi());
      mu2_chi2Ndof_Vtx.push_back(mu.normalizedChi2());
      mu2_vtxIdx_Vtx.push_back(mu.vtxIndx());
      mu2_isGlobal_Vtx.push_back(mu.isGlobalMuon());
      mu2_isTracker_Vtx.push_back(mu.isTrackerMuon());
      mu2_ecalIso_Vtx.push_back(mu.ecalIso());
      mu2_hcalIso_Vtx.push_back(mu.hcalIso());
      mu2_trackIso_Vtx.push_back(mu.trackIso());
    }
    if (iMu == 2){
      mu3_pt_Vtx.push_back(mu.pt());
      mu3_eta_Vtx.push_back(mu.eta());
      mu3_phi_Vtx.push_back(mu.phi());
      mu3_chi2Ndof_Vtx.push_back(mu.normalizedChi2());
      mu3_vtxIdx_Vtx.push_back(mu.vtxIndx());
      mu3_isGlobal_Vtx.push_back(mu.isGlobalMuon());
      mu3_isTracker_Vtx.push_back(mu.isTrackerMuon());
      mu3_ecalIso_Vtx.push_back(mu.ecalIso());
      mu3_hcalIso_Vtx.push_back(mu.hcalIso());
      mu3_trackIso_Vtx.push_back(mu.trackIso());
    }
    if (iMu == 3){
      mu4_pt_Vtx.push_back(mu.pt());
      mu4_eta_Vtx.push_back(mu.eta());
      mu4_phi_Vtx.push_back(mu.phi());
      mu4_chi2Ndof_Vtx.push_back(mu.normalizedChi2());
      mu4_vtxIdx_Vtx.push_back(mu.vtxIndx());
      mu4_isGlobal_Vtx.push_back(mu.isGlobalMuon());
      mu4_isTracker_Vtx.push_back(mu.isTrackerMuon());
      mu4_ecalIso_Vtx.push_back(mu.ecalIso());
      mu4_hcalIso_Vtx.push_back(mu.hcalIso());
      mu4_trackIso_Vtx.push_back(mu.trackIso());
    }

    int charge1 = mu.charge();
    float chi2_1 = mu.trk_chi2();
    float ndof1 = mu.trk_ndof();

    float px1 = mu.trk_pt() * std::cos(mu.trk_phi());  
    float py1 = mu.trk_pt() * std::sin(mu.trk_phi());  
    float pz1 = mu.trk_pt() * std::sinh(mu.trk_eta()); 

    reco::TrackBase::Vector momentum1(px1, py1, pz1);

    reco::TrackBase::Point refPoint1(
      mu.trk_vx(),
      mu.trk_vy(),
      mu.trk_vz()
    );

    reco::TrackBase::CovarianceMatrix cov1 = reco::TrackBase::CovarianceMatrix();
    cov1(0,0) = mu.trk_qoverpError()*mu.trk_qoverpError();
    cov1(1,1) = mu.trk_lambdaError()*mu.trk_lambdaError();
    cov1(2,2) = mu.trk_phiError()*mu.trk_phiError();
    cov1(3,3) = mu.trk_dxyError()*mu.trk_dxyError();
    cov1(4,4) = mu.trk_dszError()*mu.trk_dszError();

    cov1(0,1) = mu.trk_qoverp_lambda_cov();
    cov1(1,0) = mu.trk_qoverp_lambda_cov();
    cov1(0,2) = mu.trk_qoverp_phi_cov();
    cov1(2,0) = mu.trk_qoverp_phi_cov();
    cov1(0,3) = mu.trk_qoverp_dxy_cov();
    cov1(3,0) = mu.trk_qoverp_dxy_cov();
    cov1(0,4) = mu.trk_qoverp_dsz_cov();
    cov1(4,0) = mu.trk_qoverp_dsz_cov();

    cov1(1,2) = mu.trk_lambda_phi_cov();
    cov1(2,1) = mu.trk_lambda_phi_cov();
    cov1(1,3) = mu.trk_lambda_dxy_cov();
    cov1(3,1) = mu.trk_lambda_dxy_cov();
    cov1(1,4) = mu.trk_lambda_dsz_cov();
    cov1(4,1) = mu.trk_lambda_dsz_cov();

    cov1(2,3) = mu.trk_phi_dxy_cov();
    cov1(3,2) = mu.trk_phi_dxy_cov();
    cov1(2,4) = mu.trk_phi_dsz_cov();
    cov1(4,2) = mu.trk_phi_dsz_cov();

    cov1(3,4) = mu.trk_dxy_dsz_cov();
    cov1(4,3) = mu.trk_dxy_dsz_cov();

    reco::Track track1(chi2_1,
      ndof1,
      refPoint1,
      momentum1,
      charge1,
      cov1,
      reco::TrackBase::undefAlgorithm,
      reco::TrackBase::undefQuality
    );

    allTracksTT_Vtx.push_back({theTransientTrackBuilder.build(track1), mu.isGlobalMuon(), mu.isTrackerMuon(), px1, py1});
  }
  int counter_Vtx = 0;
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

          float sv_px = t1.px + t2.px;
          float sv_py = t1.py + t2.py;
          float sv_pt = std::hypot(sv_px, sv_py);
          float sv_dphi = (vtxPos.x() * sv_px + vtxPos.y() * sv_py) / (lxy * sv_pt);

          if (counter_Vtx == 0){
            counter_Vtx++;
            SV1_lxy_Vtx.push_back(lxy);
            SV1_prob_Vtx.push_back(vtxProb);
            SV1_chi2_Vtx.push_back(fittedVertex.totalChiSquared()); 
            if (globalVertex) SV1_global_Vtx.push_back(true);
            else  SV1_global_Vtx.push_back(false);
            SV1_px_Vtx.push_back(sv_px);
            SV1_py_Vtx.push_back(sv_py);
            SV1_pt_Vtx.push_back(sv_pt);
            SV1_dphi_Vtx.push_back(sv_dphi);
          }
          else if (counter_Vtx == 1){
            counter_Vtx++;
            SV2_lxy_Vtx.push_back(lxy);
            SV2_prob_Vtx.push_back(vtxProb);
            SV2_chi2_Vtx.push_back(fittedVertex.totalChiSquared()); 
            if (globalVertex) SV2_global_Vtx.push_back(true);
            else  SV2_global_Vtx.push_back(false);
            SV2_px_Vtx.push_back(sv_px);
            SV2_py_Vtx.push_back(sv_py);
            SV2_pt_Vtx.push_back(sv_pt);
            SV2_dphi_Vtx.push_back(sv_dphi);
          }
        }
      }
    }
  }

  /////////////////////////////////////////////////////////////////////
  ////////////////////  No VTX COLLECTION   ///////////////////////////
  /////////////////////////////////////////////////////////////////////

  for (unsigned int iMu = 0; iMu < nMus_NoVtx; ++iMu) {
    const auto& mu = muonCollectionNoVtx[iMu];
    if (mu.pt() < min_Pt) continue;
    if (std::abs(mu.eta()) > max_eta) continue;

    if (iMu == 0){
      mu1_pt_NoVtx.push_back(mu.pt());
      mu1_eta_NoVtx.push_back(mu.eta());
      mu1_phi_NoVtx.push_back(mu.phi());
      mu1_chi2Ndof_NoVtx.push_back(mu.normalizedChi2());
      mu1_vtxIdx_NoVtx.push_back(mu.vtxIndx());
      mu1_isGlobal_NoVtx.push_back(mu.isGlobalMuon());
      mu1_isTracker_NoVtx.push_back(mu.isTrackerMuon());
      mu1_ecalIso_NoVtx.push_back(mu.ecalIso());
      mu1_hcalIso_NoVtx.push_back(mu.hcalIso());
      mu1_trackIso_NoVtx.push_back(mu.trackIso());
    }
    if (iMu == 1){
      mu2_pt_NoVtx.push_back(mu.pt());
      mu2_eta_NoVtx.push_back(mu.eta());
      mu2_phi_NoVtx.push_back(mu.phi());
      mu2_chi2Ndof_NoVtx.push_back(mu.normalizedChi2());
      mu2_vtxIdx_NoVtx.push_back(mu.vtxIndx());
      mu2_isGlobal_NoVtx.push_back(mu.isGlobalMuon());
      mu2_isTracker_NoVtx.push_back(mu.isTrackerMuon());
      mu2_ecalIso_NoVtx.push_back(mu.ecalIso());
      mu2_hcalIso_NoVtx.push_back(mu.hcalIso());
      mu2_trackIso_NoVtx.push_back(mu.trackIso());
    }
    if (iMu == 2){
      mu3_pt_NoVtx.push_back(mu.pt());
      mu3_eta_NoVtx.push_back(mu.eta());
      mu3_phi_NoVtx.push_back(mu.phi());
      mu3_chi2Ndof_NoVtx.push_back(mu.normalizedChi2());
      mu3_vtxIdx_NoVtx.push_back(mu.vtxIndx());
      mu3_isGlobal_NoVtx.push_back(mu.isGlobalMuon());
      mu3_isTracker_NoVtx.push_back(mu.isTrackerMuon());
      mu3_ecalIso_NoVtx.push_back(mu.ecalIso());
      mu3_hcalIso_NoVtx.push_back(mu.hcalIso());
      mu3_trackIso_NoVtx.push_back(mu.trackIso());
    }
    if (iMu == 3){
      mu4_pt_NoVtx.push_back(mu.pt());
      mu4_eta_NoVtx.push_back(mu.eta());
      mu4_phi_NoVtx.push_back(mu.phi());
      mu4_chi2Ndof_NoVtx.push_back(mu.normalizedChi2());
      mu4_vtxIdx_NoVtx.push_back(mu.vtxIndx());
      mu4_isGlobal_NoVtx.push_back(mu.isGlobalMuon());
      mu4_isTracker_NoVtx.push_back(mu.isTrackerMuon());
      mu4_ecalIso_NoVtx.push_back(mu.ecalIso());
      mu4_hcalIso_NoVtx.push_back(mu.hcalIso());
      mu4_trackIso_NoVtx.push_back(mu.trackIso());
    }

    int charge1 = mu.charge();
    float chi2_1 = mu.trk_chi2();
    float ndof1 = mu.trk_ndof();

    float px1 = mu.trk_pt() * std::cos(mu.trk_phi());  
    float py1 = mu.trk_pt() * std::sin(mu.trk_phi());  
    float pz1 = mu.trk_pt() * std::sinh(mu.trk_eta()); 

    reco::TrackBase::Vector momentum1(px1, py1, pz1);

    reco::TrackBase::Point refPoint1(
      mu.trk_vx(),
      mu.trk_vy(),
      mu.trk_vz()
    );

    reco::TrackBase::CovarianceMatrix cov1 = reco::TrackBase::CovarianceMatrix();
    cov1(0,0) = mu.trk_qoverpError()*mu.trk_qoverpError();
    cov1(1,1) = mu.trk_lambdaError()*mu.trk_lambdaError();
    cov1(2,2) = mu.trk_phiError()*mu.trk_phiError();
    cov1(3,3) = mu.trk_dxyError()*mu.trk_dxyError();
    cov1(4,4) = mu.trk_dszError()*mu.trk_dszError();

    cov1(0,1) = mu.trk_qoverp_lambda_cov();
    cov1(1,0) = mu.trk_qoverp_lambda_cov();
    cov1(0,2) = mu.trk_qoverp_phi_cov();
    cov1(2,0) = mu.trk_qoverp_phi_cov();
    cov1(0,3) = mu.trk_qoverp_dxy_cov();
    cov1(3,0) = mu.trk_qoverp_dxy_cov();
    cov1(0,4) = mu.trk_qoverp_dsz_cov();
    cov1(4,0) = mu.trk_qoverp_dsz_cov();

    cov1(1,2) = mu.trk_lambda_phi_cov();
    cov1(2,1) = mu.trk_lambda_phi_cov();
    cov1(1,3) = mu.trk_lambda_dxy_cov();
    cov1(3,1) = mu.trk_lambda_dxy_cov();
    cov1(1,4) = mu.trk_lambda_dsz_cov();
    cov1(4,1) = mu.trk_lambda_dsz_cov();

    cov1(2,3) = mu.trk_phi_dxy_cov();
    cov1(3,2) = mu.trk_phi_dxy_cov();
    cov1(2,4) = mu.trk_phi_dsz_cov();
    cov1(4,2) = mu.trk_phi_dsz_cov();

    cov1(3,4) = mu.trk_dxy_dsz_cov();
    cov1(4,3) = mu.trk_dxy_dsz_cov();

    reco::Track track1(chi2_1,
      ndof1,
      refPoint1,
      momentum1,
      charge1,
      cov1,
      reco::TrackBase::undefAlgorithm,
      reco::TrackBase::undefQuality
    );

    allTracksTT_NoVtx.push_back({theTransientTrackBuilder.build(track1), mu.isGlobalMuon(), mu.isTrackerMuon(), px1, py1});
  }

  int counter_NoVtx = 0;
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
          float sv_px = t1.px + t2.px;
          float sv_py = t1.py + t2.py;
          float sv_pt = std::hypot(sv_px, sv_py);
          float sv_dphi = (vtxPos.x() * sv_px + vtxPos.y() * sv_py) / (lxy * sv_pt);


          if (counter_NoVtx == 0){
            counter_NoVtx++;
            SV1_lxy_NoVtx.push_back(lxy);
            SV1_prob_NoVtx.push_back(vtxProb);
            SV1_chi2_NoVtx.push_back(fittedVertex.totalChiSquared()); 
            if (globalVertex) SV1_global_NoVtx.push_back(true);
            else  SV1_global_NoVtx.push_back(false);
            SV1_px_NoVtx.push_back(sv_px);
            SV1_py_NoVtx.push_back(sv_py);
            SV1_pt_NoVtx.push_back(sv_pt);
            SV1_dphi_NoVtx.push_back(sv_dphi);
          }
          else if (counter_NoVtx == 1){
            counter_NoVtx++;
            SV2_lxy_NoVtx.push_back(lxy);
            SV2_prob_NoVtx.push_back(vtxProb);
            SV2_chi2_NoVtx.push_back(fittedVertex.totalChiSquared()); 
            if (globalVertex) SV2_global_NoVtx.push_back(true);
            else  SV2_global_NoVtx.push_back(false);
            SV2_px_NoVtx.push_back(sv_px);
            SV2_py_NoVtx.push_back(sv_py);
            SV2_dphi_NoVtx.push_back(sv_dphi);
            SV2_pt_NoVtx.push_back(sv_pt);
          }
        }
      }
    }
  }
  if (!SV1_lxy_Vtx.empty() || !SV1_lxy_NoVtx.empty()) {
    tout->Fill();
  }
}


void BDT_ntuplizer::beginJob() {
  edm::Service<TFileService> fs;

  fout = new TFile("root_output/output.root", "RECREATE");
  tout = new TTree("tout","Run3ScoutingTree");

  tout->Branch("run", &run);
  tout->Branch("lumi", &lumi);
  tout->Branch("evtn", &evtn);
  
  // ===================== NoVtx SV =====================
  tout->Branch("SV1_chi2_NoVtx", &SV1_chi2_NoVtx);
  tout->Branch("SV1_prob_NoVtx", &SV1_prob_NoVtx);
  tout->Branch("SV1_lxy_NoVtx",  &SV1_lxy_NoVtx);
  tout->Branch("SV1_global_NoVtx",  &SV1_global_NoVtx);
  tout->Branch("SV1_px_NoVtx", &SV1_px_NoVtx);
  tout->Branch("SV1_py_NoVtx", &SV1_py_NoVtx);
  tout->Branch("SV1_pt_NoVtx", &SV1_pt_NoVtx);
  tout->Branch("SV1_dphi_NoVtx", &SV1_dphi_NoVtx);

  tout->Branch("SV2_chi2_NoVtx", &SV2_chi2_NoVtx);
  tout->Branch("SV2_prob_NoVtx", &SV2_prob_NoVtx);
  tout->Branch("SV2_lxy_NoVtx",  &SV2_lxy_NoVtx);
  tout->Branch("SV2_global_NoVtx",  &SV2_global_NoVtx);
  tout->Branch("SV2_px_NoVtx", &SV2_px_NoVtx);
  tout->Branch("SV2_py_NoVtx", &SV2_py_NoVtx);
  tout->Branch("SV2_pt_NoVtx", &SV2_pt_NoVtx);
  tout->Branch("SV2_dphi_NoVtx", &SV2_dphi_NoVtx);

  // ===================== NoVtx muons =====================
  tout->Branch("nmu_NoVtx", &nmu_NoVtx);

  tout->Branch("mu1_isGlobal_NoVtx", &mu1_isGlobal_NoVtx);
  tout->Branch("mu1_isTracker_NoVtx", &mu1_isTracker_NoVtx);
  tout->Branch("mu1_pt_NoVtx", &mu1_pt_NoVtx);
  tout->Branch("mu1_eta_NoVtx", &mu1_eta_NoVtx);
  tout->Branch("mu1_phi_NoVtx", &mu1_phi_NoVtx);
  tout->Branch("mu1_chi2Ndof_NoVtx", &mu1_chi2Ndof_NoVtx);
  tout->Branch("mu1_vtxIdx_NoVtx", &mu1_vtxIdx_NoVtx);
  tout->Branch("mu1_ecalIso_NoVtx", &mu1_ecalIso_NoVtx);
  tout->Branch("mu1_hcalIso_NoVtx", &mu1_hcalIso_NoVtx);
  tout->Branch("mu1_trackIso_NoVtx", &mu1_trackIso_NoVtx);

  tout->Branch("mu2_isGlobal_NoVtx", &mu2_isGlobal_NoVtx);
  tout->Branch("mu2_isTracker_NoVtx", &mu2_isTracker_NoVtx);
  tout->Branch("mu2_pt_NoVtx", &mu2_pt_NoVtx);
  tout->Branch("mu2_eta_NoVtx", &mu2_eta_NoVtx);
  tout->Branch("mu2_phi_NoVtx", &mu2_phi_NoVtx);
  tout->Branch("mu2_chi2Ndof_NoVtx", &mu2_chi2Ndof_NoVtx);
  tout->Branch("mu2_vtxIdx_NoVtx", &mu2_vtxIdx_NoVtx);
  tout->Branch("mu2_ecalIso_NoVtx", &mu2_ecalIso_NoVtx);
  tout->Branch("mu2_hcalIso_NoVtx", &mu2_hcalIso_NoVtx);
  tout->Branch("mu2_trackIso_NoVtx", &mu2_trackIso_Vtx);

  tout->Branch("mu3_isGlobal_NoVtx", &mu3_isGlobal_NoVtx);
  tout->Branch("mu3_isTracker_NoVtx", &mu3_isTracker_NoVtx);
  tout->Branch("mu3_pt_NoVtx", &mu3_pt_NoVtx);
  tout->Branch("mu3_eta_NoVtx", &mu3_eta_NoVtx);
  tout->Branch("mu3_phi_NoVtx", &mu3_phi_NoVtx);
  tout->Branch("mu3_chi2Ndof_NoVtx", &mu3_chi2Ndof_NoVtx);
  tout->Branch("mu3_vtxIdx_NoVtx", &mu3_vtxIdx_NoVtx);
  tout->Branch("mu3_ecalIso_NoVtx", &mu3_ecalIso_NoVtx);
  tout->Branch("mu3_hcalIso_NoVtx", &mu3_hcalIso_NoVtx);
  tout->Branch("mu3_trackIso_NoVtx", &mu3_trackIso_NoVtx);

  tout->Branch("mu4_isGlobal_NoVtx", &mu4_isGlobal_NoVtx);
  tout->Branch("mu4_isTracker_NoVtx", &mu4_isTracker_NoVtx);
  tout->Branch("mu4_pt_NoVtx", &mu4_pt_NoVtx);
  tout->Branch("mu4_eta_NoVtx", &mu4_eta_NoVtx);
  tout->Branch("mu4_phi_NoVtx", &mu4_phi_NoVtx);
  tout->Branch("mu4_chi2Ndof_NoVtx", &mu4_chi2Ndof_NoVtx);
  tout->Branch("mu4_vtxIdx_NoVtx", &mu4_vtxIdx_NoVtx);
  tout->Branch("mu4_ecalIso_NoVtx", &mu4_ecalIso_NoVtx);
  tout->Branch("mu4_hcalIso_NoVtx", &mu4_hcalIso_NoVtx);
  tout->Branch("mu4_trackIso_NoVtx", &mu4_trackIso_NoVtx);

  // ===================== Vtx SV =====================
  tout->Branch("SV1_chi2_Vtx", &SV1_chi2_Vtx);
  tout->Branch("SV1_prob_Vtx", &SV1_prob_Vtx);
  tout->Branch("SV1_lxy_Vtx",  &SV1_lxy_Vtx);
  tout->Branch("SV1_global_Vtx",  &SV1_global_Vtx);
  tout->Branch("SV1_px_Vtx", &SV1_px_Vtx);
  tout->Branch("SV1_py_Vtx", &SV1_py_Vtx);
  tout->Branch("SV1_pt_Vtx", &SV1_pt_Vtx);
  tout->Branch("SV1_dphi_Vtx", &SV1_dphi_Vtx);

  tout->Branch("SV2_chi2_Vtx", &SV2_chi2_Vtx);
  tout->Branch("SV2_prob_Vtx", &SV2_prob_Vtx);
  tout->Branch("SV2_lxy_Vtx",  &SV2_lxy_Vtx);
  tout->Branch("SV2_global_Vtx",  &SV2_global_Vtx);
  tout->Branch("SV2_px_Vtx", &SV2_px_Vtx);
  tout->Branch("SV2_py_Vtx", &SV2_py_Vtx);
  tout->Branch("SV2_pt_Vtx", &SV2_pt_Vtx);
  tout->Branch("SV2_dphi_Vtx", &SV2_dphi_Vtx);

  // ===================== Vtx muons =====================
  tout->Branch("nmu_Vtx", &nmu_Vtx);

  tout->Branch("mu1_isGlobal_Vtx", &mu1_isGlobal_Vtx);
  tout->Branch("mu1_isTracker_Vtx", &mu1_isTracker_Vtx);
  tout->Branch("mu1_pt_Vtx", &mu1_pt_Vtx);
  tout->Branch("mu1_eta_Vtx", &mu1_eta_Vtx);
  tout->Branch("mu1_phi_Vtx", &mu1_phi_Vtx);
  tout->Branch("mu1_chi2Ndof_Vtx", &mu1_chi2Ndof_Vtx);
  tout->Branch("mu1_vtxIdx_Vtx", &mu1_vtxIdx_Vtx);
  tout->Branch("mu1_ecalIso_Vtx", &mu1_ecalIso_Vtx);
  tout->Branch("mu1_hcalIso_Vtx", &mu1_hcalIso_Vtx);
  tout->Branch("mu1_trackIso_Vtx", &mu1_trackIso_Vtx);

  tout->Branch("mu2_isGlobal_Vtx", &mu2_isGlobal_Vtx);
  tout->Branch("mu2_isTracker_Vtx", &mu2_isTracker_Vtx);
  tout->Branch("mu2_pt_Vtx", &mu2_pt_Vtx);
  tout->Branch("mu2_eta_Vtx", &mu2_eta_Vtx);
  tout->Branch("mu2_phi_Vtx", &mu2_phi_Vtx);
  tout->Branch("mu2_chi2Ndof_Vtx", &mu2_chi2Ndof_Vtx);
  tout->Branch("mu2_vtxIdx_Vtx", &mu2_vtxIdx_Vtx);
  tout->Branch("mu2_ecalIso_Vtx", &mu2_ecalIso_Vtx);
  tout->Branch("mu2_hcalIso_Vtx", &mu2_hcalIso_Vtx);
  tout->Branch("mu2_trackIso_Vtx", &mu2_trackIso_Vtx);

  tout->Branch("mu3_isGlobal_Vtx", &mu3_isGlobal_Vtx);
  tout->Branch("mu3_isTracker_Vtx", &mu3_isTracker_Vtx);
  tout->Branch("mu3_pt_Vtx", &mu3_pt_Vtx);
  tout->Branch("mu3_eta_Vtx", &mu3_eta_Vtx);
  tout->Branch("mu3_phi_Vtx", &mu3_phi_Vtx);
  tout->Branch("mu3_chi2Ndof_Vtx", &mu3_chi2Ndof_Vtx);
  tout->Branch("mu3_vtxIdx_Vtx", &mu3_vtxIdx_Vtx);
  tout->Branch("mu3_ecalIso_Vtx", &mu3_ecalIso_Vtx);
  tout->Branch("mu3_hcalIso_Vtx", &mu3_hcalIso_Vtx);
  tout->Branch("mu3_trackIso_Vtx", &mu3_trackIso_Vtx);

  tout->Branch("mu4_isGlobal_Vtx", &mu4_isGlobal_Vtx);
  tout->Branch("mu4_isTracker_Vtx", &mu4_isTracker_Vtx);
  tout->Branch("mu4_pt_Vtx", &mu4_pt_Vtx);
  tout->Branch("mu4_eta_Vtx", &mu4_eta_Vtx);
  tout->Branch("mu4_phi_Vtx", &mu4_phi_Vtx);
  tout->Branch("mu4_chi2Ndof_Vtx", &mu4_chi2Ndof_Vtx);
  tout->Branch("mu4_vtxIdx_Vtx", &mu4_vtxIdx_Vtx);
  tout->Branch("mu4_ecalIso_Vtx", &mu4_ecalIso_Vtx);
  tout->Branch("mu4_hcalIso_Vtx", &mu4_hcalIso_Vtx);
  tout->Branch("mu4_trackIso_Vtx", &mu4_trackIso_Vtx);
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
