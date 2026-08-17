[[Decision tree]] [[Random forest]] [[binary classification]] [[multiclass classification]] [[supervised learning]] [[Gradient boosting]] [[scikitlearn]]

# ML Classifiers

> Algorithms that assign **discrete class labels** from features — pick by data size, interpretability, imbalance, and latency — **scikit-learn classifier zoo**.

```txt
        ML Classifiers ──┬── Interview
               ├── Sources
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Interview Relevance
- **Interview probes:** Interviewers ask about ML Classifiers to check whether you can choose models/…

## Sources
- [scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html) — deep-dive
- [Google Machine Learning Crash Course](https://developers.google.com/machine-learning/crash-course) — overview

## Technical Details
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
3. Metric aligned to cost ([[binary classification]] PR-AUC versus accuracy).
4. Persist with `joblib` + training data hash + schema version.

## Mistakes to Avoid
> [!WARNING]
> **Accuracy on imbalanced data** — report precision/recall/F1 or PR-AUC per class.

> [!WARNING]
> **One-hot high cardinality** — tree models may memorize categories; target encoding with CV only.

| Symptom | Check | Fix |
|---------|-------|-----|
| All one class predicted | Imbalance, bad threshold | `class_weight`; tune threshold |
| Great offline, bad online | Train/serve skew | Feature parity tests |
| Slow inference | Forest depth, k-NN | Reduce trees; distill to logistic |
| Unstable feature importances | Correlated features | [[Random forest]] impurity vs SHAP |
| High variance across CV folds | Small data | Simpler model; collect more labels |

## Pros/Cons or Trade-offs
- **Continuous target** — [[regression]].
- **Ordered ratings** — [[ordinal classification]].
- **Search ranking**
