[[Gradient boosting]] [[Random forest]] [[Decision tree]] [[scikitlearn]] [[binary classification]]

# XGBoost

> Optimized distributed GBDT — histogram splits, regularized leaf weights, sparsity-aware — **Chen & Guestrin**; default for production tabular ML at scale.

---

## Mental model

XGBoost = [[Gradient boosting]] + engineering:

```txt
Obj = Σ loss(yᵢ, ŷᵢ) + Σ Ω(tree_k)
Ω = γ·(# leaves) + ½λ·Σwⱼ²     # penalize complex trees
```

**Second-order approximation:** uses gradient **and** Hessian for faster, stabler splits.

**Histogram algorithm:** bin continuous features → O(#bins) split search vs exact sort — huge win on wide data.

**Sparsity:** learns default direction for missing values per split — no impute required (but document missing semantics).

**Distributed:** DMatrix + column blocks; multi-GPU / cluster via `xgboost.dtrain` patterns or Spark XGBoost.

---

## Standard config / commands

### Python (native API)

```python
import xgboost as xgb
from sklearn.model_selection import train_test_split

X_tr, X_val, y_tr, y_val = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
dtrain = xgb.DMatrix(X_tr, label=y_tr, feature_names=list(X.columns))
dval = xgb.DMatrix(X_val, label=y_val, feature_names=list(X.columns))

params = {
    "objective": "binary:logistic",   # multi:softprob, reg:squarederror
    "eval_metric": "auc",
    "max_depth": 6,
    "eta": 0.05,                      # learning_rate
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "min_child_weight": 5,
    "lambda": 1.0,                    # L2 on leaf weights
    "alpha": 0.0,                     # L1
    "tree_method": "hist",            # default on recent builds
    "seed": 42,
}

bst = xgb.train(
    params,
    dtrain,
    num_boost_round=3000,
    evals=[(dtrain, "train"), (dval, "val")],
    early_stopping_rounds=50,
    verbose_eval=100,
)
```

### sklearn wrapper

```python
from xgboost import XGBClassifier

clf = XGBClassifier(
    n_estimators=2000,
    learning_rate=0.05,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    early_stopping_rounds=50,
    eval_metric="auc",
    tree_method="hist",
)
clf.fit(X_tr, y_tr, eval_set=[(X_val, y_val)], verbose=100)
```

### Imbalanced binary

```python
scale = (y == 0).sum() / (y == 1).sum()
params["scale_pos_weight"] = scale
```

### Save / serve

```python
bst.save_model("model.json")          # JSON — portable
# bst.save_model("model.ubj")         # binary, faster load
loaded = xgb.Booster()
loaded.load_model("model.json")
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `Check failed: label must be 0..K-1` | Non-contiguous labels | `LabelEncoder`; verify objective matches K |
| GPU OOM | `tree_method=gpu_hist`, huge data | Subsample; `max_bin`; CPU hist |
| Early stop at round 1 | Wrong eval metric / bad DMatrix | Match metric to objective; verify feature types |
| Worse than LightGBM on categoricals | One-hot explosion | Native cat in LightGBM/CatBoost; target encoding w/ CV |
| Different results same seed | Threading / data order | `seed`, `deterministic_histogram=1` (version-dependent) |
| Slow batch predict | Python loop over rows | `Booster.predict(DMatrix)` batch; Treelite/ONNX |

---

## Gotchas

> [!WARNING]
> **Version skew train vs serve:** XGBoost JSON models are not always forward-compatible across major versions — pin version in serving container.

> [!WARNING]
> **Leakage via target encoding** before CV — encode inside folds only.

> [!WARNING]
> **`early_stopping_rounds` in constructor vs `xgb.train`** — API differs between sklearn wrapper and native; read version docs.

> [!WARNING]
> **Overfitting with too many trees** even with early stop — also tune `min_child_weight`, `subsample`, `colsample_bytree`.

---

## When NOT to use

- **Small n, wide p with linear signal** — logistic + L1 may generalize with zero tuning.
- **Pure image/text/audio** — deep nets or pretrained embeddings dominate.
- **Need fully native categorical without encoding** — CatBoost often less pipeline work.
- **Regulatory mandate for linear interpretability** — use GAM/GLM with documented coefficients.

---

## Related

[[Gradient boosting]] · [[Random forest]] · [[Decision tree]] · [[multiclass classification]] · [[Model/Linear regression]] · [[scikitlearn]]
