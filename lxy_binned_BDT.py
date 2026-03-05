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

from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import roc_auc_score, accuracy_score, roc_curve

root_output = Path("root_output")

ctau = 100
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

QCD_50to80 = 'QCD50to80.root'
QCD_80to120 = 'QCD80to120.root'
QCD_120to170 = 'QCD120to170.root'

def plot_variable(var, ctau):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)

    # ===== Vtx =====
    var_Vtx = f"{var}_Vtx"

    if "pt" in var:
        xmin = 0
        xmax = 50
    elif "lxy" in var:
        xmin = 0
        xmax = 70
    elif "dphi" in var:
        xmin = -1
        xmax = 1
    elif "trackIso" in var:
        xmin = 0
        xmax = 10
    bins = np.linspace(xmin, xmax, 51)
    axes[0].hist(df_sig_Vtx[var_Vtx], bins=bins, histtype="step", label=f"Signal, ctau = {ctau}mm", linewidth=2)
    axes[0].hist(df_bkg_Vtx[var_Vtx], bins=bins, histtype="step", label="QCD", linewidth=2)
    axes[0].set_title(f"{var} (Vtx)")
    axes[0].set_xlabel(var)
    axes[0].set_ylabel("Entries")
    axes[0].set_xlim(xmin, xmax)
    hist_sig_Vtx, _ = np.histogram(df_sig_Vtx[var_Vtx].dropna(), bins=bins)
    hist_bkg_Vtx, _ = np.histogram(df_bkg_Vtx[var_Vtx].dropna(), bins=bins)
    ymax_Vtx = 1.2 * max(hist_sig_Vtx.max(), hist_bkg_Vtx.max())
    axes[0].set_ylim(0, ymax_Vtx)
    axes[0].legend()
    axes[0].set_yscale("log")


    # ===== NoVtx =====
    var_NoVtx = f"{var}_NoVtx"
    axes[1].hist(df_sig_NoVtx[var_NoVtx], bins=bins, histtype="step", label=f"Signal, ctau = {ctau}mm", linewidth=2)
    axes[1].hist(df_bkg_NoVtx[var_NoVtx], bins=bins, histtype="step", label="Background", linewidth=2)
    axes[1].set_title(f"{var} (NoVtx)")
    axes[1].set_xlabel(var)
    axes[1].set_xlim(xmin, xmax)
    hist_sig_NoVtx, _ = np.histogram(df_sig_NoVtx[var_NoVtx].dropna(), bins=bins)
    hist_bkg_NoVtx, _ = np.histogram(df_bkg_NoVtx[var_NoVtx].dropna(), bins=bins)
    ymax_NoVtx = 1.2 * max(hist_sig_NoVtx.max(), hist_bkg_NoVtx.max())
    axes[1].set_ylim(0, ymax_NoVtx)
    axes[1].legend()
    axes[1].set_yscale("log")

    plt.tight_layout()
    plt.savefig(f"curves_comp_{model}/{var}_ctau_{ctau}mm.png")

