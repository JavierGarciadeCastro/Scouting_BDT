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


model = 'A'

ctau_map = {1: "1", 10: "10", 100: "100"}
mA_map   = {0.40: "0p40", 2.0: "2p0"}
mpi_map  = {4: "4", 10: "10"}

def get_filename(model, ctau, mA, mpi):
    if model == 'A':
        return f"signal_A_ctau_{ctau_map[ctau]}mm_mA_{mA_map[mA]}_mpi_{mpi_map[mpi]}.root"
    elif model == 'B':
        return f"signal_B_ctau_{ctau_map[ctau]}mm_mA_{mA_map[mA]}_mpi_{mpi_map[mpi]}.root"

QCD_50to80   = 'QCD50to80.root'
QCD_80to120  = 'QCD80to120.root'
QCD_120to170 = 'QCD120to170.root'


def build_dataframe(filename, label, collection, ctau_val=None, mA_val=None, mpi_val=None):
    """
    Build a dataframe from a ROOT file.

    If label == 1 (signal), ctau_val/mA_val/mpi_val are the true parameters.
    If label == 0 (background), ctau_val/mA_val/mpi_val should be None;
    random parameters from the available grid will be assigned per event.
    """
    file = uproot.open(root_output / filename)
    tree = file["tout"]

    def max_or_default(array, default=0):
        return ak.to_numpy(ak.fill_none(ak.max(array, axis=1), default))

    branches = tree.keys()
    data = {}

    if collection == 'Vtx':
        prefix = "_Vtx"
    elif collection == 'NoVtx':
        prefix = "_NoVtx"

    sv_vars = ["chi2","prob","lxy","global","dphi","pt","3Dangle","L3D", "xErr","yErr","zErr","mu1","mu2","ndof"]
    mu_vars = ["pt","eta","phi","isGlobal","isTracker","chi2Ndof", "trk_dxy","trk_dxyError"]

    # ================= SV variables =================
    for sv in [1, 2]:
        for var in sv_vars:
            name = f"SV{sv}_{var}{prefix}"
            if name in branches:
                data[name] = max_or_default(tree[name].array())

    # ================= Muon variables =================
    for mu in [1, 2, 3, 4]:
        for var in mu_vars:
            name = f"mu{mu}_{var}{prefix}"
            if name in branches:
                data[name] = max_or_default(tree[name].array())

    df = pd.DataFrame(data)
    n_events = len(df)

    # ================= SV swap (sort by probability) =================
    swap = df[f"SV2_prob{prefix}"] > df[f"SV1_prob{prefix}"]
    for var in sv_vars:
        sv1 = f"SV1_{var}{prefix}"
        sv2 = f"SV2_{var}{prefix}"
        if sv1 in df.columns and sv2 in df.columns:
            a = df[sv1].copy()
            b = df[sv2].copy()
            df[sv1] = np.where(swap, b, a)
            df[sv2] = np.where(swap, a, b)

    if label == 1:
        df["param_ctau"] = float(ctau_val)
        df["param_mA"]   = float(mA_val)
        df["param_mpi"]  = float(mpi_val)
    else:
        rng = np.random.default_rng(seed=42)
        df["param_ctau"] = rng.choice(ctau_values,  size=n_events).astype(float)
        df["param_mA"]   = rng.choice(mA_values,    size=n_events).astype(float)
        df["param_mpi"]  = rng.choice(mpi_values,   size=n_events).astype(float)

    df["label"] = label

    return df
