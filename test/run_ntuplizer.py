import FWCore.ParameterSet.Config as cms
from TrackingTools.TransientTrack.TransientTrackBuilder_cfi import *

process = cms.Process("DarkShowerAnalysis")
from Configuration.AlCa.GlobalTag import GlobalTag
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load("run3ScoutingBDT.Scouting_BDT.BDT_ntuplizer_cfi")

process.load("TrackingTools/TransientTrack/TransientTrackBuilder_cfi")
process.load("Configuration.Geometry.GeometryRecoDB_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.GlobalTag.globaltag = '150X_mcRun3_2024_realistic_v2'


process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(1000))

#model = 'signal'
model = 'background'
if model == 'background':
  process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAODv6/QCD_Bin-PT-50to80_Fil-MuEnriched_TuneCP5_13p6TeV_pythia8/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/130000/00045f22-18e3-4cb0-95c5-c8684856f79b.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAODv6/QCD_Bin-PT-50to80_Fil-MuEnriched_TuneCP5_13p6TeV_pythia8/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/130000/02cf48fd-12ca-4354-aed2-0358860ddc18.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAODv6/QCD_Bin-PT-50to80_Fil-MuEnriched_TuneCP5_13p6TeV_pythia8/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/130000/056b89ff-2416-4495-a9ba-32eeab4afce3.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAODv6/QCD_Bin-PT-50to80_Fil-MuEnriched_TuneCP5_13p6TeV_pythia8/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/130000/05de9cce-ebd6-4583-b932-0e0b41189e18.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAODv6/QCD_Bin-PT-50to80_Fil-MuEnriched_TuneCP5_13p6TeV_pythia8/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/130000/05f13799-1622-4a36-8af8-8861f0f24683.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAODv6/QCD_Bin-PT-50to80_Fil-MuEnriched_TuneCP5_13p6TeV_pythia8/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/130000/0690a2b7-92a6-4819-8bc8-5d8f743db445.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAODv6/QCD_Bin-PT-50to80_Fil-MuEnriched_TuneCP5_13p6TeV_pythia8/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/130000/085b6e1a-937b-4c2e-a028-b110330a5b69.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAODv6/QCD_Bin-PT-50to80_Fil-MuEnriched_TuneCP5_13p6TeV_pythia8/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/130000/08c28959-cf78-4e3d-979a-d9e4dc4b8c34.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAODv6/QCD_Bin-PT-50to80_Fil-MuEnriched_TuneCP5_13p6TeV_pythia8/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/130000/08d0e093-09ee-4a50-a17b-e85d0333fa38.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAODv6/QCD_Bin-PT-50to80_Fil-MuEnriched_TuneCP5_13p6TeV_pythia8/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/130000/0a7a434b-a389-4483-8784-fc536d943996.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAODv6/QCD_Bin-PT-50to80_Fil-MuEnriched_TuneCP5_13p6TeV_pythia8/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/130000/0d288603-a295-49c6-a18d-21f9d92abc20.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAODv6/QCD_Bin-PT-50to80_Fil-MuEnriched_TuneCP5_13p6TeV_pythia8/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/130000/0d34b5ac-5a5e-4f7c-90db-67de171de3cd.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAODv6/QCD_Bin-PT-50to80_Fil-MuEnriched_TuneCP5_13p6TeV_pythia8/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/130000/0e2332fb-fad6-4077-9724-ce0f8a4ee0eb.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAODv6/QCD_Bin-PT-50to80_Fil-MuEnriched_TuneCP5_13p6TeV_pythia8/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/130000/0efff2e7-e216-4966-917b-3cdbe08c7462.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAODv6/QCD_Bin-PT-50to80_Fil-MuEnriched_TuneCP5_13p6TeV_pythia8/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/130000/0f12a6c1-e232-4601-b0cb-a00f2dd938fe.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAODv6/QCD_Bin-PT-50to80_Fil-MuEnriched_TuneCP5_13p6TeV_pythia8/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/130000/0fdc4cf6-90fa-40db-bb2b-8e8d1186c199.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAODv6/QCD_Bin-PT-50to80_Fil-MuEnriched_TuneCP5_13p6TeV_pythia8/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/130000/10557994-b2a1-4120-9142-68490abf9d5f.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAODv6/QCD_Bin-PT-50to80_Fil-MuEnriched_TuneCP5_13p6TeV_pythia8/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/130000/10bd8831-fa10-49c1-9d36-095ec9a8a286.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAODv6/QCD_Bin-PT-50to80_Fil-MuEnriched_TuneCP5_13p6TeV_pythia8/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/130000/10f7048d-07f1-4334-ab53-9e3ff6db3625.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAODv6/QCD_Bin-PT-50to80_Fil-MuEnriched_TuneCP5_13p6TeV_pythia8/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/130000/112e1d90-da81-4882-9224-5c507a7f7ae9.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAODv6/QCD_Bin-PT-50to80_Fil-MuEnriched_TuneCP5_13p6TeV_pythia8/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/130000/11efc0c4-809c-473c-b404-1ac15400ea6f.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAODv6/QCD_Bin-PT-50to80_Fil-MuEnriched_TuneCP5_13p6TeV_pythia8/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/130000/126acf5d-6310-43d2-ac89-e88240dbe34c.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAODv6/QCD_Bin-PT-50to80_Fil-MuEnriched_TuneCP5_13p6TeV_pythia8/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/130000/127ea555-ab98-41d9-91ed-2b4fdbae3575.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAODv6/QCD_Bin-PT-50to80_Fil-MuEnriched_TuneCP5_13p6TeV_pythia8/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/130000/12de9ac9-c0c9-4396-8f1a-84c53f32ea05.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAODv6/QCD_Bin-PT-50to80_Fil-MuEnriched_TuneCP5_13p6TeV_pythia8/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/130000/1301c7c0-857a-4f86-8a7b-473829fc48b2.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAODv6/QCD_Bin-PT-50to80_Fil-MuEnriched_TuneCP5_13p6TeV_pythia8/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/130000/1307a393-ff75-4dbb-a743-ffa7772e5052.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAODv6/QCD_Bin-PT-50to80_Fil-MuEnriched_TuneCP5_13p6TeV_pythia8/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/130000/1379dcb1-4b09-4654-9304-abff9cbb5567.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAODv6/QCD_Bin-PT-50to80_Fil-MuEnriched_TuneCP5_13p6TeV_pythia8/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/130000/1453dde1-44a3-464b-a655-ffe7f910db94.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAODv6/QCD_Bin-PT-50to80_Fil-MuEnriched_TuneCP5_13p6TeV_pythia8/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/130000/14fb124a-0a82-4817-98fc-ba1bc9ca3711.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAODv6/QCD_Bin-PT-50to80_Fil-MuEnriched_TuneCP5_13p6TeV_pythia8/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/130000/159a8ade-a9b7-4f60-9a36-0912a39598f2.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAODv6/QCD_Bin-PT-50to80_Fil-MuEnriched_TuneCP5_13p6TeV_pythia8/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/130000/166d1fb5-9ac4-47d4-a0bb-e22c7430e8bd.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAODv6/QCD_Bin-PT-50to80_Fil-MuEnriched_TuneCP5_13p6TeV_pythia8/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/130000/16e01a0a-b5e4-400a-be4a-da8e287ddfbe.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAODv6/QCD_Bin-PT-50to80_Fil-MuEnriched_TuneCP5_13p6TeV_pythia8/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/130000/179b1471-a95e-49ec-9118-5cdb2b692642.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAODv6/QCD_Bin-PT-50to80_Fil-MuEnriched_TuneCP5_13p6TeV_pythia8/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/130000/17dbc9e9-808d-48c8-8ac4-14fbc3a38ea3.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAODv6/QCD_Bin-PT-50to80_Fil-MuEnriched_TuneCP5_13p6TeV_pythia8/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/130000/1859b1f2-f13f-4efa-b84d-d38e235cc3a7.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAODv6/QCD_Bin-PT-50to80_Fil-MuEnriched_TuneCP5_13p6TeV_pythia8/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/130000/18f153a3-d2f6-48b3-851b-878a6bfbfe23.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAODv6/QCD_Bin-PT-50to80_Fil-MuEnriched_TuneCP5_13p6TeV_pythia8/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/130000/19425b55-eba3-4447-bbd6-26e393f41021.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAODv6/QCD_Bin-PT-50to80_Fil-MuEnriched_TuneCP5_13p6TeV_pythia8/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/130000/1a108e6c-cbbf-4f00-ac91-2cb6f636441a.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAODv6/QCD_Bin-PT-50to80_Fil-MuEnriched_TuneCP5_13p6TeV_pythia8/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/130000/1af20e37-62f6-4078-a6de-cff9e3482b8e.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAODv6/QCD_Bin-PT-50to80_Fil-MuEnriched_TuneCP5_13p6TeV_pythia8/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/130000/1b4c5b3d-62d7-4ba8-9dd7-b35af0f7ef47.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAODv6/QCD_Bin-PT-50to80_Fil-MuEnriched_TuneCP5_13p6TeV_pythia8/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/130000/1b538164-cc6a-444d-8c55-06ab176a066f.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAODv6/QCD_Bin-PT-50to80_Fil-MuEnriched_TuneCP5_13p6TeV_pythia8/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/130000/1bb6538b-3c96-4078-8061-cfb1bed20a58.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAODv6/QCD_Bin-PT-50to80_Fil-MuEnriched_TuneCP5_13p6TeV_pythia8/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/130000/1bf8b55c-401c-4394-9e42-2ae6a48d9986.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAODv6/QCD_Bin-PT-50to80_Fil-MuEnriched_TuneCP5_13p6TeV_pythia8/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/130000/1c30740e-f5c9-42a8-8dd9-0ac1cdd50cc9.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAODv6/QCD_Bin-PT-50to80_Fil-MuEnriched_TuneCP5_13p6TeV_pythia8/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/130000/1cbb3c41-fb46-47e9-bd1e-760eb5ced7e6.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAODv6/QCD_Bin-PT-50to80_Fil-MuEnriched_TuneCP5_13p6TeV_pythia8/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/130000/1d6bb29f-9144-4903-8c1a-7f93cda3245b.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAODv6/QCD_Bin-PT-50to80_Fil-MuEnriched_TuneCP5_13p6TeV_pythia8/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/130000/1d78c687-2057-4bc0-84bc-55e28f60b167.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAODv6/QCD_Bin-PT-50to80_Fil-MuEnriched_TuneCP5_13p6TeV_pythia8/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/130000/1e5f972e-f917-4ba7-8aa5-f655aa0cc7bf.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAODv6/QCD_Bin-PT-50to80_Fil-MuEnriched_TuneCP5_13p6TeV_pythia8/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/130000/1e90522f-fe8b-436a-9b36-c78d3a90f623.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAODv6/QCD_Bin-PT-50to80_Fil-MuEnriched_TuneCP5_13p6TeV_pythia8/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/130000/1f82b85c-68e9-4fb3-bd9b-fe637d2b1fc5.root'

    ),
    duplicateCheckMode = cms.untracked.string("noDuplicateCheck")
  )