def build_dataframe(filename, label, collection):

    file = uproot.open(root_output / filename)
    tree = file["tout"]

    def max_or_default(array, default=0):
        return np.array([ak.max(a) if len(a) > 0 else default for a in array])

    if collection == 'Vtx':
        df_Vtx = pd.DataFrame({
            # ================= Vtx =================
            "SV1_chi2_Vtx": max_or_default(tree["SV1_chi2_Vtx"].array()),
            "SV1_prob_Vtx": max_or_default(tree["SV1_prob_Vtx"].array()),
            "SV1_lxy_Vtx":  max_or_default(tree["SV1_lxy_Vtx"].array()),
            "SV1_global_Vtx":  max_or_default(tree["SV1_global_Vtx"].array()),
            "SV1_dphi_Vtx":  max_or_default(tree["SV1_dphi_Vtx"].array()),
            "SV1_pt_Vtx":  max_or_default(tree["SV1_pt_Vtx"].array()),
            "SV1_3Dangle_Vtx":  max_or_default(tree["SV1_3Dangle_Vtx"].array()),
            "SV1_L3D_Vtx":  max_or_default(tree["SV1_L3D_Vtx"].array()),
            "SV1_xErr_Vtx":  max_or_default(tree["SV1_xErr_Vtx"].array()),
            "SV1_yErr_Vtx":  max_or_default(tree["SV1_yErr_Vtx"].array()),
            "SV1_zErr_Vtx":  max_or_default(tree["SV1_zErr_Vtx"].array()),
            "SV1_mu1_Vtx":  max_or_default(tree["SV1_mu1_Vtx"].array()),
            "SV1_mu2_Vtx":  max_or_default(tree["SV1_mu2_Vtx"].array()),
            "SV1_ndof_Vtx":  max_or_default(tree["SV1_ndof_Vtx"].array()),
            
            "SV2_chi2_Vtx": max_or_default(tree["SV2_chi2_Vtx"].array()),
            "SV2_prob_Vtx": max_or_default(tree["SV2_prob_Vtx"].array()),
            "SV2_lxy_Vtx":  max_or_default(tree["SV2_lxy_Vtx"].array()),
            "SV2_global_Vtx":  max_or_default(tree["SV2_global_Vtx"].array()),
            "SV2_dphi_Vtx":  max_or_default(tree["SV2_dphi_Vtx"].array()),
            "SV2_pt_Vtx":  max_or_default(tree["SV2_pt_Vtx"].array()),
            "SV2_3Dangle_Vtx":  max_or_default(tree["SV2_3Dangle_Vtx"].array()),
            "SV2_L3D_Vtx":  max_or_default(tree["SV2_L3D_Vtx"].array()),
            "SV2_xErr_Vtx":  max_or_default(tree["SV2_xErr_Vtx"].array()),
            "SV2_yErr_Vtx":  max_or_default(tree["SV2_yErr_Vtx"].array()),
            "SV2_zErr_Vtx":  max_or_default(tree["SV2_zErr_Vtx"].array()),
            "SV2_mu1_Vtx":  max_or_default(tree["SV2_mu1_Vtx"].array()),
            "SV2_mu2_Vtx":  max_or_default(tree["SV2_mu2_Vtx"].array()),
            "SV2_ndof_Vtx":  max_or_default(tree["SV2_ndof_Vtx"].array()),

            "mu1_pt_Vtx": max_or_default(tree["mu1_pt_Vtx"].array()),
            "mu1_eta_Vtx": max_or_default(tree["mu1_eta_Vtx"].array()),
            "mu1_phi_Vtx": max_or_default(tree["mu1_phi_Vtx"].array()),
            "mu1_isGlobal_Vtx": max_or_default(tree["mu1_isGlobal_Vtx"].array()),
            "mu1_isTracker_Vtx": max_or_default(tree["mu1_isTracker_Vtx"].array()),
            "mu1_chi2Ndof_Vtx": max_or_default(tree["mu1_chi2Ndof_Vtx"].array()),
            "mu1_trk_dxy_Vtx": max_or_default(tree["mu1_trk_dxy_Vtx"].array()),
            "mu1_trk_dxyError_Vtx": max_or_default(tree["mu1_trk_dxyError_Vtx"].array()),
            "mu2_pt_Vtx": max_or_default(tree["mu2_pt_Vtx"].array()),
            "mu2_eta_Vtx": max_or_default(tree["mu2_eta_Vtx"].array()),
            "mu2_phi_Vtx": max_or_default(tree["mu2_phi_Vtx"].array()),
            "mu2_isGlobal_Vtx": max_or_default(tree["mu2_isGlobal_Vtx"].array()),
            "mu2_isTracker_Vtx": max_or_default(tree["mu2_isTracker_Vtx"].array()),
            "mu2_chi2Ndof_Vtx": max_or_default(tree["mu2_chi2Ndof_Vtx"].array()),
            "mu2_trk_dxy_Vtx": max_or_default(tree["mu2_trk_dxy_Vtx"].array()),
            "mu2_trk_dxyError_Vtx": max_or_default(tree["mu2_trk_dxyError_Vtx"].array()),
            "mu3_pt_Vtx": max_or_default(tree["mu3_pt_Vtx"].array()),
            "mu3_eta_Vtx": max_or_default(tree["mu3_eta_Vtx"].array()),
            "mu3_phi_Vtx": max_or_default(tree["mu3_phi_Vtx"].array()),
            "mu3_isGlobal_Vtx": max_or_default(tree["mu3_isGlobal_Vtx"].array()),
            "mu3_isTracker_Vtx": max_or_default(tree["mu3_isTracker_Vtx"].array()),
            "mu3_chi2Ndof_Vtx": max_or_default(tree["mu3_chi2Ndof_Vtx"].array()),
            "mu3_trk_dxy_Vtx": max_or_default(tree["mu3_trk_dxy_Vtx"].array()),
            "mu3_trk_dxyError_Vtx": max_or_default(tree["mu3_trk_dxyError_Vtx"].array()),
            "mu4_pt_Vtx": max_or_default(tree["mu4_pt_Vtx"].array()),
            "mu4_eta_Vtx": max_or_default(tree["mu4_eta_Vtx"].array()),
            "mu4_phi_Vtx": max_or_default(tree["mu4_phi_Vtx"].array()),
            "mu4_isGlobal_Vtx": max_or_default(tree["mu4_isGlobal_Vtx"].array()),
            "mu4_isTracker_Vtx": max_or_default(tree["mu4_isTracker_Vtx"].array()),
            "mu4_chi2Ndof_Vtx": max_or_default(tree["mu4_chi2Ndof_Vtx"].array()),
            "mu4_trk_dxy_Vtx": max_or_default(tree["mu4_trk_dxy_Vtx"].array()),
            "mu4_trk_dxyError_Vtx": max_or_default(tree["mu4_trk_dxyError_Vtx"].array()),

            "label": label
        })
        return df_Vtx

    elif collection == 'NoVtx':
        df_NoVtx = pd.DataFrame({
            # ================= NoVtx =================
            "SV1_chi2_NoVtx": max_or_default(tree["SV1_chi2_NoVtx"].array()),
            "SV1_prob_NoVtx": max_or_default(tree["SV1_prob_NoVtx"].array()),
            "SV1_lxy_NoVtx":  max_or_default(tree["SV1_lxy_NoVtx"].array()),
            "SV1_global_NoVtx":  max_or_default(tree["SV1_global_NoVtx"].array()),
            "SV1_dphi_NoVtx":  max_or_default(tree["SV1_dphi_NoVtx"].array()),
            "SV1_pt_NoVtx":  max_or_default(tree["SV1_pt_NoVtx"].array()),
            "SV1_3Dangle_NoVtx":  max_or_default(tree["SV1_3Dangle_NoVtx"].array()),
            "SV1_L3D_NoVtx":  max_or_default(tree["SV1_L3D_NoVtx"].array()),
            "SV1_xErr_NoVtx":  max_or_default(tree["SV1_xErr_NoVtx"].array()),
            "SV1_yErr_NoVtx":  max_or_default(tree["SV1_yErr_NoVtx"].array()),
            "SV1_zErr_NoVtx":  max_or_default(tree["SV1_zErr_NoVtx"].array()),
            "SV1_mu1_NoVtx":  max_or_default(tree["SV1_mu1_NoVtx"].array()),
            "SV1_mu2_NoVtx":  max_or_default(tree["SV1_mu2_NoVtx"].array()),
            "SV1_ndof_NoVtx":  max_or_default(tree["SV1_ndof_NoVtx"].array()),

            "SV2_chi2_NoVtx": max_or_default(tree["SV2_chi2_NoVtx"].array()),
            "SV2_prob_NoVtx": max_or_default(tree["SV2_prob_NoVtx"].array()),
            "SV2_lxy_NoVtx":  max_or_default(tree["SV2_lxy_NoVtx"].array()),
            "SV2_global_NoVtx":  max_or_default(tree["SV2_global_NoVtx"].array()),
            "SV2_dphi_NoVtx":  max_or_default(tree["SV2_dphi_NoVtx"].array()),
            "SV2_pt_NoVtx":  max_or_default(tree["SV2_pt_NoVtx"].array()),
            "SV2_3Dangle_NoVtx":  max_or_default(tree["SV2_3Dangle_NoVtx"].array()),
            "SV2_L3D_NoVtx":  max_or_default(tree["SV2_L3D_NoVtx"].array()),
            "SV2_xErr_NoVtx":  max_or_default(tree["SV2_xErr_NoVtx"].array()),
            "SV2_yErr_NoVtx":  max_or_default(tree["SV2_yErr_NoVtx"].array()),
            "SV2_zErr_NoVtx":  max_or_default(tree["SV2_zErr_NoVtx"].array()),
            "SV2_mu1_NoVtx":  max_or_default(tree["SV2_mu1_NoVtx"].array()),
            "SV2_mu2_NoVtx":  max_or_default(tree["SV2_mu2_NoVtx"].array()),
            "SV2_ndof_NoVtx":  max_or_default(tree["SV2_ndof_NoVtx"].array()),

            "mu1_pt_NoVtx": max_or_default(tree["mu1_pt_NoVtx"].array()),
            "mu1_eta_NoVtx": max_or_default(tree["mu1_eta_NoVtx"].array()),
            "mu1_phi_NoVtx": max_or_default(tree["mu1_phi_NoVtx"].array()),
            "mu1_isGlobal_NoVtx": max_or_default(tree["mu1_isGlobal_NoVtx"].array()),
            "mu1_isTracker_NoVtx": max_or_default(tree["mu1_isTracker_NoVtx"].array()),
            "mu1_chi2Ndof_NoVtx": max_or_default(tree["mu1_chi2Ndof_NoVtx"].array()),
            "mu1_trk_dxy_NoVtx": max_or_default(tree["mu1_trk_dxy_NoVtx"].array()),
            "mu1_trk_dxyError_NoVtx": max_or_default(tree["mu1_trk_dxyError_NoVtx"].array()),
            "mu2_pt_NoVtx": max_or_default(tree["mu2_pt_NoVtx"].array()),
            "mu2_eta_NoVtx": max_or_default(tree["mu2_eta_NoVtx"].array()),
            "mu2_phi_NoVtx": max_or_default(tree["mu2_phi_NoVtx"].array()),
            "mu2_isGlobal_NoVtx": max_or_default(tree["mu2_isGlobal_NoVtx"].array()),
            "mu2_isTracker_NoVtx": max_or_default(tree["mu2_isTracker_NoVtx"].array()),
            "mu2_chi2Ndof_NoVtx": max_or_default(tree["mu2_chi2Ndof_NoVtx"].array()),
            "mu2_trk_dxy_NoVtx": max_or_default(tree["mu2_trk_dxy_NoVtx"].array()),
            "mu2_trk_dxyError_NoVtx": max_or_default(tree["mu2_trk_dxyError_NoVtx"].array()),
            "mu3_pt_NoVtx": max_or_default(tree["mu3_pt_NoVtx"].array()),
            "mu3_eta_NoVtx": max_or_default(tree["mu3_eta_NoVtx"].array()),
            "mu3_phi_NoVtx": max_or_default(tree["mu3_phi_NoVtx"].array()),
            "mu3_isGlobal_NoVtx": max_or_default(tree["mu3_isGlobal_NoVtx"].array()),
            "mu3_isTracker_NoVtx": max_or_default(tree["mu3_isTracker_NoVtx"].array()),
            "mu3_chi2Ndof_NoVtx": max_or_default(tree["mu3_chi2Ndof_NoVtx"].array()),
            "mu3_trk_dxy_NoVtx": max_or_default(tree["mu3_trk_dxy_NoVtx"].array()),
            "mu3_trk_dxyError_NoVtx": max_or_default(tree["mu3_trk_dxyError_NoVtx"].array()),
            "mu4_pt_NoVtx": max_or_default(tree["mu4_pt_NoVtx"].array()),
            "mu4_eta_NoVtx": max_or_default(tree["mu4_eta_NoVtx"].array()),
            "mu4_phi_NoVtx": max_or_default(tree["mu4_phi_NoVtx"].array()),
            "mu4_isGlobal_NoVtx": max_or_default(tree["mu4_isGlobal_NoVtx"].array()),
            "mu4_isTracker_NoVtx": max_or_default(tree["mu4_isTracker_NoVtx"].array()),
            "mu4_chi2Ndof_NoVtx": max_or_default(tree["mu4_chi2Ndof_NoVtx"].array()),
            "mu4_trk_dxy_NoVtx": max_or_default(tree["mu4_trk_dxy_NoVtx"].array()),
            "mu4_trk_dxyError_NoVtx": max_or_default(tree["mu4_trk_dxyError_NoVtx"].array()),

            "label": label
        })
        return df_NoVtx

