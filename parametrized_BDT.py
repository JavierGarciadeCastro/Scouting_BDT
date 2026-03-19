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

ctau_values = [1, 10, 100]
mA_values   = [0.40, 2.0]
mpi_values  = [4, 10]

use_conditional = True
model = 'A'

ctau_map = {1: "1", 10: "10", 100: "100"}
mA_map   = {0.40: "0p40", 2.0: "2p0"}
mpi_map  = {4: "4", 10: "10"}

def get_filename(model, ctau, mA, mpi):
    if model == 'A':
        return f"signal_A_ctau_{ctau_map[ctau]}mm_mA_{mA_map[mA]}_mpi_{mpi_map[mpi]}.root"
    elif model == 'B':
        return f"signal_B_ctau_{ctau_map[ctau]}mm_mA_{mA_map[mA]}_mpi_{mpi_map[mpi]}.root"

def build_dataframe(filename, label, collection, ctau_val=None, mA_val=None, mpi_val=None):
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

    # SV swap (sort by probability)
    swap = df[f"SV2_prob{prefix}"] > df[f"SV1_prob{prefix}"]
    for var in sv_vars:
        sv1 = f"SV1_{var}{prefix}"
        sv2 = f"SV2_{var}{prefix}"
        if sv1 in df.columns and sv2 in df.columns:
            a = df[sv1].copy()
            b = df[sv2].copy()
            df[sv1] = np.where(swap, b, a)
            df[sv2] = np.where(swap, a, b)


    # Muon swap: reorder muons by descending pt

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

    if label == 1:
        df["param_ctau"] = float(ctau_val)
        df["param_mA"]   = float(mA_val)
        df["param_mpi"]  = float(mpi_val)
    else:
        # No params assigned here - will be stamped per param point in the loop
        df["param_ctau"] = np.nan
        df["param_mA"]   = np.nan
        df["param_mpi"]  = np.nan

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
    for col in ["param_ctau", "param_mA", "param_mpi"]:
        if col in df_Vtx.columns:
            result[col] = df_Vtx[col].values

    return pd.DataFrame(result)

def compute_class_weights(y):
    """Return per-sample weights so that sum(w[signal]) == sum(w[background])."""
    n_sig = (y == 1).sum()
    n_bkg = (y == 0).sum()
    w = np.where(y == 1, n_bkg / n_sig, 1.0)  # upweight signal, keep bkg at 1
    return w

# ================= Load signal =================
print('Preparing signal dataframe...')
mass_points = [(0.40, 4), (2.0, 10)]

all_sig_Vtx, all_sig_NoVtx = [], []
for c in ctau_values:
    for m, mp in mass_points:
        f = get_filename(model, c, m, mp)
        all_sig_Vtx.append(build_dataframe(f, 1, 'Vtx',   c, m, mp))
        all_sig_NoVtx.append(build_dataframe(f, 1, 'NoVtx', c, m, mp))

df_sig_Vtx   = pd.concat(all_sig_Vtx,   ignore_index=True)
df_sig_NoVtx = pd.concat(all_sig_NoVtx, ignore_index=True)
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

print("Total number of background events (Vtx): ", len(df_bkg_Vtx))
print("Total number of background events (NoVtx): ", len(df_bkg_NoVtx))
print("Total number of background events (OR): ", len(df_bkg_OR))

print("Total number of signal events (Vtx): ", len(df_sig_Vtx))
print("Total number of signal events (NoVtx): ", len(df_sig_NoVtx))
print("Total number of signal events (OR): ", len(df_sig_OR))

# ================= Lxy binning =================
lxy_bins   = [0.0, 0.2, 1.0, 2.4, 3.1, 7.0, 11.0, 16.0, 70.0]
lxy_labels = ["0p0to0p2","0p2to1p0","1p0to2p4","2p4to3p1","3p1to7p0","7p0to11p0","11p0to16p0","16p0to70p0"]