def build_OR_dataframe(df_Vtx, df_NoVtx, prefix_vtx="_Vtx", prefix_novtx="_NoVtx"):
    n = len(df_Vtx)
    lxy_vtx = df_Vtx[f"SV1_lxy{prefix_vtx}"].values
    lxy_novtx = df_NoVtx[f"SV1_lxy{prefix_novtx}"].values
    pt_vtx = df_Vtx[f"SV1_pt{prefix_vtx}"].values
    pt_novtx = df_NoVtx[f"SV1_pt{prefix_novtx}"].values

    use_vtx_sv = (lxy_vtx > 0)
    sv_matched = use_vtx_sv & (np.abs(lxy_vtx - lxy_novtx) < 0.1) & (np.abs(pt_vtx - pt_novtx) < 0.1)

    result = {}
    sv_vars = ["chi2","prob","lxy","global","dphi","pt","3Dangle","L3D","xErr","yErr","zErr","mu1","mu2","ndof"]
    for sv in [1, 2]:
        for var in sv_vars:
            vtx_col = f"SV{sv}_{var}{prefix_vtx}"
            novtx_col = f"SV{sv}_{var}{prefix_novtx}"
            if vtx_col in df_Vtx.columns and novtx_col in df_NoVtx.columns:
                result[f"SV{sv}_{var}"] = np.where(use_vtx_sv, df_Vtx[vtx_col].values, df_NoVtx[novtx_col].values)

    mu_vars = ["pt","eta","phi","isGlobal","isTracker","chi2Ndof","trk_dxy","trk_dxyError"]

    mu_eta_vtx = np.stack([df_Vtx[f"mu{i}_eta{prefix_vtx}"].values for i in range(1,5)], axis=1)
    mu_phi_vtx = np.stack([df_Vtx[f"mu{i}_phi{prefix_vtx}"].values for i in range(1,5)], axis=1)
    mu_pt_vtx  = np.stack([df_Vtx[f"mu{i}_pt{prefix_vtx}"].values for i in range(1,5)], axis=1)

    mu_eta_novtx = np.stack([df_NoVtx[f"mu{i}_eta{prefix_novtx}"].values for i in range(1,5)], axis=1)
    mu_phi_novtx = np.stack([df_NoVtx[f"mu{i}_phi{prefix_novtx}"].values for i in range(1,5)], axis=1)
    mu_pt_novtx  = np.stack([df_NoVtx[f"mu{i}_pt{prefix_novtx}"].values for i in range(1,5)], axis=1)

    matched_novtx = np.zeros((n, 4), dtype=bool)
    for vi in range(4):
        for ni in range(4):
            deta = mu_eta_vtx[:, vi] - mu_eta_novtx[:, ni]
            dphi = (mu_phi_vtx[:, vi] - mu_phi_novtx[:, ni] + np.pi) % (2*np.pi) - np.pi
            dR = np.sqrt(deta**2 + dphi**2)
            has_vtx_mu = mu_pt_vtx[:, vi] > 0
            matched_novtx[:, ni] |= (has_vtx_mu & (dR < 0.1))

    unmatched_novtx = (mu_pt_novtx > 0) & ~matched_novtx

    n_vtx_muons = (mu_pt_vtx > 0).sum(axis=1)

    for vi in range(4):
        vtx_col_exists = mu_pt_vtx[:, vi] > 0
        for var in mu_vars:
            vtx_vals = df_Vtx[f"mu{vi+1}_{var}{prefix_vtx}"].values
            novtx_vals = df_NoVtx[f"mu{vi+1}_{var}{prefix_novtx}"].values
            result[f"mu{vi+1}_{var}"] = np.where(vtx_col_exists, vtx_vals, 0.0)

    slot = np.zeros(n, dtype=int)
    for ni in range(4):
        is_unmatched = unmatched_novtx[:, ni]
        target_slot = n_vtx_muons + slot
        for s in range(4):
            mask = is_unmatched & (target_slot == s)
            if not mask.any():
                continue
            for var in mu_vars:
                novtx_vals = df_NoVtx[f"mu{ni+1}_{var}{prefix_novtx}"].values
                current = result[f"mu{s+1}_{var}"]
                result[f"mu{s+1}_{var}"] = np.where(mask, novtx_vals, current)
        slot += is_unmatched.astype(int)

    result["label"] = df_Vtx["label"].values

    for col in ["param_ctau", "param_mA", "param_mpi"]:
        if col in df_Vtx.columns:
            result[col] = df_Vtx[col].values

    df_OR = pd.DataFrame(result)
    return df_OR


print('Preparing signal dataframe...')

mass_points = [(0.40, 4), (2.0, 10)]

all_sig_Vtx = []
all_sig_NoVtx = []
for c in ctau_values:
    for m, mp in mass_points:
        f = get_filename(model, c, m, mp)
        all_sig_Vtx.append(build_dataframe(f, 1, 'Vtx', c, m, mp))
        all_sig_NoVtx.append(build_dataframe(f, 1, 'NoVtx', c, m, mp))

df_sig_Vtx = pd.concat(all_sig_Vtx, ignore_index=True)
df_sig_NoVtx = pd.concat(all_sig_NoVtx, ignore_index=True)

print('Preparing background dataframe...')
df_QCD_50to80_Vtx    = build_dataframe(QCD_50to80,   0, 'Vtx')
df_QCD_50to80_NoVtx  = build_dataframe(QCD_50to80,   0, 'NoVtx')
df_QCD_80to120_Vtx   = build_dataframe(QCD_80to120,  0, 'Vtx')
df_QCD_80to120_NoVtx = build_dataframe(QCD_80to120,  0, 'NoVtx')
df_QCD_120to170_Vtx  = build_dataframe(QCD_120to170, 0, 'Vtx')
df_QCD_120to170_NoVtx= build_dataframe(QCD_120to170, 0, 'NoVtx')

df_bkg_Vtx = pd.concat([df_QCD_50to80_Vtx, df_QCD_80to120_Vtx, df_QCD_120to170_Vtx], ignore_index=True)
df_bkg_NoVtx = pd.concat([df_QCD_50to80_NoVtx, df_QCD_80to120_NoVtx, df_QCD_120to170_NoVtx], ignore_index=True)