print('Preparing signal dataframe...')

df_sig_Vtx = build_dataframe(filename_sig, 1, 'Vtx')
df_sig_NoVtx = build_dataframe(filename_sig, 1, 'NoVtx')

print('Preparing background dataframe...')
df_QCD_50to80_Vtx = build_dataframe(QCD_50to80, 0, 'Vtx')
df_QCD_50to80_NoVtx = build_dataframe(QCD_50to80, 0, 'NoVtx')
df_QCD_80to120_Vtx = build_dataframe(QCD_80to120, 0, 'Vtx')
df_QCD_80to120_NoVtx = build_dataframe(QCD_80to120, 0, 'NoVtx')
#df_QCD_120to170_Vtx = build_dataframe(QCD_120to170, 0, 'Vtx')
#df_QCD_120to170_NoVtx = build_dataframe(QCD_120to170, 0, 'NoVtx')

#df_bkg_Vtx = pd.concat([df_QCD_50to80_Vtx, df_QCD_80to120_Vtx, df_QCD_120to170_Vtx], ignore_index=True)
#df_bkg_NoVtx = pd.concat([df_QCD_50to80_NoVtx, df_QCD_80to120_NoVtx, df_QCD_120to170_NoVtx], ignore_index=True)
df_bkg_Vtx = pd.concat([df_QCD_50to80_Vtx, df_QCD_80to120_Vtx], ignore_index=True)
df_bkg_NoVtx = pd.concat([df_QCD_50to80_NoVtx, df_QCD_80to120_NoVtx], ignore_index=True)


