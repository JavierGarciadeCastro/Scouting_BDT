import uproot
import matplotlib.pyplot as plt
import awkward as ak
import numpy as np
import mplhep
import re
from collections import Counter
import pandas as pd
import os
from pathlib import Path

root_output = Path("root_output")

ctau = 10
model = 'A'
if model == 'A':
    if ctau == 1:
        filename_sig = 'signal_A_1mm.root'
    elif ctau == 10:
        filename_sig = 'signal_A_10mm.root'
    elif ctau == 100:
        filename_sig = 'signal_A_100mm.root'
    
if model == 'B':
    if ctau == 1:
        filename_sig = 'signal_B_1mm.root'
    elif ctau == 10:
        filename_sig = 'signal_B_10mm.root'
    elif ctau == 100:
        filename_sig = 'signal_B_100mm.root'

bkg_files = ["QCD50to80.root", "QCD80to120.root", "QCD120to170.root"]

def apply_cuts(arr):
    mu_pt = np.stack([arr["mu1_pt_Vtx"],arr["mu2_pt_Vtx"],arr["mu3_pt_Vtx"],arr["mu4_pt_Vtx"],], axis=1)
    mu_eta = np.stack([arr["mu1_eta_Vtx"],arr["mu2_eta_Vtx"],arr["mu3_eta_Vtx"],arr["mu4_eta_Vtx"],], axis=1)
    mu_phi = np.stack([arr["mu1_phi_Vtx"],arr["mu2_phi_Vtx"],arr["mu3_phi_Vtx"],arr["mu4_phi_Vtx"],], axis=1)
    mu_dxy = np.stack([arr["mu1_trk_dxy_Vtx"],arr["mu2_trk_dxy_Vtx"],arr["mu3_trk_dxy_Vtx"],arr["mu4_trk_dxy_Vtx"],], axis=1)
    mu_dxyErr = np.stack([arr["mu1_trk_dxyError_Vtx"],arr["mu2_trk_dxyError_Vtx"],arr["mu3_trk_dxyError_Vtx"],arr["mu4_trk_dxyError_Vtx"],], axis=1)
    mu_chi2Ndof = np.stack([arr["mu1_chi2Ndof_Vtx"],arr["mu2_chi2Ndof_Vtx"],arr["mu3_chi2Ndof_Vtx"],arr["mu4_chi2Ndof_Vtx"],], axis=1)

    idx1 = arr["SV1_mu1_Vtx"] - 1
    idx2 = arr["SV1_mu2_Vtx"] - 1

    rows = np.arange(mu_pt.shape[0])

    mu1_pt  = mu_pt[rows, idx1]
    mu2_pt  = mu_pt[rows, idx2]
    
    mu1_eta = mu_eta[rows, idx1]
    mu2_eta = mu_eta[rows, idx2]
    
    mu1_phi = mu_phi[rows, idx1]
    mu2_phi = mu_phi[rows, idx2]
    
    mu1_dxy = mu_dxy[rows, idx1]
    mu2_dxy = mu_dxy[rows, idx2]

    mu1_dxyErr = mu_dxyErr[rows, idx1]
    mu2_dxyErr = mu_dxyErr[rows, idx2]

    mu1_chi2Ndof = mu_chi2Ndof[rows, idx1]
    mu2_chi2Ndof = mu_chi2Ndof[rows, idx2]

    delta_eta = mu1_eta - mu2_eta
    delta_phi = mu1_phi - mu2_phi
    delta_phi = (delta_phi + np.pi) % (2*np.pi) - np.pi
    delta_phi = np.where(np.abs(delta_phi) > 1e-6, delta_phi, 1e-6)
    dxyErr1 = np.where(mu1_dxyErr > 1e-6, mu1_dxyErr, 1e-6)
    dxyErr2 = np.where(mu2_dxyErr > 1e-6, mu2_dxyErr, 1e-6)

    log_ratio = np.log10(np.abs(delta_eta) / np.abs(delta_phi))
    dxy_sig1 = mu1_dxy / dxyErr1
    dxy_sig2 = mu2_dxy / dxyErr2
    sv_chi2Ndof = arr["SV1_chi2_Vtx"] / arr["SV1_ndof_Vtx"]


    mask = (
        (arr["SV1_xErr_Vtx"] < 0.05) &
        (arr["SV1_yErr_Vtx"] < 0.05) &
        (arr["SV1_zErr_Vtx"] < 0.1) &
        (arr["SV1_dphi_Vtx"] > 0) &
        (arr["SV1_3Dangle_Vtx"] > 0)&
        (arr["SV1_lxy_Vtx"] < 70)&
        (sv_chi2Ndof < 3) &
        (delta_phi < 2.8) &
        (dxy_sig1 > 2) &
        (dxy_sig2 > 2) &
        (mu1_chi2Ndof < 3) &
        (mu2_chi2Ndof < 3) &
        (log_ratio < 1.25)
    )

    arr_selected = {k: v[mask] for k, v in arr.items()}

    return arr_selected

