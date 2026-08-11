[[binary classification]] [[ML Classifiers]] [[sigmoid]] [[scikitlearn]] [[Decision tree]]

# Multiclass classification

> Predict one label from **K > 2** classes — reduction strategies, metrics, and production pitfalls.

---

## Mental model

Binary classifiers naturally output one score; multiclass extends via:

```txt
One-vs-Rest (OvR):     K binary models — "class k vs all others"
One-vs-One (OvO):      K(K-1)/2 pairwise models — vote or aggregate
Softmax / multinomial: Single model, K outputs summing to 1 (logistic extension)
```

**Decision boundary view:** OvR creates K half-spaces; softmax learns coupled boundaries (preferred for linear/logistic when classes compete).

**Output types:**
- **Hard label:** argmax of scores
- **Probabilities:** must sum to 1 — calibrate if used for ranking or thresholds
- **Top-k:** return k highest classes (search, catalog)

**Imbalance:** macro vs micro vs weighted F1 — pick metric matching business cost (rare class recall vs overall accuracy).

---

## Standard config / commands

### sklearn strategies

```python
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
from sklearn.ensemble import RandomForestClassifier

# Native multiclass (softmax for LogisticRegression)
clf = LogisticRegression(max_iter=1000, multi_class="multinomial", solver="lbfgs")
clf.fit(X_train, y_train)
proba = clf.predict_proba(X_val)  # shape (n_samples, n_classes)

# OvR wrapper for binary-only base estimators
ovr = OneVsRestClassifier(RandomForestClassifier(n_estimators=200))
ovr.fit(X_train, y_train)
```

### Metrics (always report more than accuracy)

```python
from sklearn.metrics import classification_report, confusion_matrix, top_k_accuracy_score

print(classification_report(y_val, y_pred, zero_division=0))
print(confusion_matrix(y_val, y_pred))
# If model outputs probabilities:
top3 = top_k_accuracy_score(y_val, proba, k=3)
```

| Metric | When |
|--------|------|
| Macro F1 | Equal weight per class (rare classes matter) |
| Weighted F1 | Weight by support (closer to accuracy) |
| Micro F1 | Global TP/FP/FN (multi-label overlap) |
| Top-k accuracy | Search / recommender tolerance |

### Encoding labels

```python
from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
y_enc = le.fit_transform(y_train)
# Persist le.classes_ for serving decode
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Always predicts majority class | Class imbalance, wrong metric | `class_weight="balanced"`; SMOTE cautiously; macro F1 |
| Confusion between two similar classes | Feature overlap | Add discriminative features; hierarchical classification |
| Probabilities don't sum to 1 | Wrong API / broken wrapper | Use `predict_proba`; verify OvR calibration |
| Great val, bad prod slice | Train skew vs prod geography | Stratified split by segment; monitor per-class recall |
| K increases, latency spikes | OvO explosion | Switch to OvR or native multiclass; model distillation |
| Label string mismatch at serve | Encoder drift | Version `LabelEncoder` / label map with model artifact |

---

## Gotchas

> [!WARNING]
> **Hierarchical labels treated flat:** "dog" vs "golden retriever" as sibling classes wastes signal — use taxonomy-aware loss or cascade.

> [!WARNING]
> **Argmax ≠ best business action:** cost matrix (misclassify fraud as legit ≠ reverse) — optimize expected cost, not accuracy.

> [!WARNING]
> **Multi-label ≠ multiclass:** user can pick multiple tags — use `MultiOutputClassifier` or sigmoid per label, not softmax.

> [!WARNING]
> **Calibration per class:** OvR probabilities often miscalibrated — isotonic/Platt on validation per class for threshold tuning.

---

## When NOT to use

- **Extremely large K (millions of labels)** — extreme classification, embeddings + ANN retrieval ([[ANN]]), not full softmax.
- **Ordinal classes** (small < medium < large) — treat as [[ordinal classification]], not nominal multiclass.
- **Need interpretable per-class rules** — shallow [[Decision tree]] or separate binary models per business line.

---

## Related

[[binary classification]] · [[ordinal classification]] · [[ML Classifiers]] · [[Mean Average Precision (MAP)]] · [[Normalized Discounted Cumulative Gain (NDCG)]] · [[Decision tree]] · [[Gradient boosting]]
