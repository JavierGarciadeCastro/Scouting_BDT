# Vertexing for Scouting muons in hltpackerVtx collection

This code creates the inputs for a BDT and trains it

## HOW TO RUN:
1. Set up a CMSSW release:
```bash
cmsrel CMSSW_15_1_0
cd CMSSW_15_1_0/src
cmsenv
```
2. Set up the correct directories and clone git repo:
```bash
mkdir run3ScoutingBDT
cd run3ScoutingBDT
git clone https://github.com/JavierGarciadeCastro/Scouting_BDT
cd Scouting_BDT
```
3. Compile the code:
```bash
scram b -j 8
```
4. Create the root files:
Set model to signal and run the ntuplizer, then set to background and run again
```bash
cmsRun test/run_ntuplizer.py
```
5. Train and run the BDT
```bash
python3 BDT_training.py
```