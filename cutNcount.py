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

ctau = 1
model = 'A'
if model == 'A':
    if ctau == 1:
        filename_sig = 'signal1_A_1mm.root'
    elif ctau == 10:
        filename_sig = 'signal1_A_10mm.root'
    elif ctau == 100:
        filename_sig = 'signal1_A_100mm.root'
    
if model == 'B':
    if ctau == 1:
        filename_sig = 'signal_B_1mm.root'
    elif ctau == 10:
        filename_sig = 'signal_B_10mm.root'
    elif ctau == 100:
        filename_sig = 'signal_B_100mm.root'

bkg_files = ["QCD50to80.root", "QCD80to120.root", "QCD120to170.root"]

def apply_cuts(arr):
    # ================= Muon arrays =================
    mu_pt = np.stack([arr[f"mu{i}_pt_Vtx"] for i in range(1,5)], axis=1)
    mu_eta = np.stack([arr[f"mu{i}_eta_Vtx"] for i in range(1,5)], axis=1)
    mu_phi = np.stack([arr[f"mu{i}_phi_Vtx"] for i in range(1,5)], axis=1)
    mu_dxy = np.stack([arr[f"mu{i}_trk_dxy_Vtx"] for i in range(1,5)], axis=1)
    mu_dxyErr = np.stack([arr[f"mu{i}_trk_dxyError_Vtx"] for i in range(1,5)], axis=1)
    mu_chi2Ndof = np.stack([arr[f"mu{i}_chi2Ndof_Vtx"] for i in range(1,5)], axis=1)

    rows = np.arange(mu_pt.shape[0])

    # ================= SV1 muons =================
    idx1 = arr["SV1_mu1_Vtx"]
    idx2 = arr["SV1_mu2_Vtx"]
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
    sv1_xErr = arr["SV1_xErr_Vtx"]
    sv1_yErr = arr["SV1_yErr_Vtx"]
    sv1_zErr = arr["SV1_zErr_Vtx"]
    sv1_dphi = arr["SV1_dphi_Vtx"]
    sv1_3Dangle = arr["SV1_3Dangle_Vtx"]
    sv1_lxy = arr["SV1_lxy_Vtx"]
    sv1_chi2Ndof = arr["SV1_chi2_Vtx"] / arr["SV1_ndof_Vtx"]

    # ================= SV2 variables (if they exist) =================
    idx1_2 = arr["SV2_mu1_Vtx"]
    idx2_2 = arr["SV2_mu2_Vtx"]
    mu1_pt_2  = mu_pt[rows, idx1_2]
    mu2_pt_2  = mu_pt[rows, idx2_2]
    mu1_eta_2 = mu_eta[rows, idx1_2]
    mu2_eta_2 = mu_eta[rows, idx2_2]
    mu1_phi_2 = mu_phi[rows, idx1_2]
    mu2_phi_2 = mu_phi[rows, idx2_2]
    mu1_dxy_2 = mu_dxy[rows, idx1_2]
    mu2_dxy_2 = mu_dxy[rows, idx2_2]
    mu1_dxyErr_2 = mu_dxyErr[rows, idx1_2]
    mu2_dxyErr_2 = mu_dxyErr[rows, idx2_2]
    mu1_chi2Ndof_2 = mu_chi2Ndof[rows, idx1_2]
    mu2_chi2Ndof_2 = mu_chi2Ndof[rows, idx2_2]

    sv2_xErr = arr["SV2_xErr_Vtx"]
    sv2_yErr = arr["SV2_yErr_Vtx"]
    sv2_zErr = arr["SV2_zErr_Vtx"]
    sv2_dphi = arr["SV2_dphi_Vtx"]
    sv2_3Dangle = arr["SV2_3Dangle_Vtx"]
    sv2_lxy = arr["SV2_lxy_Vtx"]
    sv2_chi2Ndof = arr["SV2_chi2_Vtx"] / arr["SV2_ndof_Vtx"]

    # ================= Function to compute SV quality + dimuon cuts =================
    def compute_mask(sv_xErr, sv_yErr, sv_zErr, sv_dphi, sv_3Dangle, sv_lxy, sv_chi2, 
                     mu1_dxy, mu2_dxy, mu1_dxyErr, mu2_dxyErr, mu1_chi2Ndof, mu2_chi2Ndof, 
                     mu1_phi, mu2_phi, mu1_eta, mu2_eta):
        # SV cuts
        sv_mask = ((sv_xErr < 0.05) & (sv_yErr < 0.05) & (sv_zErr < 0.1) & (sv_dphi > 0) & (sv_3Dangle > 0) & (sv_lxy < 70) & (sv_lxy > 0) & (sv_chi2 < 3))

        # Dimuon cuts
        delta_phi = mu1_phi - mu2_phi
        delta_phi = (delta_phi + np.pi) % (2*np.pi) - np.pi
        delta_phi = np.where(np.abs(delta_phi) > 1e-6, delta_phi, 1e-6)
        delta_eta = mu1_eta - mu2_eta
        log_ratio = np.log10(np.abs(delta_eta) / np.abs(delta_phi))
        dxyErr1 = np.where(mu1_dxyErr > 1e-6, mu1_dxyErr, 1e-6)
        dxyErr2 = np.where(mu2_dxyErr > 1e-6, mu2_dxyErr, 1e-6)
        dxy_sig1 = np.abs(mu1_dxy) / dxyErr1
        dxy_sig2 = np.abs(mu2_dxy) / dxyErr2

        dimuon_mask = (
            (dxy_sig1 > 2) & 
            (dxy_sig2 > 2) &
            (mu1_chi2Ndof < 3) & 
            (mu2_chi2Ndof < 3) & 
            (delta_phi < 2.8) & 
            (log_ratio < 1.25)
        )

        return sv_mask & dimuon_mask

    # ================= Masks =================
    mask1 = compute_mask(sv1_xErr, sv1_yErr, sv1_zErr, sv1_dphi, sv1_3Dangle, sv1_lxy, sv1_chi2Ndof,
                         mu1_dxy, mu2_dxy, mu1_dxyErr, mu2_dxyErr, mu1_chi2Ndof, mu2_chi2Ndof,
                         mu1_phi, mu2_phi, mu1_eta, mu2_eta)

    mask2 = compute_mask(sv2_xErr, sv2_yErr, sv2_zErr, sv2_dphi, sv2_3Dangle, sv2_lxy, sv2_chi2Ndof,
                        mu1_dxy_2, mu2_dxy_2, mu1_dxyErr_2, mu2_dxyErr_2, mu1_chi2Ndof_2, mu2_chi2Ndof_2,
                        mu1_phi_2, mu2_phi_2, mu1_eta_2, mu2_eta_2)

    # ================= Final selection =================
    final_mask = mask1 | mask2

    arr_selected = {k: v[final_mask] for k, v in arr.items()}
    return arr_selected