if model == 'signal':
  process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-1p0-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/140000/ad3a1bee-13b6-4d0c-90da-7ca085c674e6.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-1p0-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/140000/06ce5622-abe5-41a3-9952-4c8f6a4a2731.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-1p0-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/140000/26105aa6-a22d-4a70-a898-79c44fa762f6.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-1p0-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/140000/c3ed856e-d041-4f5c-b47b-ab6b17503c4b.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-1p0-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/140000/e81c0205-61a2-4fd9-8e60-b620cf7023eb.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-1p0-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/140000/74d301f7-a9cb-4e05-b256-c6e721b85211.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-1p0-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/140000/09e3b4d8-54a9-4f3e-b01a-91bfce11cadc.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-1p0-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/140000/53d14b8c-7d0d-4b1d-afbd-07f9f7d69245.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-1p0-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/140000/515b2e2c-5d9f-4e79-a815-ec5779819aac.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-1p0-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/140000/b605e42c-d918-4126-adf3-d9697cb3ed7d.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-1p0-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/140000/8b5433d7-0f29-4e0a-a846-b225c7e9b29e.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-1p0-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/140000/053bfdc7-b645-4432-9343-52f2f268ca53.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-1p0-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/140000/df49e047-2436-4d97-aa8d-5f9aaee2f1db.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-1p0-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/140000/9d4efa86-81eb-4179-9487-4aea8b53a596.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-1p0-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/140000/a958aecb-27db-4ac2-94e5-1983d9f5f00f.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-1p0-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/140000/deec9328-96eb-4cc6-9f8d-d8ad42331604.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-1p0-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/140000/21589db6-b2d0-4f0c-9709-d4bef0f6ec52.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-1p0-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/140000/da6006a5-6dab-4279-9928-fd17b0e05202.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-1p0-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/140000/96e45dd9-cb5e-4efd-8b50-e36e7a91b873.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-1p0-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/130000/7c105ccb-84f0-4ffb-90a9-467300c7fb74.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-1p0-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/130000/0509ec06-308d-4732-9717-ab2284edc5e4.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-1p0-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/130000/afaee59f-5c36-4dff-bcd2-190a2c7f2f3d.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-1p0-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/130000/9a199576-bc47-4dfd-83d6-d1d090cec064.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-1p0-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/130000/9fba4a4f-7a59-42ea-8677-ae8488517409.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-1p0-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/130000/70b1432c-eb95-4319-8ee2-95988e7725d0.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-1p0-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/130000/bbc7f837-a5e6-4991-bfb0-93ba26fee7e4.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-1p0-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/130000/3c567b8d-fbac-4ed4-ab31-b1820e25c8b2.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-1p0-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/130000/df2d8780-11f4-46ae-b97a-9cad2bd3a931.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-1p0-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/130000/b47b52c3-bf5e-4a31-9539-e4992e87c7f5.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-1p0-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/130000/9f575cc5-7a83-4803-a534-3931913f515b.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-1p0-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/130000/0d9f9b4f-be49-40a2-ad7d-213c3323bc22.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-1p0-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/130000/ab51abb5-07a8-4a48-a81b-709a9aac551b.root'
    ),
    duplicateCheckMode = cms.untracked.string("noDuplicateCheck")
  )