df_sig_OR = build_OR_dataframe(df_sig_Vtx, df_sig_NoVtx)
df_bkg_OR = build_OR_dataframe(df_bkg_Vtx, df_bkg_NoVtx)


df_Vtx = pd.concat([df_sig_Vtx,   df_bkg_Vtx],   ignore_index=True)
df_NoVtx = pd.concat([df_sig_NoVtx, df_bkg_NoVtx], ignore_index=True)
df_OR = pd.concat([df_sig_OR,    df_bkg_OR],     ignore_index=True)

lxy_bins   = [0.0, 0.2, 1.0, 2.4, 3.1, 7.0, 11.0, 16.0, 70.0]
lxy_labels = ["0p0to0p2","0p2to1p0","1p0to2p4","2p4to3p1", "3p1to7p0","7p0to11p0","11p0to16p0","16p0to70p0"]

df_Vtx["lxy_bin"] = pd.cut(df_Vtx["SV1_lxy_Vtx"], bins=lxy_bins, labels=lxy_labels, include_lowest=True)
df_NoVtx["lxy_bin"] = pd.cut(df_NoVtx["SV1_lxy_NoVtx"], bins=lxy_bins, labels=lxy_labels, include_lowest=True)
df_OR["lxy_bin"] = pd.cut(df_OR["SV1_lxy"], bins=lxy_bins, labels=lxy_labels, include_lowest=True)

print(df_sig_OR.columns.tolist())

#cut_signal1A = {
#    1: {"0p0to0p2": (0.026, 0.897),"0p2to1p0": (0.413, 0.749),"1p0to2p4": (0.564, 0.677),"2p4to3p1": (0.636, 0.706),"3p1to7p0": (0.705, 0.746),"7p0to11p0": (0.760, 0.902),"11p0to16p0": (0.639, 0.925),"16p0to70p0": (0.301, 0.969)},
#    10: {"0p0to0p2": (0.141, 0.897),"0p2to1p0": (0.473, 0.749),"1p0to2p4": (0.653, 0.677),"2p4to3p1": (0.717, 0.706),"3p1to7p0": (0.756, 0.746),"7p0to11p0": (0.767, 0.902),"11p0to16p0": (0.647, 0.925),"16p0to70p0": (0.320, 0.969)},
#    100: {"0p0to0p2": (0.313, 0.897),"0p2to1p0": (0.474, 0.749),"1p0to2p4": (0.633, 0.677),"2p4to3p1": (0.695, 0.706),"3p1to7p0": (0.704, 0.746),"7p0to11p0": (0.633, 0.902),"11p0to16p0": (0.450, 0.925),"16p0to70p0": (0.127, 0.969)}
#}

