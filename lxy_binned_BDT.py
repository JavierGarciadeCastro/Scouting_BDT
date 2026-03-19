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
mA = 0.40
if model == 'A' and mA == 0.40:
    if ctau == 1:
        filename_sig = 'signal_A_ctau_1mm_mA_0p40_mpi_4.root'
    elif ctau == 10:
        filename_sig = 'signal_A_ctau_10mm_mA_0p40_mpi_4.root'
    elif ctau == 100:
        filename_sig = 'signal_A_ctau_100mm_mA_0p40_mpi_4.root'
elif model == 'A' and mA == 2:
    if ctau == 1:
        filename_sig = 'signal_A_ctau_1mm_mA_2p0_mpi_10.root'
    elif ctau == 10:
        filename_sig = 'signal_A_ctau_10mm_mA_2p0_mpi_10.root'
    elif ctau == 100:
        filename_sig = 'signal_A_ctau_100mm_mA_2p0_mpi_10.root'
    
if model == 'B':
    if ctau == 1:
        filename_sig = 'signal_B_1mm.root'
    elif ctau == 10:
        filename_sig = 'signal_B_10mm.root'
    elif ctau == 100:
        filename_sig = 'signal_B_100mm.root'

print(filename_sig)

def get_filename(model, ctau, mA, mpi):
    if model == 'A':
        return f"signal_A_ctau_{ctau_map[ctau]}mm_mA_{mA_map[mA]}_mpi_{mpi_map[mpi]}.root"
    elif model == 'B':
        return f"signal_B_ctau_{ctau_map[ctau]}mm_mA_{mA_map[mA]}_mpi_{mpi_map[mpi]}.root"

def build_dataframe(filename, label, collection):
    file = uproot.open(root_output / filename)
    tree = file["tout"]

    def max_or_default(array, default=np.nan):
        return ak.to_numpy(ak.fill_none(ak.max(array, axis=1), default))

    branches = tree.keys()
    data = {}

    if collection == 'Vtx':
        prefix = "_Vtx"
    elif collection == 'NoVtx':
        prefix = "_NoVtx"

    sv_vars = ["chi2","prob","lxy","global","dphi","pt","3Dangle","L3D","xErr","yErr","zErr","mu1","mu2","ndof"]
    mu_vars = ["pt","eta","phi","isGlobal","isTracker","chi2Ndof","trk_dxy","trk_dxyError"]

    for sv in [1, 2]:
        for var in sv_vars:
            name = f"SV{sv}_{var}{prefix}"
            if name in branches:
                data[name] = max_or_default(tree[name].array())

    for mu in [1, 2, 3, 4]:
        for var in mu_vars:
            name = f"mu{mu}_{var}{prefix}"
            if name in branches:
                data[name] = max_or_default(tree[name].array())

    df = pd.DataFrame(data)

    # SV swap (sort by probability, fillna so NaNs don't break comparison)
    swap = df[f"SV2_prob{prefix}"].fillna(0) > df[f"SV1_prob{prefix}"].fillna(0)
    for var in sv_vars:
        sv1 = f"SV1_{var}{prefix}"
        sv2 = f"SV2_{var}{prefix}"
        if sv1 in df.columns and sv2 in df.columns:
            a = df[sv1].copy()
            b = df[sv2].copy()
            df[sv1] = np.where(swap, b, a)
            df[sv2] = np.where(swap, a, b)

    # Muon reordering: sort by descending pt, NaNs go last
    pt_cols = [f"mu{i}_pt{prefix}" for i in range(1, 5)]
    pt_stacked = np.stack([df[c].values for c in pt_cols], axis=1)
    sort_idx = np.argsort(-np.where(np.isnan(pt_stacked), -np.inf, pt_stacked), axis=1)

    for var in mu_vars:
        cols = [f"mu{i}_{var}{prefix}" for i in range(1, 5)]
        if not all(c in df.columns for c in cols):
            continue
        stacked = np.stack([df[c].values for c in cols], axis=1)
        sorted_vals = stacked[np.arange(len(df))[:, None], sort_idx]
        for i in range(4):
            df[f"mu{i+1}_{var}{prefix}"] = sorted_vals[:, i]

    df["label"] = label
    return df