def build_numpy_arrays(filename, collection, label):
    file = uproot.open(root_output / filename)
    tree = file["tout"]

    def max_or_default(array, default=0):
        return ak.to_numpy(ak.fill_none(ak.max(array, axis=1), default))

    branches = tree.keys()
    arr = {}

    if collection == 'Vtx':
        prefix = "_Vtx"
    elif collection == 'NoVtx':
        prefix = "_NoVtx"


    sv_vars = ["chi2", "prob", "lxy", "global", "dphi", "pt", "3Dangle", "L3D", "xErr", "yErr", "zErr", "mu1", "mu2", "ndof"]
    mu_vars = ["pt", "eta", "phi", "isGlobal", "isTracker", "chi2Ndof", "trk_dxy", "trk_dxyError"]

    for sv in [1, 2]:
        for var in sv_vars:
            name = f"SV{sv}_{var}{prefix}"
            if name in branches:
                arr[name] = max_or_default(tree[name].array())
    for mu in [1, 2, 3, 4]:
        for var in mu_vars:
            name = f"mu{mu}_{var}{prefix}"
            if name in branches:
                arr[name] = max_or_default(tree[name].array())

    # ================= Sort SVs by probability =================
    prob1 = arr[f"SV1_prob{prefix}"]
    prob2 = arr[f"SV2_prob{prefix}"]
    swap = prob2 > prob1

    for var in sv_vars:
        sv1 = f"SV1_{var}{prefix}"
        sv2 = f"SV2_{var}{prefix}"
        if sv1 in arr and sv2 in arr:
            a = arr[sv1].copy()
            b = arr[sv2].copy()
            arr[sv1] = np.where(swap, b, a)
            arr[sv2] = np.where(swap, a, b)

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