df_Vtx = pd.concat([df_sig_Vtx, df_bkg_Vtx], ignore_index=True)
df_NoVtx = pd.concat([df_sig_NoVtx, df_bkg_NoVtx], ignore_index=True)

lxy_bins = [0.0, 0.2, 1.0, 2.4, 3.1, 7.0, 11.0, 16.0, 70.0]

lxy_labels = ["0p0to0p2", "0p2to1p0", "1p0to2p4", "2p4to3p1", "3p1to7p0", "7p0to11p0", "11p0to16p0", "16p0to70p0"]

df_Vtx["lxy_bin"] = pd.cut(df_Vtx["SV1_lxy_Vtx"], bins=lxy_bins, labels=lxy_labels, include_lowest=True)
df_NoVtx["lxy_bin"] = pd.cut(df_NoVtx["SV1_lxy_NoVtx"], bins=lxy_bins, labels=lxy_labels, include_lowest=True)


cut_points_dict = {
    1: {
        "0p0to0p2": (0.026, 0.996),
        "0p2to1p0": (0.048, 0.991),
        "1p0to2p4": (0.065, 0.986),
        "2p4to3p1": (0.066, 0.990),
        "3p1to7p0": (0.064, 0.988),
        "7p0to11p0": (0.045, 1.000),
        "11p0to16p0": (0.050, 1.000),
        "16p0to70p0": (0.015, 1.000)
    },
    10: {
        "0p0to0p2": (0.014, 0.996),
        "0p2to1p0": (0.042, 0.991),
        "1p0to2p4": (0.057, 0.986),
        "2p4to3p1": (0.064, 0.990),
        "3p1to7p0": (0.064, 0.988),
        "7p0to11p0": (0.060, 1.000),
        "11p0to16p0": (0.045, 1.000),
        "16p0to70p0": (0.020, 1.000)
    },
    100: {
        "0p0to0p2": (0.001, 0.996),
        "0p2to1p0": (0.029, 0.991),
        "1p0to2p4": (0.029, 0.986),
        "2p4to3p1": (0.045, 0.990),
        "3p1to7p0": (0.031, 0.988),
        "7p0to11p0": (0.028, 1.000),
        "11p0to16p0": (0.020, 1.000),
        "16p0to70p0": (0.011, 1.000)
    }
}

