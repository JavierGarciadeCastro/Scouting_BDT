import FWCore.ParameterSet.Config as cms

BDT_ntuplizer = cms.EDAnalyzer("BDT_ntuplizer",
    ScoutingmuonsVtx = cms.InputTag("hltScoutingMuonPackerVtx"),
    ScoutingmuonsNoVtx = cms.InputTag("hltScoutingMuonPackerNoVtx"),
    hltScoutingMuonPacker_displacedVtx = cms.InputTag("hltScoutingMuonPackerNoVtx","displacedVtx","HLT")
)

scouting_BDT_ntuplizer = cms.Sequence(BDT_ntuplizer)