def build_OR_dataframe(df_Vtx, df_NoVtx, prefix_vtx="_Vtx", prefix_novtx="_NoVtx"):
    n = len(df_Vtx)

    sv_vars = ["chi2","prob","lxy","global","dphi","pt","3Dangle","L3D","xErr","yErr","zErr","mu1","mu2","ndof"]
    mu_vars = ["pt","eta","phi","isGlobal","isTracker","chi2Ndof","trk_dxy","trk_dxyError"]

    # Stack SV arrays: shape (n, 2) for SV1 and SV2
    lxy_vtx = np.stack([df_Vtx[f"SV{s}_lxy{prefix_vtx}"].values   for s in [1,2]], axis=1)
    pt_vtx  = np.stack([df_Vtx[f"SV{s}_pt{prefix_vtx}"].values    for s in [1,2]], axis=1)
    lxy_novtx = np.stack([df_NoVtx[f"SV{s}_lxy{prefix_novtx}"].values for s in [1,2]], axis=1)
    pt_novtx  = np.stack([df_NoVtx[f"SV{s}_pt{prefix_novtx}"].values  for s in [1,2]], axis=1)

    use_vtx_sv = (lxy_vtx > 0)  # shape (n, 2)

    result = {}

    # Initialize SV result arrays from Vtx where available, else NoVtx SV1
    for si, sv in enumerate([1, 2]):
        for var in sv_vars:
            vtx_col   = f"SV{sv}_{var}{prefix_vtx}"
            novtx_col = f"SV{sv}_{var}{prefix_novtx}"
            if vtx_col in df_Vtx.columns and novtx_col in df_NoVtx.columns:
                result[f"SV{sv}_{var}"] = np.where(
                    use_vtx_sv[:, si],
                    df_Vtx[vtx_col].values,
                    df_NoVtx[novtx_col].values
                )

    # For events where use_vtx_sv is False, try to add unmatched NoVtx SVs
    # matched_novtx[i, nj] = True if NoVtx SV nj is matched to any Vtx SV
    matched_novtx_sv = np.zeros((n, 2), dtype=bool)
    for vi in range(2):
        for ni in range(2):
            has_vtx_sv = lxy_vtx[:, vi] > 0
            dlxy = np.abs(lxy_vtx[:, vi] - lxy_novtx[:, ni])
            dpt  = np.abs(pt_vtx[:, vi]  - pt_novtx[:, ni])
            matched_novtx_sv[:, ni] |= (has_vtx_sv & (dlxy < 0.1) & (dpt < 0.2))

    unmatched_novtx_sv = (lxy_novtx > 0) & ~matched_novtx_sv  # shape (n, 2)

    n_vtx_svs = (lxy_vtx > 0).sum(axis=1)  # how many Vtx SVs each event has

    slot = np.zeros(n, dtype=int)
    for ni in range(2):
        is_unmatched = unmatched_novtx_sv[:, ni]
        target_slot  = n_vtx_svs + slot
        for s in range(2):
            mask = is_unmatched & (target_slot == s)
            if not mask.any():
                continue
            for var in sv_vars:
                novtx_col = f"SV{ni+1}_{var}{prefix_novtx}"
                current   = result[f"SV{s+1}_{var}"]
                result[f"SV{s+1}_{var}"] = np.where(
                    mask,
                    df_NoVtx[novtx_col].values,
                    current
                )
        slot += is_unmatched.astype(int)

    # ================= Muon variables =================
    mu_eta_vtx   = np.stack([df_Vtx[f"mu{i}_eta{prefix_vtx}"].values    for i in range(1,5)], axis=1)
    mu_phi_vtx   = np.stack([df_Vtx[f"mu{i}_phi{prefix_vtx}"].values    for i in range(1,5)], axis=1)
    mu_pt_vtx    = np.stack([df_Vtx[f"mu{i}_pt{prefix_vtx}"].values     for i in range(1,5)], axis=1)
    mu_eta_novtx = np.stack([df_NoVtx[f"mu{i}_eta{prefix_novtx}"].values for i in range(1,5)], axis=1)
    mu_phi_novtx = np.stack([df_NoVtx[f"mu{i}_phi{prefix_novtx}"].values for i in range(1,5)], axis=1)
    mu_pt_novtx  = np.stack([df_NoVtx[f"mu{i}_pt{prefix_novtx}"].values  for i in range(1,5)], axis=1)

    matched_novtx = np.zeros((n, 4), dtype=bool)
    for vi in range(4):
        for ni in range(4):
            deta = mu_eta_vtx[:, vi] - mu_eta_novtx[:, ni]
            dphi = (mu_phi_vtx[:, vi] - mu_phi_novtx[:, ni] + np.pi) % (2*np.pi) - np.pi
            dR   = np.sqrt(deta**2 + dphi**2)
            has_vtx_mu = mu_pt_vtx[:, vi] > 0
            matched_novtx[:, ni] |= (has_vtx_mu & (dR < 0.1))

    unmatched_novtx = (mu_pt_novtx > 0) & ~matched_novtx
    n_vtx_muons = (mu_pt_vtx > 0).sum(axis=1)

    for vi in range(4):
        vtx_col_exists = mu_pt_vtx[:, vi] > 0
        for var in mu_vars:
            vtx_vals = df_Vtx[f"mu{vi+1}_{var}{prefix_vtx}"].values
            result[f"mu{vi+1}_{var}"] = np.where(vtx_col_exists, vtx_vals, 0.0)

    slot = np.zeros(n, dtype=int)
    for ni in range(4):
        is_unmatched = unmatched_novtx[:, ni]
        target_slot  = n_vtx_muons + slot
        for s in range(4):
            mask = is_unmatched & (target_slot == s)
            if not mask.any():
                continue
            for var in mu_vars:
                novtx_vals = df_NoVtx[f"mu{ni+1}_{var}{prefix_novtx}"].values
                current    = result[f"mu{s+1}_{var}"]
                result[f"mu{s+1}_{var}"] = np.where(mask, novtx_vals, current)
        slot += is_unmatched.astype(int)

    result["label"] = df_Vtx["label"].values

    return pd.DataFrame(result)

