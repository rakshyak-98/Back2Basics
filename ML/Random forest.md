[[Decision tree]] [[Gradient boosting]] [[xg boost]] [[scikitlearn]] [[ML Classifiers]]

# Random forest

> Bagged ensemble of decorrelated [[Decision tree]]s — vote (classify) or average (regress) — **Breiman (2001)**; strong default before boosting tuning.

---

## Mental model

```txt
For b = 1..B:
  1. Bootstrap sample of rows (with replacement)
  2. At each split, consider random subset of features (m ≈ √p classify, p/3 regress)
  3. Grow tree to full depth (or limited) — no pruning per tree
Predict: majority vote / mean of tree outputs
```

**Why it works:** individual trees overfit; averaging **uncorrelated** errors reduces variance without heavy bias increase. Random feature subsampling at splits decorrelates trees beyond bagging alone.

**OOB (out-of-bag):** ~37% of rows left out per tree → free validation estimate without holdout set.

```txt
Variance ↓  (ensemble)
Bias ~      (deep trees)
Speed ↑     (embarrassingly parallel fit + predict)
```

---

## Standard config / commands

### Classification

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV

clf = RandomForestClassifier(
    n_estimators=300,        # more trees → stabler; diminishing returns ~500+
    max_depth=None,          # trees grow until pure/leaves min — often OK for RF
    min_samples_leaf=5,
    max_features="sqrt",     # default for classification
    class_weight="balanced_subsample",  # per bootstrap sample
    n_jobs=-1,
    random_state=42,
    oob_score=True,
)
clf.fit(X_train, y_train)
print(clf.oob_score_)
```

### Regression

```python
from sklearn.ensemble import RandomForestRegressor

reg = RandomForestRegressor(
    n_estimators=500,
    max_features=0.33,       # or "sqrt" / log2
    min_samples_leaf=3,
    n_jobs=-1,
)
```

### Feature importance (use with caution)

```python
import pandas as pd

imp = pd.Series(clf.feature_importances_, index=X.columns).sort_values(ascending=False)
# Prefer permutation importance for correlated features:
from sklearn.inspection import permutation_importance
pi = permutation_importance(clf, X_val, y_val, n_repeats=10, random_state=42)
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| OOB good, val bad | Data shift / leakage in features | Audit temporal split; remove leaky cols |
| Barely beats single tree | Too few trees or correlated features | ↑ `n_estimators`; tune `max_features` |
| Memory blowup on fit | `n_estimators` × deep trees × wide data | Limit depth; `max_samples`; subsample rows |
| Slow inference | Hundreds of deep trees | Reduce trees; [[Gradient boosting]] with fewer deeper stages; treelite |
| Importance ranks nonsense | Correlated features | Permutation importance; SHAP |
| Class imbalance ignored | Default majority vote | `class_weight`; stratified bootstrap |

---

## Gotchas

> [!WARNING]
> **Extrapolation (regression):** same as trees — predictions plateau outside training range.

> [!WARNING]
> **High-cardinality categoricals:** sklearn needs encoding; consider CatBoost/LightGBM for native categoricals.

> [!WARNING]
> **Probability calibration:** vote fractions ≠ calibrated probs — use `CalibratedClassifierCV` if thresholds matter.

> [!WARNING]
> **Time series:** i.i.d. bootstrap breaks temporal structure — use blocked bootstrap or dedicated time-series models.

---

## When NOT to use

- **Need peak tabular accuracy** after tuning budget — [[Gradient boosting]] / [[xg boost]] usually wins Kaggle-style tabular.
- **Linear separable with sparse high-dim text** — linear models + hashing faster and simpler.
- **Strict latency (< few ms) on edge** — model size of hundreds of trees may exceed budget; linear or tiny NN.
- **Online learning** — full retrain required; not incremental.

---

## Related

[[Decision tree]] · [[Gradient boosting]] · [[xg boost]] · [[multiclass classification]] · [[binary classification]] · [[Visualization/feature importance]] · [[scikitlearn]]
