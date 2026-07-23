[[Random forest]] [[Gradient boosting]] [[xg boost]] [[Decision tree]] [[Visualization/Residual plot]]

# Feature importance

> Quantify which inputs drive predictions — impurity/Gain (trees), coefficients (linear), SHAP (model-agnostic) — **interpretability vs correctness tradeoffs**.

---

## Mental model

"Importance" is **not one number** — definition depends on method:

```txt
Tree impurity decrease  → fast, biased toward high-cardinality features
Permutation importance  → shuffle column, measure metric drop (model-agnostic)
SHAP values             → additive fair attribution (costly)
Linear |β|              → only if features scaled comparably
```

Use importance for **debugging and prioritization**, not legal causality without domain review.

| Method | Pros | Cons |
|--------|------|------|
| `feature_importances_` (RF/GBDT) | Built-in | Correlated features split credit |
| `permutation_importance` | Any estimator | Slow; needs val set |
| SHAP | Consistent local/global | Compute; approximate on large data |

---

## Standard config / commands

### XGBoost / sklearn tree built-in

```python
import matplotlib.pyplot as plt
from sklearn.inspection import permutation_importance

# XGBoost
import xgboost as xgb
xgb.plot_importance(model, max_num_features=15)
plt.tight_layout()
plt.show()

# sklearn RF — impurity-based
importances = clf.feature_importances_
```

### Permutation (preferred for honest ranking)

```python
result = permutation_importance(
    pipe, X_val, y_val, n_repeats=10, random_state=42, scoring="roc_auc"
)
for name, imp in sorted(zip(feature_names, result.importances_mean), key=lambda x: -x[1])[:10]:
    print(f"{name}: {imp:.4f}")
```

### SHAP (tree explainer)

```python
import shap
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_sample)
shap.summary_plot(shap_values, X_sample, feature_names=feature_names)
```

Fit importance on **validation** data the model didn't train on.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| One-hot column tops chart | Cardinality bias | Group categories; permutation/SHAP |
| Importance contradicts domain | Leakage feature | Audit pipeline; drop suspect cols |
| SHAP slow | Full dataset | Sample 1k–5k rows |
| All near zero | Wrong scoring metric | Match business metric in permutation |
| Train vs val importance differs | Overfit | Compare on held-out only |

---

## Gotchas

> [!WARNING]
> **High-cardinality categoricals** inflate tree impurity importance — don't trust raw `feature_importances_` alone.

> [!WARNING]
> **Correlated features** — importance splits between twins; joint removal test beats per-feature rank.

---

## When NOT to use

- **Regulatory causal claims** — importance ≠ causal effect; run proper experiments.
- **Production monitoring** — track **feature distribution drift**, not static importance charts.
- **Deep vision/NLP** — use saliency/attention/LLM explainers, not tabular impurity.

---

## Related

[[Random forest]] · [[Gradient boosting]] · [[xg boost]] · [[Decision tree]] · [[data preprocessing]]
