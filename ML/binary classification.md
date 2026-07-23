[[multiclass classification]] [[sigmoid]] [[ML Classifiers]] [[scikitlearn]] [[Mean Average Precision (MAP)]]

# Binary classification

> Predict one of two labels (spam/ham, fraud/legit) — optimize threshold on **precision/recall tradeoff**, not raw accuracy — **Hastie, Tibshirani, Friedman (ESL)**.

---

## Mental model

Output is usually **P(y=1 | x)** ∈ [0,1] from [[sigmoid]] (logistic) or margin score from [[Model/support vector machines (SVM)]]. You pick a **decision threshold** (default 0.5) to emit class 1 vs 0.

```txt
score(x) → probability p → if p ≥ τ then positive else negative
```

Imbalanced data (1% fraud): 99% accuracy by predicting all negatives — useless. Track **ROC-AUC**, **PR-AUC**, **F1**, **calibration**, and **cost-sensitive** metrics tied to business harm.

| Metric | When it matters |
|--------|-----------------|
| **ROC-AUC** | Rank quality; less sensitive to prevalence |
| **PR-AUC** | Heavy imbalance; focuses on positives |
| **F1** | Balance precision/recall for single threshold |
| **Brier / calibration** | Probabilities used for pricing or routing |

---

## Standard config / commands

```python
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import (
    classification_report, roc_auc_score, average_precision_score,
    precision_recall_curve,
)
from sklearn.calibration import CalibratedClassifierCV

clf = LogisticRegression(max_iter=1000, class_weight="balanced")  # ↑ recall on minority
clf.fit(X_train, y_train)

proba = clf.predict_proba(X_test)[:, 1]
print("ROC-AUC:", roc_auc_score(y_test, proba))
print("PR-AUC:", average_precision_score(y_test, proba))

# Tune threshold for target precision
prec, rec, thresh = precision_recall_curve(y_test, proba)
# pick τ where prec >= 0.95 for fraud review queue
```

### XGBoost binary (common production default)

```python
import xgboost as xgb
model = xgb.XGBClassifier(
    objective="binary:logistic",
    scale_pos_weight=(y_train == 0).sum() / (y_train == 1).sum(),  # imbalance knob
    eval_metric="aucpr",
)
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| High accuracy, bad business outcome | Class balance, threshold | PR-AUC; tune τ; `class_weight` / `scale_pos_weight` |
| Model always predicts negative | Prevalence, features, leakage | SMOTE (careful); better features; check label definition |
| Probabilities look wrong | Calibration plot | Platt / isotonic via `CalibratedClassifierCV` |
| Train AUC 1.0, prod collapse | Target leakage, temporal split | Time-based split; remove post-outcome features |
| Different results per run | Random seed, data order | Set seeds; stratified CV |

---

## Gotchas

> [!WARNING]
> **Default 0.5 threshold** is rarely optimal when false negatives cost 100× false positives (medical, fraud).

> [!WARNING]
> **Accuracy on imbalanced data** is a vanity metric in design reviews.

---

## When NOT to use

- **More than two unordered classes** — [[multiclass classification]].
- **Ordered labels** (low/medium/high) — [[ordinal classification]].
- **Ranking/search quality** — [[Mean Average Precision (MAP)]] / [[Normalized Discounted Cumulative Gain (NDCG)]].

---

## Related

[[multiclass classification]] · [[sigmoid]] · [[Decision tree]] · [[Gradient boosting]] · [[Visualization/Residual plot]] · [[data preprocessing]]