def compute_class_weights(y):
    """Return per-sample weights so that sum(w[signal]) == sum(w[background])."""
    n_sig = (y == 1).sum()
    n_bkg = (y == 0).sum()
    w = np.where(y == 1, n_bkg / n_sig, 1.0)  # upweight signal, keep bkg at 1
    return w



# ================= Load signal =================
print('Preparing signal dataframe...')
df_sig_Vtx = build_dataframe(filename_sig, 1, 'Vtx')
df_sig_NoVtx = build_dataframe(filename_sig, 1, 'NoVtx')
df_sig_OR    = build_OR_dataframe(df_sig_Vtx, df_sig_NoVtx)

# ================= Load background =================
print('Preparing background dataframe...')

df_bkg_Vtx = pd.concat([
    build_dataframe('QCD15to20.root',   0, 'Vtx'),
    build_dataframe('QCD20to30.root',   0, 'Vtx'),
    build_dataframe('QCD30to50.root',   0, 'Vtx'),
    build_dataframe('QCD50to80.root',   0, 'Vtx'),
    build_dataframe('QCD80to120.root',  0, 'Vtx'),
    build_dataframe('QCD120to170.root', 0, 'Vtx'),
    build_dataframe('QCD170to300.root', 0, 'Vtx'),
    build_dataframe('QCD300to470.root', 0, 'Vtx'),
    build_dataframe('QCD470to600.root', 0, 'Vtx'),
    build_dataframe('QCD600to800.root', 0, 'Vtx'),
    build_dataframe('QCD800to1000.root', 0, 'Vtx')
], ignore_index=True)


df_bkg_NoVtx = pd.concat([
    build_dataframe('QCD15to20.root',   0, 'NoVtx'),
    build_dataframe('QCD20to30.root',   0, 'NoVtx'),
    build_dataframe('QCD30to50.root',   0, 'NoVtx'),
    build_dataframe('QCD50to80.root',   0, 'NoVtx'),
    build_dataframe('QCD80to120.root',  0, 'NoVtx'),
    build_dataframe('QCD120to170.root', 0, 'NoVtx'),
    build_dataframe('QCD170to300.root', 0, 'NoVtx'),
    build_dataframe('QCD300to470.root', 0, 'NoVtx'),
    build_dataframe('QCD470to600.root', 0, 'NoVtx'),
    build_dataframe('QCD600to800.root', 0, 'NoVtx'),
    build_dataframe('QCD800to1000.root', 0, 'NoVtx')
], ignore_index=True)

df_bkg_OR = build_OR_dataframe(df_bkg_Vtx, df_bkg_NoVtx)


