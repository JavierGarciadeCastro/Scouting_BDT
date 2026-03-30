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
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "TTree.h"

#include "RecoVertex/KalmanVertexFit/interface/KalmanVertexFitter.h"
#include "RecoVertex/VertexPrimitives/interface/TransientVertex.h"
#include "HLTrigger/HLTcore/interface/TriggerExpressionData.h"
#include "HLTrigger/HLTcore/interface/TriggerExpressionEvaluator.h"
#include "HLTrigger/HLTcore/interface/TriggerExpressionParser.h"
#include "L1Trigger/L1TGlobal/interface/L1TGlobalUtil.h"
#include "CommonTools/Utils/interface/StringCutObjectSelector.h"

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
    triggerExpression::Data triggerCache_;
    const std::vector<std::string> vtriggerSelection_;
    edm::EDGetToken algToken_;
    std::vector<triggerExpression::Evaluator*> vtriggerSelector_;
    std::shared_ptr<l1t::L1TGlobalUtil> l1GtUtils_;
    std::vector<std::string> l1Seeds_;
    TString l1Names[100] = {""};
    Bool_t l1Result[100] = {false};
    Bool_t hltResult[100] = {false}; 
    bool passL1, passHLT;



    unsigned int run, lumi, evtn;
    edm::EDGetTokenT<std::vector<Run3ScoutingMuon>> muTokenScoutingVtx_;
    edm::EDGetTokenT<std::vector<Run3ScoutingMuon>> muTokenScoutingNoVtx_;
    edm::EDGetTokenT<std::vector<Run3ScoutingVertex>> svTokenScouting_;
    edm::ESGetToken<TransientTrackBuilder, TransientTrackRecord> theTransientTrackBuilderToken_;
    edm::EDGetTokenT<std::vector<reco::GenParticle>> genToken_;
    
    TFile* fout;
    TTree* tout;

    std::vector<int> passTrigger_;
    
    // ===================== SV variables =====================
    std::vector<unsigned int> SV1_ndof_NoVtx, SV1_ndof_Vtx;
    std::vector<unsigned int> SV2_ndof_NoVtx, SV2_ndof_Vtx;
    std::vector<float> SV1_chi2_NoVtx, SV1_prob_NoVtx, SV1_chi2Ndof_NoVtx, SV1_lxy_NoVtx;
    std::vector<float> SV1_chi2_Vtx,  SV1_prob_Vtx,  SV1_chi2Ndof_Vtx,  SV1_lxy_Vtx;
    std::vector<float> SV2_chi2_NoVtx, SV2_prob_NoVtx, SV2_chi2Ndof_NoVtx, SV2_lxy_NoVtx;
    std::vector<float> SV1_px_NoVtx, SV1_py_NoVtx, SV1_pt_NoVtx, SV1_dphi_NoVtx, SV1_px_Vtx, SV1_py_Vtx, SV1_pt_Vtx, SV1_dphi_Vtx;
    std::vector<float> SV2_px_NoVtx, SV2_py_NoVtx, SV2_pt_NoVtx, SV2_dphi_NoVtx, SV2_px_Vtx, SV2_py_Vtx, SV2_pt_Vtx, SV2_dphi_Vtx;
    std::vector<float> SV2_3Dangle_NoVtx, SV1_3Dangle_NoVtx, SV2_3Dangle_Vtx, SV1_3Dangle_Vtx;
    std::vector<float> SV2_L3D_NoVtx, SV1_L3D_NoVtx, SV2_L3D_Vtx, SV1_L3D_Vtx;
    std::vector<float> SV2_chi2_Vtx,  SV2_prob_Vtx,  SV2_chi2Ndof_Vtx,  SV2_lxy_Vtx;
    std::vector<float> SV1_xErr_Vtx,  SV2_xErr_Vtx, SV1_yErr_Vtx, SV2_yErr_Vtx, SV1_zErr_Vtx, SV2_zErr_Vtx;
    std::vector<float> SV1_xErr_NoVtx,  SV2_xErr_NoVtx, SV1_yErr_NoVtx, SV2_yErr_NoVtx, SV1_zErr_NoVtx, SV2_zErr_NoVtx;
    std::vector<bool> SV1_global_NoVtx, SV1_global_Vtx, SV2_global_NoVtx, SV2_global_Vtx;
    std::vector<bool> SV1_mu1_NoVtx, SV1_mu2_NoVtx, SV2_mu1_NoVtx, SV2_mu2_NoVtx;
    std::vector<bool> SV1_mu1_Vtx, SV1_mu2_Vtx, SV2_mu1_Vtx, SV2_mu2_Vtx;

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
    std::vector<float> mu1_trk_dxy_NoVtx, mu2_trk_dxy_NoVtx, mu3_trk_dxy_NoVtx, mu4_trk_dxy_NoVtx;
    std::vector<float> mu1_trk_dxyError_NoVtx, mu2_trk_dxyError_NoVtx, mu3_trk_dxyError_NoVtx, mu4_trk_dxyError_NoVtx;
    std::vector<float> mu1_trk_dxy_Vtx, mu2_trk_dxy_Vtx, mu3_trk_dxy_Vtx, mu4_trk_dxy_Vtx;
    std::vector<float> mu1_trk_dxyError_Vtx, mu2_trk_dxyError_Vtx, mu3_trk_dxyError_Vtx, mu4_trk_dxyError_Vtx;
    std::vector<std::vector<int>> mu1_vtxIdx_NoVtx, mu1_vtxIdx_Vtx;
    std::vector<std::vector<int>> mu2_vtxIdx_NoVtx, mu2_vtxIdx_Vtx;
    std::vector<std::vector<int>> mu3_vtxIdx_NoVtx, mu3_vtxIdx_Vtx;
    std::vector<std::vector<int>> mu4_vtxIdx_NoVtx, mu4_vtxIdx_Vtx;

    //GEN particle variables (for gen-matching)
    std::vector<float> gen_pt, gen_eta, gen_phi;

    float min_Pt, max_eta;
};