'''
if lifetime == 10:
  process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-10-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2560000/0cffd46a-92f5-4401-94d6-6ab55b6fd824.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-10-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2560000/4ef75fa6-c4d5-455b-871f-d2bd5a690dbc.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-10-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2560000/7bd6635a-8489-4e17-b161-fd83a7866aa2.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-10-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2560000/fddfed3a-699f-42b9-a94d-e6046af395ff.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-10-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2560000/c84603e5-2b4b-4420-be0f-569367249042.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-10-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2560000/917795b6-2b24-42f0-846f-3a351d38e829.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-10-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2560000/d5d54f4b-5e27-4a29-8a03-7788d34a82a6.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-10-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2560000/d810ea01-2eeb-457c-85a2-bd3825da3262.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-10-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2560000/a29640bc-0968-4de7-9f17-ebeaae609fdb.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-10-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2560000/2762f2d9-df40-4efd-b579-b1aa9a2bd3b1.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-10-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2560000/5d3adddf-ba37-4bcf-9b65-1f2cfd058a4b.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-10-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2560000/b04b18ee-e886-440e-9ff3-e83341ed5609.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-10-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2560000/8293333b-d884-4914-a283-2ce3c10fb2b7.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-10-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2560000/165f7d54-5257-4020-aaa1-4379ffc25a28.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-10-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2560000/b8ee9a61-84a5-48cd-8f1e-4b7704f8b13f.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-10-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2560000/b5355353-2d48-434c-b81b-b166791a398d.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-10-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2560000/e2ff5dc5-556c-4f98-ba84-5ace903cdddb.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-10-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2560000/61bf9d89-b72f-4848-bcb9-37d0adf5e456.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-10-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2560000/7db007ba-8151-4447-bb41-07b699264d9d.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-10-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2560000/bb1afab6-ae09-4131-82a3-2ff00bab710f.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-10-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2560000/6e56dd7d-a0ae-499a-84b9-5a302e28d60e.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-10-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2560000/a015b7db-9f84-409c-992d-368684a0fd59.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-10-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/130000/8eafb1f3-8eda-47bd-86b8-214a14372649.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-10-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/130000/03d76157-071a-4b90-91bf-0f8eed2325d1.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-10-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/130000/695d4c10-07c9-42fc-9e1f-b22e530617d9.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-10-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/130000/ef48bdb1-0559-45c2-8563-9967e6d90e67.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-10-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/130000/48a74bf5-3b13-4af4-8e9c-58e6d8ef09c2.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-10-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/130000/b82f9ac3-9996-4b42-a66b-025c71332dc1.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-10-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/130000/9d9085b2-8677-444f-80f7-30cf587a5c82.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-10-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/130000/6d859627-b7b5-4185-86c3-039d1d91e2e7.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-10-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/130000/80a61881-90d8-4566-b470-4f2480e64689.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-10-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/130000/bcc9d7aa-84bf-49d7-9e59-d40aecc7e406.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-10-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/130000/49b6280f-755f-4b15-8f6c-baf99683f04a.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-10-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/130000/f365ef92-757f-4ec9-acd7-12441bb107d5.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-10-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/130000/6fcab8e9-e4c5-46dd-a9b8-fbcb67e93974.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-10-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/130000/e5b3a9c7-c9a5-4227-a453-b15f045c12db.root'
    ),
    duplicateCheckMode = cms.untracked.string("noDuplicateCheck")
  )

if lifetime == 100:
  process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-100-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/120000/106c0880-cfb4-4979-a1f0-453539be63b8.root',
      #'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-100-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2560000/34e17105-0813-4819-8aa6-fef5d35f3016.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-100-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2560000/7e97a4bb-ce3f-43e9-8092-6362cfa9bdc8.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-100-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2560000/947bc259-d24a-40f1-9d72-f52fb83ddcc2.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-100-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2560000/1e711024-0524-4dd6-870b-0f99992e033e.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-100-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2560000/30488219-7075-4db4-9bcb-e9cf1a74b11b.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-100-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2560000/765876b9-b9bf-4b14-a3d0-748c8407732f.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-100-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2560000/dac454a9-db9f-4d87-be93-70a94a968e17.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-100-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2560000/e02ada9b-46f8-4285-9725-8062ec1836ac.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-100-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2560000/80242a6b-fa36-40c2-b1ed-5fbb5a8e72cb.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-100-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2560000/6ec7e8e1-7bdd-4a18-b762-21ced85689fd.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-100-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2560000/203e64db-a3d0-465c-9c7c-7e3c56587077.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-100-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2560000/12cd1210-8266-4fb8-aa31-47fb2dfa59e7.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-100-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2560000/3a5ecddd-def9-4e59-ac56-b4574412c2f6.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-100-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2560000/5dd2e6db-3d1f-4ad3-994b-4ec874b16d8f.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-100-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2560000/825618c3-aaa3-4a93-a234-bc2b874532de.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-100-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2560000/869df3da-d674-456c-85a4-e401a32865b1.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-100-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2560000/d1d58977-5cdf-47ee-a3af-b63871b3143a.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-100-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2560000/efb35252-904e-40c4-aebf-653ab825649d.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-100-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2560000/12160267-bcc7-42af-b8ac-7741214777bb.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-100-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2560000/03c5d627-1f78-41f6-b285-1a3b28e08f7b.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-100-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2560000/cc52a4c3-b34c-491a-bb08-6401bce013b9.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-100-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/120000/416da713-7d7d-4251-a585-eca9b6cac66d.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-100-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/120000/4ad254b6-7108-40d3-a939-02b18f8b79cf.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-100-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/120000/ebbea963-ffb3-46cb-a554-dceb32d2e4c8.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-100-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/120000/03f68049-d4a1-440c-84cf-42ccca437982.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-100-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/120000/c30491d0-2292-410d-988e-cad3bafe4378.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-100-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/120000/40d28ad6-f56d-4e4e-8be5-41fe8f162cd0.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-100-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/120000/f969d6ae-8238-425e-8b23-f62963561247.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-100-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/120000/868615c5-85d2-429f-8e31-6713c113b3a3.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-100-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/120000/0a505f32-b016-4bd2-a8af-4532da6108f4.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-100-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/120000/a245681f-3943-477e-830e-0d4babe4172e.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-100-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/120000/c191e1f3-7fe6-46c9-831d-9db04c33ebe7.root',
      'root://cms-xrd-global.cern.ch//store/mc/RunIII2024Summer24MiniAOD/GluGluHToDarkShowers-ScenarioA_Par-ctau-100-mA-2p00-mpi-10_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/120000/c1932480-1632-46d2-ad1a-3ee417c486ee.root'
    ),
    duplicateCheckMode = cms.untracked.string("noDuplicateCheck")
  )
'''

process.p = cms.Path(process.scouting_BDT_ntuplizer)
