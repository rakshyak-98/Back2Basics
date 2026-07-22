[[Decision tree]] [[Random forest]] [[binary classification]] [[multiclass classification]] [[supervised learning]]

# ML Classifiers

> Algorithms that assign **discrete class labels** from features — pick by data size, interpretability, imbalance, and latency — **scikit-learn classifier zoo**.

---

## Mental model

**Features** (predictors, X) → **classifier** → **predicted label** (target, y). All sklearn classifiers share `fit(X, y)` and `predict(X)`.

```txt
Features x₁…xₚ  →  f(x)  →  ŷ ∈ {classes}
```

| Family | Strength | Weakness |
|--------|----------|----------|
| **Logistic / linear** | Fast, interpretable | Linear boundaries |
| **[[Decision tree]]** | Rules, interactions | Overfits alone |
| **[[Random forest]]** | Strong default tabular | Heavy model size |
| **[[Gradient boosting]]** | Peak tabular accuracy | Tuning, train time |
| **[[Model/support vector machines (SVM)]]** | Small/medium, kernels | Poor on huge sparse |
| **k-NN** | No training | Slow predict, curse of dim |
| **[[ANN]]** | Images, text, huge data | Needs data + GPU |

**Target leakage:** any feature available only after the label is known must be dropped before training.

---

## Standard config / commands

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import cross_validate

candidates = {
    "logistic": LogisticRegression(max_iter=1000, class_weight="balanced"),
    "rf": RandomForestClassifier(n_estimators=300, class_weight="balanced", random_state=42),
}

for name, clf in candidates.items():
    pipe = Pipeline([("prep", preprocess), ("clf", clf)])
    scores = cross_validate(pipe, X, y, cv=5, scoring=["f1_macro", "roc_auc"])
    print(name, scores["test_f1_macro"].mean())
```

### Production checklist

1. Stratified split (or time split for temporal data).
2. [[data preprocessing]] inside Pipeline.
3. Metric aligned to cost ([[binary classification]] PR-AUC vs accuracy).
4. Persist with `joblib` + training data hash + schema version.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| All one class predicted | Imbalance, bad threshold | `class_weight`; tune threshold |
| Great offline, bad online | Train/serve skew | Feature parity tests |
| Slow inference | Forest depth, k-NN | Reduce trees; distill to logistic |
| Unstable feature importances | Correlated features | [[Random forest]] impurity vs SHAP |
| High variance across CV folds | Small data | Simpler model; collect more labels |

---

## Gotchas

> [!WARNING]
> **Accuracy on imbalanced data** — report precision/recall/F1 or PR-AUC per class.

> [!WARNING]
> **One-hot high cardinality** — tree models may memorize categories; target encoding with CV only.

---

## When NOT to use

- **Continuous target** — [[regression]].
- **Ordered ratings** — [[ordinal classification]].
- **Search ranking** — learning-to-rank + [[Normalized Discounted Cumulative Gain (NDCG)]].

---

## Related

[[binary classification]] · [[multiclass classification]] · [[Decision tree]] · [[Random forest]] · [[Gradient boosting]] · [[scikitlearn]]