//Constructor
BDT_ntuplizer::BDT_ntuplizer(const edm::ParameterSet& iConfig) :
  triggerCache_{triggerExpression::Data(iConfig.getParameterSet("triggerConfiguration"), consumesCollector())},
  vtriggerSelection_{iConfig.getParameter<vector<string>>("triggerSelection")},
  algToken_{consumes<BXVector<GlobalAlgBlk>>(iConfig.getParameter<edm::InputTag>("AlgInputTag"))},
  muTokenScoutingVtx_{consumes<std::vector<Run3ScoutingMuon>>(iConfig.getParameter<edm::InputTag>("ScoutingmuonsVtx"))},
  muTokenScoutingNoVtx_{consumes<std::vector<Run3ScoutingMuon>>(iConfig.getParameter<edm::InputTag>("ScoutingmuonsNoVtx"))},
  svTokenScouting_{consumes<std::vector<Run3ScoutingVertex>>(iConfig.getParameter<edm::InputTag>("hltScoutingMuonPacker_displacedVtx"))},
  theTransientTrackBuilderToken_{esConsumes(edm::ESInputTag("", "TransientTrackBuilder"))},
  genToken_{consumes<std::vector<reco::GenParticle>>(iConfig.getParameter<edm::InputTag>("genParticlesInputTag"))}
  {vtriggerSelector_.reserve(vtriggerSelection_.size());
    for (auto const& vt : vtriggerSelection_)
      vtriggerSelector_.push_back(triggerExpression::parse(vt));
    l1GtUtils_ = std::make_shared<l1t::L1TGlobalUtil>(iConfig, consumesCollector(), l1t::UseEventSetupIn::RunAndEvent);
    l1Seeds_ = iConfig.getParameter<std::vector<std::string>>("l1Seeds");
    for (unsigned int i = 0; i < l1Seeds_.size(); i++) {
      const auto& l1seed(l1Seeds_.at(i));
      l1Names[i] = TString(l1seed);
    }
  }