df_Vtx = pd.concat([df_sig_Vtx, df_bkg_Vtx], ignore_index=True)
df_NoVtx = pd.concat([df_sig_NoVtx, df_bkg_NoVtx], ignore_index=True)
df_OR = pd.concat([df_sig_OR, df_bkg_OR], ignore_index=True)

lxy_bins = [0.0, 0.2, 1.0, 2.4, 3.1, 7.0, 11.0, 16.0, 70.0]

lxy_labels = ["0p0to0p2", "0p2to1p0", "1p0to2p4", "2p4to3p1", "3p1to7p0", "7p0to11p0", "11p0to16p0", "16p0to70p0"]

df_Vtx["lxy_bin"] = pd.cut(df_Vtx["SV1_lxy_Vtx"], bins=lxy_bins, labels=lxy_labels, include_lowest=True)
df_NoVtx["lxy_bin"] = pd.cut(df_NoVtx["SV1_lxy_NoVtx"], bins=lxy_bins, labels=lxy_labels, include_lowest=True)
df_OR["lxy_bin"] = pd.cut(df_OR["SV1_lxy"], bins=lxy_bins, labels=lxy_labels, include_lowest=True)


#cut_signal1A = {
#    1: {"0p0to0p2": (0.026, 0.897),"0p2to1p0": (0.413, 0.749),"1p0to2p4": (0.564, 0.677),"2p4to3p1": (0.636, 0.706),"3p1to7p0": (0.705, 0.746),"7p0to11p0": (0.760, 0.902),"11p0to16p0": (0.639, 0.925),"16p0to70p0": (0.301, 0.969)},
#    10: {"0p0to0p2": (0.141, 0.897),"0p2to1p0": (0.473, 0.749),"1p0to2p4": (0.653, 0.677),"2p4to3p1": (0.717, 0.706),"3p1to7p0": (0.756, 0.746),"7p0to11p0": (0.767, 0.902),"11p0to16p0": (0.647, 0.925),"16p0to70p0": (0.320, 0.969)},
#    100: {"0p0to0p2": (0.313, 0.897),"0p2to1p0": (0.474, 0.749),"1p0to2p4": (0.633, 0.677),"2p4to3p1": (0.695, 0.706),"3p1to7p0": (0.704, 0.746),"7p0to11p0": (0.633, 0.902),"11p0to16p0": (0.450, 0.925),"16p0to70p0": (0.127, 0.969)}
#}