def build_numpy_arrays(filename, collection, label):
    file = uproot.open(root_output / filename)
    tree = file["tout"]

    def max_or_default(array, default=0):
        return np.array([ak.max(a) if len(a) > 0 else default for a in array])

    branches = tree.keys()
    arr = {}

    if collection == 'Vtx':
        prefix = "_Vtx"
    elif collection == 'NoVtx':
        prefix = "_NoVtx"
    else:
        raise ValueError("collection must be 'Vtx' or 'NoVtx'")

    for sv in [1, 2]:
        for var in ["chi2", "prob", "lxy", "global", "dphi", "pt", "3Dangle", "L3D",
                    "xErr", "yErr", "zErr", "mu1", "mu2", "ndof"]:
            name = f"SV{sv}_{var}{prefix}"
            if name in branches:
                arr[name] = max_or_default(tree[name].array())
    for mu in [1, 2, 3, 4]:
        for var in ["pt", "eta", "phi", "isGlobal", "isTracker", "chi2Ndof",
                    "trk_dxy", "trk_dxyError"]:
            name = f"mu{mu}_{var}{prefix}"
            if name in branches:
                arr[name] = max_or_default(tree[name].array())

    arr["label"] = np.full_like(arr[list(arr.keys())[0]], label)
    return arr

sig_arrays = build_numpy_arrays(filename_sig, "Vtx", label=1)
bkg_arrays_list = [build_numpy_arrays(f, "Vtx", label=0) for f in bkg_files]
bkg_arrays = {k: np.concatenate([arr[k] for arr in bkg_arrays_list]) for k in bkg_arrays_list[0].keys()}

all_events = {k: np.concatenate([sig_arrays[k], bkg_arrays[k]]) for k in sig_arrays.keys()}
lxy_bins = [0.0, 0.2, 1.0, 2.4, 3.1, 7.0, 11.0, 16.0, 70.0]
lxy_labels = ["0p0to0p2", "0p2to1p0", "1p0to2p4", "2p4to3p1", "3p1to7p0", "7p0to11p0", "11p0to16p0", "16p0to70p0"]

lxy = all_events["SV1_lxy_Vtx"]
labels = all_events["label"]

results = []

for i in range(len(lxy_bins) - 1):

    low  = lxy_bins[i]
    high = lxy_bins[i+1]
    lbl  = lxy_labels[i]

    bin_mask = (lxy >= low) & (lxy < high)
    arr_bin = {k: v[bin_mask] for k, v in all_events.items()}
    arr_pass = apply_cuts(arr_bin)

    sig_total = np.sum(arr_bin["label"] == 1)
    bkg_total = np.sum(arr_bin["label"] == 0)
    sig_pass = np.sum(arr_pass["label"] == 1)
    bkg_pass = np.sum(arr_pass["label"] == 0)

    sig_eff = sig_pass / sig_total if sig_total > 0 else np.nan
    bkg_rej = 1 - (bkg_pass / bkg_total) if bkg_total > 0 else np.nan

    results.append({
        "lxy_bin": lbl,
        "sig_total": sig_total,
        "sig_pass": sig_pass,
        "sig_eff": sig_eff,
        "bkg_total": bkg_total,
        "bkg_pass": bkg_pass,
        "bkg_rej": bkg_rej
    })

for r in results:
    print(
        f"{r['lxy_bin']:>12} | "
        f"Sig: {r['sig_pass']}/{r['sig_total']}  "
        f"(eff={r['sig_eff']:.3f}) | "
        f"Bkg: {r['bkg_pass']}/{r['bkg_total']}  "
        f"(rej={r['bkg_rej']:.3f})"
    )