//Destructor
BDT_ntuplizer::~BDT_ntuplizer() = default;

void BDT_ntuplizer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
  run = iEvent.id().run();
  lumi = iEvent.id().luminosityBlock();
  evtn = iEvent.id().event();

  min_Pt = 3;
  max_eta = 2.5;
  float minVtxProb = 0.001;

  bool passL1 = false;
  bool passHLT = false;


  const auto& theTransientTrackBuilder = iSetup.getData(theTransientTrackBuilderToken_);
  edm::Handle<std::vector<Run3ScoutingMuon>> ScoutingmuonsVtx;
  edm::Handle<std::vector<Run3ScoutingMuon>> ScoutingmuonsNoVtx;
  edm::Handle<std::vector<Run3ScoutingVertex>> ScoutingdisplacedVertices;
  edm::Handle<std::vector<reco::GenParticle>> GenParts;

  iEvent.getByToken(muTokenScoutingVtx_, ScoutingmuonsVtx);
  iEvent.getByToken(muTokenScoutingNoVtx_, ScoutingmuonsNoVtx);
  iEvent.getByToken(svTokenScouting_, ScoutingdisplacedVertices);
  iEvent.getByToken(genToken_, GenParts);

  /////////////////////////////////////////////////////////////////////
  ///////////////////////// TRIGGERS //////////////////////////////////
  /////////////////////////////////////////////////////////////////////

  l1GtUtils_->retrieveL1(iEvent, iSetup, algToken_);
  passTrigger_.clear();

  for (unsigned int i = 0; i < l1Seeds_.size(); i++) {
    const auto& l1seed(l1Seeds_.at(i));
    bool l1htbit = false;
    double prescale = -1;
    l1GtUtils_->getFinalDecisionByName(l1seed, l1htbit);
    l1GtUtils_->getPrescaleByName(l1seed, prescale);
    l1Result[i] = l1htbit;
    if (l1Result[i] == 1){
      passL1 = true;
    }
  }
  
  if (triggerCache_.setEvent(iEvent, iSetup)) {
    for (unsigned int i = 0; i < vtriggerSelector_.size(); i++) {
      auto& vts(vtriggerSelector_.at(i));
      bool result = false;
      if (vts) {
        if (triggerCache_.configurationUpdated())
          vts->init(triggerCache_);
        result = (*vts)(triggerCache_);
      }
      hltResult[i] = result;
      if (result)
        passHLT = true;
    }
  }
  passTrigger_.push_back(passL1 && passHLT);

  /////////////////////////////////////////////////////////////////////
  //////////////////////// GEN PARTICLES //////////////////////////////
  /////////////////////////////////////////////////////////////////////

  gen_pt.clear(); gen_eta.clear(); gen_phi.clear();
  auto GenPart = *GenParts;
  unsigned int nGenParts = GenPart.size();

  for (unsigned int iGen = 0; iGen < nGenParts; ++iGen) {
    auto genpart = GenPart[iGen];
    
    if (abs(genpart.pdgId())==13 && genpart.status() == 1) {
    //if (abs(genpart.pdgId())==13) {
      gen_pt.push_back(genpart.pt());
      gen_eta.push_back(genpart.eta());
      gen_phi.push_back(genpart.phi());
    }
  }

  /////////////////////////////////////////////////////////////////////
  //////////////////////////// MUONS //////////////////////////////////
  /////////////////////////////////////////////////////////////////////

  struct TaggedTT {reco::TransientTrack tt; bool isGlobal; bool isTracker; float px; float py; float pz; int mu_index;};
  std::vector<TaggedTT> allTracksTT_NoVtx;
  std::vector<TaggedTT> allTracksTT_Vtx;

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
  SV2_3Dangle_NoVtx.clear(); SV1_3Dangle_NoVtx.clear(); SV2_3Dangle_Vtx.clear(); SV1_3Dangle_Vtx.clear();
  SV2_L3D_NoVtx.clear(); SV1_L3D_NoVtx.clear(); SV2_L3D_Vtx.clear(); SV1_L3D_Vtx.clear();
  SV1_xErr_NoVtx.clear(); SV2_xErr_NoVtx.clear(); SV1_yErr_NoVtx.clear(); SV2_yErr_NoVtx.clear(); SV1_zErr_NoVtx.clear(); SV2_zErr_NoVtx.clear(); 
  SV1_xErr_Vtx.clear(); SV2_xErr_Vtx.clear(); SV1_yErr_Vtx.clear(); SV2_yErr_Vtx.clear(); SV1_zErr_Vtx.clear(); SV2_zErr_Vtx.clear(); 
  SV1_mu1_Vtx.clear(); SV1_mu2_Vtx.clear(); SV2_mu1_Vtx.clear(); SV2_mu2_Vtx.clear(); 
  SV1_mu1_NoVtx.clear(); SV1_mu2_NoVtx.clear(); SV2_mu1_NoVtx.clear(); SV2_mu2_NoVtx.clear(); 
  
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
  mu1_trk_dxy_NoVtx.clear(); mu2_trk_dxy_NoVtx.clear(); mu3_trk_dxy_NoVtx.clear(); mu4_trk_dxy_NoVtx.clear(); 
  mu1_trk_dxyError_NoVtx.clear(); mu2_trk_dxyError_NoVtx.clear(); mu3_trk_dxyError_NoVtx.clear(); mu4_trk_dxyError_NoVtx.clear();
  mu1_trk_dxy_Vtx.clear(); mu2_trk_dxy_Vtx.clear(); mu3_trk_dxy_Vtx.clear(); mu4_trk_dxy_Vtx.clear(); 
  mu1_trk_dxyError_Vtx.clear(); mu2_trk_dxyError_Vtx.clear(); mu3_trk_dxyError_Vtx.clear(); mu4_trk_dxyError_Vtx.clear();

  const auto& muonCollectionVtx = *ScoutingmuonsVtx;
  const auto& muonCollectionNoVtx = *ScoutingmuonsNoVtx;
  unsigned int nMus_Vtx = muonCollectionVtx.size();
  unsigned int nMus_NoVtx = muonCollectionNoVtx.size();

  nmu_NoVtx.push_back(nMus_NoVtx);
  nmu_Vtx.push_back(nMus_Vtx);

  /////////////////////////////////////////////////////////////////////
  ////////////////////// VTX COLLECTION   /////////////////////////////
  /////////////////////////////////////////////////////////////////////

  int muCounter_Vtx = 0;

  for (unsigned int iMu = 0; iMu < nMus_Vtx; ++iMu) {
    const auto& mu = muonCollectionVtx[iMu];

    if (mu.pt() < min_Pt) continue;
    if (std::abs(mu.eta()) > max_eta) continue;

    if (muCounter_Vtx == 0){
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
      mu1_trk_dxy_Vtx.push_back(mu.trk_dxy());
      mu1_trk_dxyError_Vtx.push_back(mu.trk_dxyError());
    }
    else if (muCounter_Vtx == 1){
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
      mu2_trk_dxy_Vtx.push_back(mu.trk_dxy());
      mu2_trk_dxyError_Vtx.push_back(mu.trk_dxyError());
    }
    else if (muCounter_Vtx == 2){
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
      mu3_trk_dxy_Vtx.push_back(mu.trk_dxy());
      mu3_trk_dxyError_Vtx.push_back(mu.trk_dxyError());
    }
    else if (muCounter_Vtx == 3){
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
      mu4_trk_dxy_Vtx.push_back(mu.trk_dxy());
      mu4_trk_dxyError_Vtx.push_back(mu.trk_dxyError());
    }
    int muIndex = muCounter_Vtx;
    muCounter_Vtx++;

    int charge1 = mu.charge();
    float chi2_1 = mu.trk_chi2();
    float ndof1 = mu.trk_ndof();

    float px = mu.trk_pt() * std::cos(mu.trk_phi());  
    float py = mu.trk_pt() * std::sin(mu.trk_phi());  
    float pz = mu.trk_pt() * std::sinh(mu.trk_eta()); 

    reco::TrackBase::Vector momentum1(px, py, pz);

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
    allTracksTT_Vtx.push_back({theTransientTrackBuilder.build(track1), mu.isGlobalMuon(), mu.isTrackerMuon(), px, py, pz, muIndex});
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

          GlobalError vtxErr = fittedVertex.vertexState().error();
          float xErr = std::sqrt(vtxErr.cxx());
          float yErr = std::sqrt(vtxErr.cyy());
          float zErr = std::sqrt(vtxErr.czz());

          float lxy = std::hypot(vtxPos.x(), vtxPos.y());
          float L3D = std::sqrt(vtxPos.x()*vtxPos.x() + vtxPos.y()*vtxPos.y() + vtxPos.z()*vtxPos.z());

          float sv_px = t1.px + t2.px;
          float sv_py = t1.py + t2.py;
          float sv_pz = t1.pz + t2.pz;

          float sv_pt = std::hypot(sv_px, sv_py);
          float sv_p = std::sqrt(sv_px*sv_px + sv_py*sv_py + sv_pz*sv_pz);

          float sv_dphi = (vtxPos.x() * sv_px + vtxPos.y() * sv_py) / (lxy * sv_pt);
          float sv_3Dangle = (vtxPos.x() * sv_px + vtxPos.y() * sv_py + vtxPos.z() * sv_pz) / (L3D * sv_p);
          int sv_ndof = fittedVertex.degreesOfFreedom();

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
            SV1_L3D_Vtx.push_back(L3D);
            SV1_3Dangle_Vtx.push_back(sv_3Dangle);
            SV1_xErr_Vtx.push_back(xErr);
            SV1_yErr_Vtx.push_back(yErr);
            SV1_zErr_Vtx.push_back(zErr);
            SV1_mu1_Vtx.push_back(t1.mu_index);
            SV1_mu2_Vtx.push_back(t2.mu_index);
            SV1_ndof_Vtx.push_back(sv_ndof);
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
            SV2_L3D_Vtx.push_back(L3D);
            SV2_3Dangle_Vtx.push_back(sv_3Dangle);
            SV2_xErr_Vtx.push_back(xErr);
            SV2_yErr_Vtx.push_back(yErr);
            SV2_zErr_Vtx.push_back(zErr);
            SV2_mu1_Vtx.push_back(t1.mu_index);
            SV2_mu2_Vtx.push_back(t2.mu_index);
            SV2_ndof_Vtx.push_back(sv_ndof);
          }
        }
      }
    }
  }

  /////////////////////////////////////////////////////////////////////
  ////////////////////  No VTX COLLECTION   ///////////////////////////
  /////////////////////////////////////////////////////////////////////

  int muCounter_NoVtx = 0;

  for (unsigned int iMu = 0; iMu < nMus_NoVtx; ++iMu) {
    const auto& mu = muonCollectionNoVtx[iMu];
    if (mu.pt() < min_Pt) continue;
    if (std::abs(mu.eta()) > max_eta) continue;

    if (muCounter_NoVtx == 0){
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
      mu1_trk_dxy_NoVtx.push_back(mu.trk_dxy());
      mu1_trk_dxyError_NoVtx.push_back(mu.trk_dxyError());
    }
    else if (muCounter_NoVtx == 1){
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
      mu2_trk_dxy_NoVtx.push_back(mu.trk_dxy());
      mu2_trk_dxyError_NoVtx.push_back(mu.trk_dxyError());
    }
    else if (muCounter_NoVtx == 2){
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
      mu3_trk_dxy_NoVtx.push_back(mu.trk_dxy());
      mu3_trk_dxyError_NoVtx.push_back(mu.trk_dxyError());
    }
    else if (muCounter_NoVtx == 3){
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
      mu4_trk_dxy_NoVtx.push_back(mu.trk_dxy());
      mu4_trk_dxyError_NoVtx.push_back(mu.trk_dxyError());
    }

    int muIndex = muCounter_NoVtx;
    muCounter_NoVtx++;

    int charge1 = mu.charge();
    float chi2_1 = mu.trk_chi2();
    float ndof1 = mu.trk_ndof();

    float px = mu.trk_pt() * std::cos(mu.trk_phi());  
    float py = mu.trk_pt() * std::sin(mu.trk_phi());  
    float pz = mu.trk_pt() * std::sinh(mu.trk_eta()); 

    reco::TrackBase::Vector momentum1(px, py, pz);

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

    allTracksTT_NoVtx.push_back({theTransientTrackBuilder.build(track1), mu.isGlobalMuon(), mu.isTrackerMuon(), px, py, pz, muIndex});
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

          GlobalError vtxErr = fittedVertex.vertexState().error();
          float xErr = std::sqrt(vtxErr.cxx());
          float yErr = std::sqrt(vtxErr.cyy());
          float zErr = std::sqrt(vtxErr.czz());

          float lxy = std::hypot(vtxPos.x(), vtxPos.y());
          float L3D = std::sqrt(vtxPos.x()*vtxPos.x() + vtxPos.y()*vtxPos.y() + vtxPos.z()*vtxPos.z());

          float sv_px = t1.px + t2.px;
          float sv_py = t1.py + t2.py;
          float sv_pz = t1.pz + t2.pz;
          float sv_pt = std::hypot(sv_px, sv_py);
          float sv_p = std::sqrt(sv_px*sv_px + sv_py*sv_py + sv_pz*sv_pz);

          float sv_dphi = (vtxPos.x() * sv_px + vtxPos.y() * sv_py) / (lxy * sv_pt);
          float sv_3Dangle = (vtxPos.x() * sv_px + vtxPos.y() * sv_py + vtxPos.z() * sv_pz) / (L3D * sv_p);
          int sv_ndof = fittedVertex.degreesOfFreedom();


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
            SV1_L3D_NoVtx.push_back(L3D);
            SV1_3Dangle_NoVtx.push_back(sv_3Dangle);
            SV1_xErr_NoVtx.push_back(xErr);
            SV1_yErr_NoVtx.push_back(yErr);
            SV1_zErr_NoVtx.push_back(zErr);
            SV1_mu1_NoVtx.push_back(t1.mu_index);
            SV1_mu2_NoVtx.push_back(t2.mu_index);
            SV1_ndof_NoVtx.push_back(sv_ndof);
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
            SV2_L3D_NoVtx.push_back(L3D);
            SV2_3Dangle_NoVtx.push_back(sv_3Dangle);
            SV2_xErr_NoVtx.push_back(xErr);
            SV2_yErr_NoVtx.push_back(yErr);
            SV2_zErr_NoVtx.push_back(zErr);
            SV2_mu1_NoVtx.push_back(t1.mu_index);
            SV2_mu2_NoVtx.push_back(t2.mu_index);
            SV2_ndof_NoVtx.push_back(sv_ndof);
          }
        }
      }
    }
  }
  //if (!SV1_lxy_Vtx.empty() || !SV1_lxy_NoVtx.empty()) {
    tout->Fill();
  //}
}


