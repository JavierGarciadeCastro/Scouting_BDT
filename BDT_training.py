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

def build_dataframe(filename, label):
    import uproot
    import awkward as ak
    import pandas as pd
    import numpy as np

    file = uproot.open(root_output / filename)
    tree = file["tout"]

    n_events = tree.num_entries

    def max_or_default(array, default=0):
        return np.array([ak.max(a) if len(a) > 0 else default for a in array])

    df = pd.DataFrame({
        # NoVtx SV
        "SV_chi2_NoVtx": max_or_default(tree["SV_chi2_NoVtx"].array()),
        "SV_prob_NoVtx": max_or_default(tree["SV_prob_NoVtx"].array()),
        "SV_lxy_NoVtx": max_or_default(tree["SV_lxy_NoVtx"].array()),
        "SV_global_NoVtx": max_or_default(tree["SV_global_NoVtx"].array()),
        "SV_tracker_NoVtx": max_or_default(tree["SV_tracker_NoVtx"].array()),

        # NoVtx muons
        "mu_pt_NoVtx": max_or_default(tree["mu_pt_NoVtx"].array()),
        "mu_eta_NoVtx": max_or_default(tree["mu_eta_NoVtx"].array()),
        "mu_phi_NoVtx": max_or_default(tree["mu_phi_NoVtx"].array()),
        "mu_isGlobal_NoVtx": max_or_default(tree["mu_isGlobal_NoVtx"].array()),
        "mu_isTracker_NoVtx": max_or_default(tree["mu_isTracker_NoVtx"].array()),
        "mu_chi2Ndof_NoVtx": max_or_default(tree["mu_chi2Ndof_NoVtx"].array()),

        # Vtx SV
        "SV_chi2_Vtx": max_or_default(tree["SV_chi2_Vtx"].array()),
        "SV_prob_Vtx": max_or_default(tree["SV_prob_Vtx"].array()),
        "SV_lxy_Vtx": max_or_default(tree["SV_lxy_Vtx"].array()),
        "SV_global_Vtx": max_or_default(tree["SV_global_Vtx"].array()),
        "SV_tracker_Vtx": max_or_default(tree["SV_tracker_Vtx"].array()),

        # Vtx muons
        "mu_pt_Vtx": max_or_default(tree["mu_pt_Vtx"].array()),
        "mu_eta_Vtx": max_or_default(tree["mu_eta_Vtx"].array()),
        "mu_phi_Vtx": max_or_default(tree["mu_phi_Vtx"].array()),
        "mu_isGlobal_Vtx": max_or_default(tree["mu_isGlobal_Vtx"].array()),
        "mu_isTracker_Vtx": max_or_default(tree["mu_isTracker_Vtx"].array()),
        "mu_chi2Ndof_Vtx": max_or_default(tree["mu_chi2Ndof_Vtx"].array()),

        "label": label
    })

    return df

df_sig = build_dataframe("signal.root", 1)
df_bkg = build_dataframe("bkg.root", 0)

df = pd.concat([df_sig, df_bkg], ignore_index=True)
print(df.head())


X = df.drop("label", axis=1)
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

bdt = XGBClassifier(
    n_estimators=100,
    max_depth=3,
    learning_rate=0.1,
    use_label_encoder=False,
    eval_metric='logloss'
)

bdt.fit(X_train, y_train)

y_pred = bdt.predict(X_test)
y_pred_prob = bdt.predict_proba(X_test)[:,1]

print("Accuracy:", accuracy_score(y_test, y_pred))
print("ROC AUC:", roc_auc_score(y_test, y_pred_prob))


fpr, tpr, thresholds = roc_curve(y_test, y_pred_prob)

plt.style.use(mplhep.style.CMS)
plt.figure(figsize=(6,6))
plt.plot(fpr, tpr, label=f'BDT (AUC = {roc_auc_score(y_test, y_pred_prob):.3f})')
plt.plot([0,1],[0,1],'k--', alpha=0.5)
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve")
plt.legend()
plt.savefig('ROC_curve.png')

importances = bdt.feature_importances_
feat_names = X.columns

plt.figure(figsize=(8,6))
plt.barh(feat_names, importances)
plt.xlabel("Feature importance")
plt.ylabel("Variable")
plt.title("XGBoost Feature Importance")
plt.savefig('Feature_Importance.png')