for bin_label in lxy_labels:

    print(f"\n=== Lxy bin: {bin_label} ===")

    df_bin_Vtx = df_Vtx[df_Vtx["lxy_bin"] == bin_label].copy()
    df_bin_NoVtx = df_NoVtx[df_NoVtx["lxy_bin"] == bin_label].copy()
    df_bin_OR = df_OR[df_OR["lxy_bin"] == bin_label].copy()

    print("Vtx events: ", len(df_bin_Vtx))
    print("NoVtx events: ", len(df_bin_NoVtx))
    print("OR events: ", len(df_bin_OR))

    if len(df_bin_Vtx) < 100 or len(df_bin_NoVtx) < 100:
        print("Not enough events, skipping")
        continue

    drop_cols = ["label", "lxy_bin", "param_ctau", "param_mA", "param_mpi"]
    

    X_Vtx_bin = df_bin_Vtx.drop(drop_cols, axis=1)
    y_Vtx_bin = df_bin_Vtx["label"]
    params_Vtx  = df_bin_Vtx[["param_ctau", "param_mA", "param_mpi"]]

    X_NoVtx_bin = df_bin_NoVtx.drop(drop_cols, axis=1)
    y_NoVtx_bin = df_bin_NoVtx["label"]
    params_NoVtx = df_bin_NoVtx[["param_ctau", "param_mA", "param_mpi"]]

    X_OR_bin = df_bin_OR.drop(drop_cols, axis=1)
    y_OR_bin = df_bin_OR["label"]
    params_OR = df_bin_OR[["param_ctau", "param_mA", "param_mpi"]]

    X_train_Vtx, X_test_Vtx, y_train_Vtx, y_test_Vtx = train_test_split(X_Vtx_bin, y_Vtx_bin, test_size=0.3, random_state=42, stratify=y_Vtx_bin)
    X_train_NoVtx, X_test_NoVtx, y_train_NoVtx, y_test_NoVtx = train_test_split(X_NoVtx_bin, y_NoVtx_bin, test_size=0.3, random_state=42, stratify=y_NoVtx_bin)
    X_train_OR, X_test_OR, y_train_OR, y_test_OR = train_test_split(X_OR_bin, y_OR_bin, test_size=0.3, random_state=42, stratify=y_OR_bin)

    params_test_Vtx   = params_Vtx.loc[X_test_Vtx.index]
    params_test_NoVtx = params_NoVtx.loc[X_test_NoVtx.index]
    params_test_OR    = params_OR.loc[X_test_OR.index]

    bdt_Vtx = XGBClassifier(n_estimators=100, max_depth=3, learning_rate=0.1, use_label_encoder=False, eval_metric="logloss", tree_method='hist', n_jobs=1)
    bdt_NoVtx = XGBClassifier(n_estimators=100, max_depth=3, learning_rate=0.1, use_label_encoder=False, eval_metric="logloss", tree_method='hist', n_jobs=1)
    bdt_OR = XGBClassifier(n_estimators=100, max_depth=3, learning_rate=0.1, use_label_encoder=False, eval_metric="logloss", tree_method='hist', n_jobs=1)

    bdt_Vtx.fit(X_train_Vtx, y_train_Vtx)
    bdt_NoVtx.fit(X_train_NoVtx, y_train_NoVtx)
    bdt_OR.fit(X_train_OR, y_train_OR)

    for c in ctau_values:
        for m, mp in mass_points:
            for collection, bdt, X_test, y_test, params_test in [("Vtx", bdt_Vtx, X_test_Vtx, y_test_Vtx, params_test_Vtx), ("NoVtx", bdt_NoVtx, X_test_NoVtx, y_test_NoVtx, params_test_NoVtx), ("OR", bdt_OR, X_test_OR, y_test_OR, params_test_OR)]:
                sig_mask = (params_test["param_ctau"] == float(c)) & (params_test["param_mA"] == float(m)) & (params_test["param_mpi"] == float(mp))
                bkg_mask = y_test == 0
                eval_mask = sig_mask | bkg_mask
                X_eval = X_test[eval_mask]
                y_eval = y_test[eval_mask]
                y_pred = bdt.predict_proba(X_eval)[:, 1]
                fpr, tpr, _ = roc_curve(y_eval, y_pred)
                auc = roc_auc_score(y_eval, y_pred)

                if collection == "Vtx":
                    fpr_Vtx, tpr_Vtx, auc_Vtx = fpr, tpr, auc
                elif collection == "NoVtx":
                    fpr_NoVtx, tpr_NoVtx, auc_NoVtx = fpr, tpr, auc
                elif collection == "OR":
                    fpr_OR, tpr_OR, auc_OR = fpr, tpr, auc

            fig, ax = plt.subplots(figsize=(6, 6), constrained_layout=True)
            ax.plot(fpr_Vtx, tpr_Vtx, label=f'Vtx (AUC = {auc_Vtx:.3f})')
            ax.plot(fpr_NoVtx, tpr_NoVtx, label=f'NoVtx (AUC = {auc_NoVtx:.3f})')
            ax.plot(fpr_OR, tpr_OR, label=f'OR (AUC = {auc_OR:.3f})')
            ax.plot([0, 1], [0, 1], 'k--', alpha=0.5)
            #sig_eff, bkg_rej = cut_signal1A[c][bin_label]
            #ax.scatter(1 - bkg_rej, sig_eff, color='red', s=60, label='Cut and Count', zorder=5)
            ax.set_xlabel("False Positive Rate")
            ax.set_ylabel("True Positive Rate")
            ax.set_title(f"ROC Curve (ctau={c}mm, mA={m}, mpi={mp}, Lxy={bin_label})")
            ax.legend(loc="lower right")
            fig.savefig(f'curves_param_{model}/ROC_ctau_{c}_mA{mA_map[m]}_mpi{mp}_lxy_{bin_label}_log.png', dpi=150, bbox_inches="tight")
            plt.close(fig)

    for tag, bdt, X_bin in [("Vtx", bdt_Vtx, X_Vtx_bin), ("NoVtx", bdt_NoVtx, X_NoVtx_bin), ("OR", bdt_OR, X_OR_bin)]:
        importances = bdt.feature_importances_
        feat_names  = X_bin.columns
        sorted_idx  = np.argsort(importances)
        fig, ax = plt.subplots(figsize=(8, 10), constrained_layout=True)
        ax.barh(feat_names[sorted_idx], importances[sorted_idx])
        ax.set_xlabel(f"Feature importance ({tag})")
        ax.set_ylabel("Variable")
        ax.set_title(f"Feature Importance {tag} (Lxy={bin_label})")
        ax.tick_params(axis='y', labelsize=8)
        fig.savefig(f'curves_param_{model}/FeatImp_{tag}_lxy_{bin_label}.png', dpi=150, bbox_inches="tight")
        plt.close(fig)