void BDT_ntuplizer::beginJob() {
  edm::Service<TFileService> fs;

  fout = new TFile("root_output/output.root", "RECREATE");
  tout = new TTree("tout","Run3ScoutingTree");

  tout->Branch("run", &run);
  tout->Branch("lumi", &lumi);
  tout->Branch("evtn", &evtn);
  tout->Branch("passTrigger", &passTrigger_);

  // =================== Gen Variables ===================
  tout->Branch("gen_pt", &gen_pt);
  tout->Branch("gen_eta", &gen_eta);
  tout->Branch("gen_phi", &gen_phi);

  // ===================== NoVtx SV =====================
  tout->Branch("SV1_chi2_NoVtx", &SV1_chi2_NoVtx);
  tout->Branch("SV1_prob_NoVtx", &SV1_prob_NoVtx);
  tout->Branch("SV1_lxy_NoVtx",  &SV1_lxy_NoVtx);
  tout->Branch("SV1_global_NoVtx",  &SV1_global_NoVtx);
  tout->Branch("SV1_px_NoVtx", &SV1_px_NoVtx);
  tout->Branch("SV1_py_NoVtx", &SV1_py_NoVtx);
  tout->Branch("SV1_pt_NoVtx", &SV1_pt_NoVtx);
  tout->Branch("SV1_dphi_NoVtx", &SV1_dphi_NoVtx);
  tout->Branch("SV1_3Dangle_NoVtx", &SV1_3Dangle_NoVtx);
  tout->Branch("SV1_L3D_NoVtx", &SV1_L3D_NoVtx);
  tout->Branch("SV1_xErr_NoVtx", &SV1_xErr_NoVtx);
  tout->Branch("SV1_yErr_NoVtx", &SV1_yErr_NoVtx);
  tout->Branch("SV1_zErr_NoVtx", &SV1_zErr_NoVtx);
  tout->Branch("SV1_mu1_NoVtx", &SV1_mu1_NoVtx);
  tout->Branch("SV1_mu2_NoVtx", &SV1_mu2_NoVtx);
  tout->Branch("SV1_ndof_NoVtx", &SV1_ndof_NoVtx);


  tout->Branch("SV2_chi2_NoVtx", &SV2_chi2_NoVtx);
  tout->Branch("SV2_prob_NoVtx", &SV2_prob_NoVtx);
  tout->Branch("SV2_lxy_NoVtx",  &SV2_lxy_NoVtx);
  tout->Branch("SV2_global_NoVtx",  &SV2_global_NoVtx);
  tout->Branch("SV2_px_NoVtx", &SV2_px_NoVtx);
  tout->Branch("SV2_py_NoVtx", &SV2_py_NoVtx);
  tout->Branch("SV2_pt_NoVtx", &SV2_pt_NoVtx);
  tout->Branch("SV2_dphi_NoVtx", &SV2_dphi_NoVtx);
  tout->Branch("SV2_3Dangle_NoVtx", &SV2_3Dangle_NoVtx);
  tout->Branch("SV2_L3D_NoVtx", &SV2_L3D_NoVtx);
  tout->Branch("SV2_xErr_NoVtx", &SV2_xErr_NoVtx);
  tout->Branch("SV2_yErr_NoVtx", &SV2_yErr_NoVtx);
  tout->Branch("SV2_zErr_NoVtx", &SV2_zErr_NoVtx);
  tout->Branch("SV2_mu1_NoVtx", &SV2_mu1_NoVtx);
  tout->Branch("SV2_mu2_NoVtx", &SV2_mu2_NoVtx);
  tout->Branch("SV2_ndof_NoVtx", &SV2_ndof_NoVtx);

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
  tout->Branch("mu1_trk_dxy_NoVtx", &mu1_trk_dxy_NoVtx);
  tout->Branch("mu1_trk_dxyError_NoVtx", &mu1_trk_dxyError_NoVtx);

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
  tout->Branch("mu2_trk_dxy_NoVtx", &mu2_trk_dxy_NoVtx);
  tout->Branch("mu2_trk_dxyError_NoVtx", &mu2_trk_dxyError_NoVtx);

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
  tout->Branch("mu3_trk_dxy_NoVtx", &mu3_trk_dxy_NoVtx);
  tout->Branch("mu3_trk_dxyError_NoVtx", &mu3_trk_dxyError_NoVtx);

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
  tout->Branch("mu4_trk_dxy_NoVtx", &mu4_trk_dxy_NoVtx);
  tout->Branch("mu4_trk_dxyError_NoVtx", &mu4_trk_dxyError_NoVtx);

  // ===================== Vtx SV =====================
  tout->Branch("SV1_chi2_Vtx", &SV1_chi2_Vtx);
  tout->Branch("SV1_prob_Vtx", &SV1_prob_Vtx);
  tout->Branch("SV1_lxy_Vtx",  &SV1_lxy_Vtx);
  tout->Branch("SV1_global_Vtx",  &SV1_global_Vtx);
  tout->Branch("SV1_px_Vtx", &SV1_px_Vtx);
  tout->Branch("SV1_py_Vtx", &SV1_py_Vtx);
  tout->Branch("SV1_pt_Vtx", &SV1_pt_Vtx);
  tout->Branch("SV1_dphi_Vtx", &SV1_dphi_Vtx);
  tout->Branch("SV1_3Dangle_Vtx", &SV1_3Dangle_Vtx);
  tout->Branch("SV1_L3D_Vtx", &SV1_L3D_Vtx);
  tout->Branch("SV1_xErr_Vtx", &SV1_xErr_Vtx);
  tout->Branch("SV1_yErr_Vtx", &SV1_yErr_Vtx);
  tout->Branch("SV1_zErr_Vtx", &SV1_zErr_Vtx);
  tout->Branch("SV1_mu1_Vtx", &SV1_mu1_Vtx);
  tout->Branch("SV1_mu2_Vtx", &SV1_mu2_Vtx);
  tout->Branch("SV1_ndof_Vtx", &SV1_ndof_Vtx);

  tout->Branch("SV2_chi2_Vtx", &SV2_chi2_Vtx);
  tout->Branch("SV2_prob_Vtx", &SV2_prob_Vtx);
  tout->Branch("SV2_lxy_Vtx",  &SV2_lxy_Vtx);
  tout->Branch("SV2_global_Vtx",  &SV2_global_Vtx);
  tout->Branch("SV2_px_Vtx", &SV2_px_Vtx);
  tout->Branch("SV2_py_Vtx", &SV2_py_Vtx);
  tout->Branch("SV2_pt_Vtx", &SV2_pt_Vtx);
  tout->Branch("SV2_dphi_Vtx", &SV2_dphi_Vtx);
  tout->Branch("SV2_3Dangle_Vtx", &SV2_3Dangle_Vtx);
  tout->Branch("SV2_L3D_Vtx", &SV2_L3D_Vtx);
  tout->Branch("SV2_xErr_Vtx", &SV2_xErr_Vtx);
  tout->Branch("SV2_yErr_Vtx", &SV2_yErr_Vtx);
  tout->Branch("SV2_zErr_Vtx", &SV2_zErr_Vtx);
  tout->Branch("SV2_mu1_Vtx", &SV2_mu1_Vtx);
  tout->Branch("SV2_mu2_Vtx", &SV2_mu2_Vtx);
  tout->Branch("SV2_ndof_Vtx", &SV2_ndof_Vtx);

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
  tout->Branch("mu1_trk_dxy_Vtx", &mu1_trk_dxy_Vtx);
  tout->Branch("mu1_trk_dxyError_Vtx", &mu1_trk_dxyError_Vtx);

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
  tout->Branch("mu2_trk_dxy_Vtx", &mu2_trk_dxy_Vtx);
  tout->Branch("mu2_trk_dxyError_Vtx", &mu2_trk_dxyError_Vtx);

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
  tout->Branch("mu3_trk_dxy_Vtx", &mu3_trk_dxy_Vtx);
  tout->Branch("mu3_trk_dxyError_Vtx", &mu3_trk_dxyError_Vtx);

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
  tout->Branch("mu4_trk_dxy_Vtx", &mu4_trk_dxy_Vtx);
  tout->Branch("mu4_trk_dxyError_Vtx", &mu4_trk_dxyError_Vtx);
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
