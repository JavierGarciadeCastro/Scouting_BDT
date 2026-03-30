import FWCore.ParameterSet.Config as cms

DoubleMuL1 = ["L1_DoubleMu0_Upt8_SQ_er2p0", "L1_DoubleMu0_Upt7_SQ_er2p0", "L1_DoubleMu_15_7", "L1_DoubleMu4p5er2p0_SQ_OS_Mass_Min7", "L1_DoubleMu4p5er2p0_SQ_OS_Mass_7to18", "L1_DoubleMu8_SQ", 
    "L1_DoubleMu4er2p0_SQ_OS_dR_Max1p6", "L1_DoubleMu0er1p4_SQ_OS_dR_Max1p4","L1_DoubleMu4p5_SQ_OS_dR_Max1p2", "L1_DoubleMu0_Upt15_Upt7", "L1_DoubleMu0_Upt6_IP_Min1_Upt4", "L1_DoubleMu0_Upt6_SQ_er2p0"]

SingleMuL1 = ["L1_SingleMu11_SQ14_BMTF","L1_SingleMu10_SQ14_BMTF"]

DoubleMuHLT = ["DST_PFScouting_DoubleMuon_v*"]
SingleMuHLT = ["DST_PFScouting_SingleMuon_v*"]

BDT_ntuplizer = cms.EDAnalyzer("BDT_ntuplizer",
    ScoutingmuonsVtx = cms.InputTag("hltScoutingMuonPackerVtx"),
    ScoutingmuonsNoVtx = cms.InputTag("hltScoutingMuonPackerNoVtx"),
    hltScoutingMuonPacker_displacedVtx = cms.InputTag("hltScoutingMuonPackerNoVtx","displacedVtx","HLT"),
    genParticlesInputTag = cms.InputTag('prunedGenParticles', '', 'PAT'),
    triggerSelection = cms.vstring(SingleMuHLT + DoubleMuHLT),
    triggerConfiguration = cms.PSet(
        hltResults            = cms.InputTag('TriggerResults','','HLT'),
        l1tResults            = cms.InputTag('','',''),
        l1tIgnoreMaskAndPrescale = cms.bool(False),
        throw                 = cms.bool(True),
        usePathStatus = cms.bool(False),
    ),
    AlgInputTag = cms.InputTag("gtStage2Digis"),
    l1tAlgBlkInputTag = cms.InputTag("gtStage2Digis"),
    l1tExtBlkInputTag = cms.InputTag("gtStage2Digis"),
    ReadPrescalesFromFile = cms.bool(False),
    l1Seeds = cms.vstring(DoubleMuL1 + SingleMuL1)
)

scouting_BDT_ntuplizer = cms.Sequence(BDT_ntuplizer)