df_sig_Vtx["lxy_bin"]   = pd.cut(df_sig_Vtx["SV1_lxy_Vtx"],     bins=lxy_bins, labels=lxy_labels, include_lowest=True)
df_sig_NoVtx["lxy_bin"] = pd.cut(df_sig_NoVtx["SV1_lxy_NoVtx"], bins=lxy_bins, labels=lxy_labels, include_lowest=True)
df_sig_OR["lxy_bin"]    = pd.cut(df_sig_OR["SV1_lxy"],           bins=lxy_bins, labels=lxy_labels, include_lowest=True)
df_bkg_Vtx["lxy_bin"]   = pd.cut(df_bkg_Vtx["SV1_lxy_Vtx"],     bins=lxy_bins, labels=lxy_labels, include_lowest=True)
df_bkg_NoVtx["lxy_bin"] = pd.cut(df_bkg_NoVtx["SV1_lxy_NoVtx"], bins=lxy_bins, labels=lxy_labels, include_lowest=True)
df_bkg_OR["lxy_bin"]    = pd.cut(df_bkg_OR["SV1_lxy"],           bins=lxy_bins, labels=lxy_labels, include_lowest=True)

# params are kept as features, only drop label and lxy_bin
if use_conditional:
    drop_cols = ["label", "lxy_bin"]
else:
    drop_cols = ["label", "lxy_bin", "param_ctau", "param_mA", "param_mpi"]

param_grid = [(c, m, mp) for c in ctau_values for m, mp in mass_points]
print("Param grid: ", param_grid)

os.makedirs(f'curves_even_CB{model}', exist_ok=True)