for bin_label in lxy_labels:

    print(f"\n=== Lxy bin: {bin_label} ===")

    # ================= Vtx =================
    df_bin_Vtx = df_Vtx[df_Vtx["lxy_bin"] == bin_label].copy()
    df_bin_NoVtx = df_NoVtx[df_NoVtx["lxy_bin"] == bin_label].copy()
    df_bin_OR = df_OR[df_OR["lxy_bin"] == bin_label].copy()

    print("Vtx events: ", len(df_bin_Vtx))
    print("NoVtx events: ", len(df_bin_NoVtx))
    print("OR events: ", len(df_bin_OR))
    if len(df_bin_Vtx) < 100 or len(df_bin_NoVtx) < 100:
        print("Not enough events, skipping")
        continue

    X_Vtx_bin = df_bin_Vtx.drop(["label", "lxy_bin"], axis=1)
    y_Vtx_bin = df_bin_Vtx["label"]

    X_NoVtx_bin = df_bin_NoVtx.drop(["label", "lxy_bin"], axis=1)
    y_NoVtx_bin = df_bin_NoVtx["label"]

    X_OR_bin = df_bin_OR.drop(["label", "lxy_bin"], axis=1)
    y_OR_bin = df_bin_OR["label"]

    w_Vtx   = compute_class_weights(y_Vtx_bin.values)
    w_NoVtx = compute_class_weights(y_NoVtx_bin.values)
    w_OR    = compute_class_weights(y_OR_bin.values)

    X_train_Vtx, X_test_Vtx, y_train_Vtx, y_test_Vtx, w_train_Vtx, w_test_Vtx = train_test_split(X_Vtx_bin, y_Vtx_bin, w_Vtx, test_size=0.3, random_state=42, stratify=y_Vtx_bin)
    X_train_NoVtx, X_test_NoVtx, y_train_NoVtx, y_test_NoVtx, w_train_NoVtx, w_test_NoVtx = train_test_split(X_NoVtx_bin, y_NoVtx_bin, w_NoVtx, test_size=0.3, random_state=42, stratify=y_NoVtx_bin)
    X_train_OR, X_test_OR, y_train_OR, y_test_OR, w_train_OR, w_test_OR = train_test_split(X_OR_bin, y_OR_bin, w_OR, test_size=0.3, random_state=42, stratify=y_OR_bin)

    bdt_Vtx = XGBClassifier(n_estimators=100, max_depth=3, learning_rate=0.1, use_label_encoder=False, eval_metric="logloss", tree_method='hist', n_jobs=1)
    bdt_NoVtx = XGBClassifier(n_estimators=100, max_depth=3, learning_rate=0.1, use_label_encoder=False, eval_metric="logloss", tree_method='hist', n_jobs=1)
    bdt_OR = XGBClassifier(n_estimators=100, max_depth=3, learning_rate=0.1, use_label_encoder=False, eval_metric="logloss", tree_method='hist', n_jobs=1)

 
    bdt_Vtx.fit(X_train_Vtx, y_train_Vtx, sample_weight=w_train_Vtx)
    bdt_NoVtx.fit(X_train_NoVtx, y_train_NoVtx, sample_weight=w_train_NoVtx)
    bdt_OR.fit(X_train_OR, y_train_OR, sample_weight=w_train_OR)

    y_pred_prob_Vtx = bdt_Vtx.predict_proba(X_test_Vtx)[:, 1]
    y_pred_prob_NoVtx = bdt_NoVtx.predict_proba(X_test_NoVtx)[:, 1]
    y_pred_prob_OR = bdt_OR.predict_proba(X_test_OR)[:, 1]

    # ================= ROC =================

    os.makedirs(f'curves_comp_{model}', exist_ok=True)

    fpr_Vtx, tpr_Vtx, _ = roc_curve(y_test_Vtx, y_pred_prob_Vtx)
    fpr_NoVtx, tpr_NoVtx, _ = roc_curve(y_test_NoVtx, y_pred_prob_NoVtx)
    fpr_OR, tpr_OR, _ = roc_curve(y_test_OR, y_pred_prob_OR)


    fig, ax = plt.subplots(figsize=(6, 6), constrained_layout=True)

    ax.plot(fpr_Vtx, tpr_Vtx, label=f'Vtx (AUC = {roc_auc_score(y_test_Vtx, y_pred_prob_Vtx):.3f})')
    ax.plot(fpr_NoVtx, tpr_NoVtx, label=f'NoVtx (AUC = {roc_auc_score(y_test_NoVtx, y_pred_prob_NoVtx):.3f})')
    ax.plot(fpr_OR, tpr_OR, label=f'OR (AUC = {roc_auc_score(y_test_OR, y_pred_prob_OR):.3f})')

    ax.plot([0, 1], [0, 1], 'k--', alpha=0.5)
    #sig_eff, bkg_rej = cut_signal1A[ctau][bin_label]
    #ax.scatter(1-bkg_rej, sig_eff, color='red', s=60, label='Cut and Count', zorder=5)
    #ax.set_xscale('log')
    #ax.set_yscale('log')
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title(f"ROC Curve (ctau = {ctau}mm, Lxy = {bin_label})")
    ax.legend(loc="lower right")

    fig.savefig(f'curves_comp_{model}/ROC_ctau_{ctau}_lxy_{bin_label}.png', dpi=150, bbox_inches="tight")
    plt.close(fig)

    for tag, bdt, X_bin in [("Vtx", bdt_Vtx, X_Vtx_bin), ("NoVtx", bdt_NoVtx, X_NoVtx_bin), ("OR", bdt_OR, X_OR_bin)]:
        importances = bdt.feature_importances_
        feat_names  = X_bin.columns
        sorted_idx  = np.argsort(importances)
        fig, ax = plt.subplots(figsize=(8, 10), constrained_layout=True)
        ax.barh(feat_names[sorted_idx], importances[sorted_idx])
        ax.set_xlabel(f"Feature importance ({tag})")
        ax.set_ylabel("Variable")
        ax.set_title(f"Feature Importance {tag} (ctau={ctau}mm, Lxy={bin_label})")
        ax.tick_params(axis='y', labelsize=8)
        fig.savefig(f'curves_comp_{model}/FeatImp_{tag}_ctau_{ctau}_lxy_{bin_label}.png', dpi=150, bbox_inches="tight")
        plt.close(fig)