for bin_label in lxy_labels:

    print(f"\n=== Lxy bin: {bin_label} ===")

    # ================= Vtx =================
    df_bin_Vtx = df_Vtx[df_Vtx["lxy_bin"] == bin_label].copy()
    df_bin_NoVtx = df_NoVtx[df_NoVtx["lxy_bin"] == bin_label].copy()

    print(len(df_bin_Vtx))
    print(len(df_bin_NoVtx))
    if len(df_bin_Vtx) < 100 or len(df_bin_NoVtx) < 100:
        print("Not enough events, skipping")
        continue

    X_Vtx_bin = df_bin_Vtx.drop(["label", "lxy_bin"], axis=1)
    y_Vtx_bin = df_bin_Vtx["label"]

    X_NoVtx_bin = df_bin_NoVtx.drop(["label", "lxy_bin"], axis=1)
    y_NoVtx_bin = df_bin_NoVtx["label"]

    X_train_Vtx, X_test_Vtx, y_train_Vtx, y_test_Vtx = train_test_split(
        X_Vtx_bin, y_Vtx_bin, test_size=0.3, random_state=42, stratify=y_Vtx_bin
    )

    X_train_NoVtx, X_test_NoVtx, y_train_NoVtx, y_test_NoVtx = train_test_split(
        X_NoVtx_bin, y_NoVtx_bin, test_size=0.3, random_state=42, stratify=y_NoVtx_bin
    )

    # Train models
    bdt_Vtx = XGBClassifier(
        n_estimators=100,
        max_depth=3,
        learning_rate=0.1,
        use_label_encoder=False,
        eval_metric="logloss"
    )

    bdt_NoVtx = XGBClassifier(
        n_estimators=100,
        max_depth=3,
        learning_rate=0.1,
        use_label_encoder=False,
        eval_metric="logloss"
    )

    bdt_Vtx.fit(X_train_Vtx, y_train_Vtx)
    bdt_NoVtx.fit(X_train_NoVtx, y_train_NoVtx)

    y_pred_prob_Vtx = bdt_Vtx.predict_proba(X_test_Vtx)[:, 1]
    y_pred_prob_NoVtx = bdt_NoVtx.predict_proba(X_test_NoVtx)[:, 1]

    # ================= ROC =================
    fpr_Vtx, tpr_Vtx, _ = roc_curve(y_test_Vtx, y_pred_prob_Vtx)
    fpr_NoVtx, tpr_NoVtx, _ = roc_curve(y_test_NoVtx, y_pred_prob_NoVtx)

    epsilon = 1e-6  # tiny value to avoid log(0)

    # clip FPR/TPR to avoid zeros
    fpr_Vtx_plot = np.clip(fpr_Vtx, epsilon, 1)
    tpr_Vtx_plot = np.clip(tpr_Vtx, epsilon, 1)
    
    fpr_NoVtx_plot = np.clip(fpr_NoVtx, epsilon, 1)
    tpr_NoVtx_plot = np.clip(tpr_NoVtx, epsilon, 1)

    fig, ax = plt.subplots(figsize=(6, 6), constrained_layout=True)

    ax.plot(fpr_Vtx, tpr_Vtx,
            label=f'Vtx (AUC = {roc_auc_score(y_test_Vtx, y_pred_prob_Vtx):.3f})')

    ax.plot(fpr_NoVtx, tpr_NoVtx,
            label=f'NoVtx (AUC = {roc_auc_score(y_test_NoVtx, y_pred_prob_NoVtx):.3f})')

    ax.plot([0, 1], [0, 1], 'k--', alpha=0.5)
    sig_eff, bkg_rej = cut_points_dict[ctau][bin_label]
    ax.scatter(1-bkg_rej, sig_eff, color='red', s=60, label='Cut Point', zorder=5)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title(f"ROC Curve (ctau = {ctau}mm, Lxy = {bin_label})")
    ax.legend(loc="lower right")

    fig.savefig(f'curves_comp_{model}/ROC_ctau_{ctau}_lxy_{bin_label}_log.png',
                dpi=150, bbox_inches="tight")
    plt.close(fig)

    # ================= Feature importance Vtx =================
    importances_Vtx = bdt_Vtx.feature_importances_
    feat_names_Vtx = X_Vtx_bin.columns

    fig, ax = plt.subplots(figsize=(8, 10), constrained_layout=True)
    ax.barh(feat_names_Vtx, importances_Vtx)
    ax.set_xlabel("Feature importance (Vtx)")
    ax.set_ylabel("Variable")
    ax.set_title(f"Feature Importance Vtx (ctau = {ctau}mm, Lxy = {bin_label})")
    ax.tick_params(axis='y', labelsize=8)
    ax.invert_yaxis()

    fig.savefig(f'curves_comp_{model}/FeatImp_Vtx_ctau_{ctau}_lxy_{bin_label}.png',
                dpi=150, bbox_inches="tight")
    plt.close(fig)

    # ================= Feature importance NoVtx =================
    importances_NoVtx = bdt_NoVtx.feature_importances_
    feat_names_NoVtx = X_NoVtx_bin.columns

    fig, ax = plt.subplots(figsize=(8, 10), constrained_layout=True)
    ax.barh(feat_names_NoVtx, importances_NoVtx)
    ax.set_xlabel("Feature importance (NoVtx)")
    ax.set_ylabel("Variable")
    ax.set_title(f"Feature Importance NoVtx (ctau = {ctau}mm, Lxy = {bin_label})")
    ax.tick_params(axis='y', labelsize=8)
    ax.invert_yaxis()

    fig.savefig(f'curves_comp_{model}/FeatImp_NoVtx_ctau_{ctau}_lxy_{bin_label}.png',
                dpi=150, bbox_inches="tight")
    plt.close(fig)