# ================= Main loop =================
for bin_label in lxy_labels:
    print(f"\n=== Lxy bin: {bin_label} ===")

    bkg_bin_Vtx   = df_bkg_Vtx[df_bkg_Vtx["lxy_bin"]     == bin_label].copy()
    bkg_bin_NoVtx = df_bkg_NoVtx[df_bkg_NoVtx["lxy_bin"] == bin_label].copy()
    bkg_bin_OR    = df_bkg_OR[df_bkg_OR["lxy_bin"]        == bin_label].copy()
    print("Number of background events (Vtx): ", len(bkg_bin_Vtx))
    print("Number of background events (NoVtx): ", len(bkg_bin_NoVtx))
    print("Number of background events (OR): ", len(bkg_bin_OR))
    if len(bkg_bin_OR) < 100:
        print("Not enough background events, skipping")
        continue

    # Build combined dataset across all param points
    all_combined_Vtx, all_combined_NoVtx, all_combined_OR = [], [], []

    for ctau_val, mA_val, mpi_val in param_grid:
        print("Ctau = ", ctau_val, "mA = ", mA_val, "mpi = ", mpi_val)
        sig_bin_Vtx   = df_sig_Vtx[(df_sig_Vtx["param_ctau"]     == ctau_val) & (df_sig_Vtx["param_mA"]     == mA_val) & (df_sig_Vtx["param_mpi"]     == mpi_val) & (df_sig_Vtx["lxy_bin"]     == bin_label)].copy()
        sig_bin_NoVtx = df_sig_NoVtx[(df_sig_NoVtx["param_ctau"] == ctau_val) & (df_sig_NoVtx["param_mA"]   == mA_val) & (df_sig_NoVtx["param_mpi"]   == mpi_val) & (df_sig_NoVtx["lxy_bin"]   == bin_label)].copy()
        sig_bin_OR    = df_sig_OR[(df_sig_OR["param_ctau"]        == ctau_val) & (df_sig_OR["param_mA"]      == mA_val) & (df_sig_OR["param_mpi"]      == mpi_val) & (df_sig_OR["lxy_bin"]      == bin_label)].copy()
        print("Number of signal events (Vtx): ", len(sig_bin_Vtx))
        print("Number of signal events (NoVtx): ", len(sig_bin_NoVtx))
        print("Number of signal events (OR): ", len(sig_bin_OR))

        bkg_Vtx   = bkg_bin_Vtx.copy()
        bkg_Vtx["param_ctau"]   = float(ctau_val)
        bkg_Vtx["param_mA"]   = float(mA_val)
        bkg_Vtx["param_mpi"]   = float(mpi_val)

        bkg_NoVtx = bkg_bin_NoVtx.copy()
        bkg_NoVtx["param_ctau"] = float(ctau_val)
        bkg_NoVtx["param_mA"] = float(mA_val)
        bkg_NoVtx["param_mpi"] = float(mpi_val)

        bkg_OR    = bkg_bin_OR.copy()
        bkg_OR["param_ctau"]    = float(ctau_val)
        bkg_OR["param_mA"]    = float(mA_val)
        bkg_OR["param_mpi"]    = float(mpi_val)

        all_combined_Vtx.append(pd.concat([sig_bin_Vtx,   bkg_Vtx],   ignore_index=True))
        all_combined_NoVtx.append(pd.concat([sig_bin_NoVtx, bkg_NoVtx], ignore_index=True))
        all_combined_OR.append(pd.concat([sig_bin_OR,    bkg_OR],    ignore_index=True))

    df_combined_Vtx   = pd.concat(all_combined_Vtx,   ignore_index=True)
    df_combined_NoVtx = pd.concat(all_combined_NoVtx, ignore_index=True)
    df_combined_OR    = pd.concat(all_combined_OR,    ignore_index=True)

    X_Vtx,   y_Vtx   = df_combined_Vtx.drop(drop_cols,   axis=1), df_combined_Vtx["label"]
    X_NoVtx, y_NoVtx = df_combined_NoVtx.drop(drop_cols, axis=1), df_combined_NoVtx["label"]
    X_OR,    y_OR    = df_combined_OR.drop(drop_cols,    axis=1), df_combined_OR["label"]

    # After building df_combined_Vtx, df_combined_NoVtx, df_combined_OR,
    # and before train_test_split:
    w_Vtx   = compute_class_weights(y_Vtx.values)
    w_NoVtx = compute_class_weights(y_NoVtx.values)
    w_OR    = compute_class_weights(y_OR.values)

    X_train_Vtx,   X_test_Vtx,   y_train_Vtx,   y_test_Vtx,   w_train_Vtx,   w_test_Vtx   = train_test_split(X_Vtx,   y_Vtx,   w_Vtx,   test_size=0.3, random_state=42, stratify=y_Vtx)
    X_train_NoVtx, X_test_NoVtx, y_train_NoVtx, y_test_NoVtx, w_train_NoVtx, w_test_NoVtx = train_test_split(X_NoVtx, y_NoVtx, w_NoVtx, test_size=0.3, random_state=42, stratify=y_NoVtx)
    X_train_OR,    X_test_OR,    y_train_OR,    y_test_OR,    w_train_OR,    w_test_OR    = train_test_split(X_OR,    y_OR,    w_OR,    test_size=0.3, random_state=42, stratify=y_OR)

    bdt_Vtx   = XGBClassifier(n_estimators=100, max_depth=3, learning_rate=0.1, use_label_encoder=False, eval_metric="logloss", tree_method='hist', n_jobs=1)
    bdt_NoVtx = XGBClassifier(n_estimators=100, max_depth=3, learning_rate=0.1, use_label_encoder=False, eval_metric="logloss", tree_method='hist', n_jobs=1)
    bdt_OR    = XGBClassifier(n_estimators=100, max_depth=3, learning_rate=0.1, use_label_encoder=False, eval_metric="logloss", tree_method='hist', n_jobs=1)

    bdt_Vtx.fit(X_train_Vtx, y_train_Vtx, sample_weight=w_train_Vtx)
    bdt_NoVtx.fit(X_train_NoVtx, y_train_NoVtx, sample_weight=w_train_NoVtx)
    bdt_OR.fit(X_train_OR, y_train_OR, sample_weight=w_train_OR)

    # Feature importance: once per lxy bin
    for tag, bdt, X_bin in [("Vtx", bdt_Vtx, X_Vtx), ("NoVtx", bdt_NoVtx, X_NoVtx), ("OR", bdt_OR, X_OR)]:
        importances = bdt.feature_importances_
        sorted_idx  = np.argsort(importances)
        fig, ax = plt.subplots(figsize=(8, 10), constrained_layout=True)
        ax.barh(X_bin.columns[sorted_idx], importances[sorted_idx])
        ax.set_title(f"Feature Importance {tag} (Lxy={bin_label})")
        ax.tick_params(axis='y', labelsize=8)
        fig.savefig(f'curves_swap_even_CB_dropParams{model}/FeatImp_{tag}_lxy_{bin_label}.png', dpi=150, bbox_inches="tight")
        plt.close(fig)

    # ROC curves: one per param point
    for ctau_val, mA_val, mpi_val in param_grid:
        fpr_Vtx, tpr_Vtx, auc_Vtx     = None, None, None
        fpr_NoVtx, tpr_NoVtx, auc_NoVtx = None, None, None
        fpr_OR, tpr_OR, auc_OR         = None, None, None

        for tag, bdt, X_test, y_test, df_combined in [
            ("Vtx",   bdt_Vtx,   X_test_Vtx,   y_test_Vtx,   df_combined_Vtx.loc[X_test_Vtx.index]),
            ("NoVtx", bdt_NoVtx, X_test_NoVtx, y_test_NoVtx, df_combined_NoVtx.loc[X_test_NoVtx.index]),
            ("OR",    bdt_OR,    X_test_OR,    y_test_OR,    df_combined_OR.loc[X_test_OR.index]),
        ]:
            param_mask = (
                (df_combined["param_ctau"] == float(ctau_val)) &
                (df_combined["param_mA"]   == float(mA_val))   &
                (df_combined["param_mpi"]  == float(mpi_val))
            )
            X_eval = X_test[param_mask]
            y_eval = y_test[param_mask]

            if len(y_eval) < 10 or y_eval.nunique() < 2:
                print(f"  Skipping ROC for {tag} ctau={ctau_val} mA={mA_val} mpi={mpi_val} - not enough events")
                continue

            y_pred = bdt.predict_proba(X_eval)[:, 1]
            fpr, tpr, _ = roc_curve(y_eval, y_pred)
            auc = roc_auc_score(y_eval, y_pred)

            if tag == "Vtx":     fpr_Vtx,   tpr_Vtx,   auc_Vtx   = fpr, tpr, auc
            elif tag == "NoVtx": fpr_NoVtx, tpr_NoVtx, auc_NoVtx = fpr, tpr, auc
            elif tag == "OR":    fpr_OR,    tpr_OR,    auc_OR    = fpr, tpr, auc

        if any(x is None for x in [fpr_Vtx, fpr_NoVtx, fpr_OR]):
            continue

        fig, ax = plt.subplots(figsize=(6, 6), constrained_layout=True)
        ax.plot(fpr_Vtx,   tpr_Vtx,   label=f'Vtx (AUC={auc_Vtx:.3f})')
        ax.plot(fpr_NoVtx, tpr_NoVtx, label=f'NoVtx (AUC={auc_NoVtx:.3f})')
        ax.plot(fpr_OR,    tpr_OR,    label=f'OR (AUC={auc_OR:.3f})')
        ax.plot([0, 1], [0, 1], 'k--', alpha=0.5)
        ax.set_xlabel("False Positive Rate")
        ax.set_ylabel("True Positive Rate")
        ax.set_title(f"ROC Curve (ctau={ctau_val}mm, mA={mA_val}, mpi={mpi_val}, Lxy={bin_label})")
        ax.legend(loc="lower right")
        fig.savefig(f'curves_swap_even_CB_dropParams{model}/ROC_ctau_{ctau_val}_mA{mA_map[mA_val]}_mpi{mpi_val}_lxy_{bin_label}.png', dpi=150, bbox_inches="tight")
        plt.close(fig)