[[regression]] [[binary classification]] [[multiclass classification]] [[data preprocessing]] [[estimator]]

# Supervised learning

> Learn a mapping **X → y** from labeled examples; generalize to unseen data via train/val/test discipline — **Hastie et al. (ESL)**.

---

## Mental model

You have pairs `(xᵢ, yᵢ)`. The algorithm picks a function class (linear, tree, neural net) and minimizes **empirical risk** + regularization on training data. Success = low error on **new** data from the same distribution.

```txt
Training set  → fit model parameters
Validation set  → tune hyperparameters / early stop
Test set        → report once (never tune on this)
```

| Task type | Target y | Typical algorithms |
|-----------|----------|-------------------|
| **Regression** | Continuous | [[Model/Linear regression]], [[Gradient boosting]], [[ANN]] |
| **Binary classification** | {0,1} | Logistic, [[Decision tree]], [[Model/support vector machines (SVM)]] |
| **Multiclass** | K labels | Softmax, one-vs-rest, [[Random forest]] |
| **Ordinal** | Ordered classes | [[ordinal classification]] |
| **Ranking** | Relevance order | LambdaMART, [[Normalized Discounted Cumulative Gain (NDCG)]] |

**Distribution shift** (train 2022, deploy 2026) breaks supervised assumptions — monitor features and labels in prod.

---

## Standard config / commands

```python
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, classification_report

X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y if classification else None)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

pipe = Pipeline([("prep", preprocess), ("model", base_estimator)])
pipe.fit(X_train, y_train)

# Regression
print(mean_squared_error(y_test, pipe.predict(X_test), squared=False))

# Classification
print(classification_report(y_test, pipe.predict(X_test)))
```

### Baseline first (always)

```python
from sklearn.dummy import DummyClassifier, DummyRegressor
baseline = DummyClassifier(strategy="most_frequent")  # or DummyRegressor(strategy="mean")
baseline.fit(X_train, y_train)
# Your model must beat this on the metric that matters
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Perfect train, poor test | Overfit, leakage | Regularize; simpler model; audit features |
| Baseline beats model | Broken features, wrong metric | EDA; [[data preprocessing]] |
| Metrics drift in prod | Label delay, shift | Retrain pipeline; feature monitoring |
| Labels inconsistent | Annotation guidelines | Inter-rater agreement; gold set |
| Slow iteration | No pipeline | sklearn Pipeline + single `fit` path |

---

## Gotchas

> [!WARNING]
> **Tuning on test set** — any decision using test labels (including feature selection) inflates scores. Hold out test until the end.

> [!WARNING]
> **Random split on time-series** — use temporal split; future leaking into past.

---

## When NOT to use

- **No labels / labels too expensive** — semi-supervised or unsupervised clustering (different playbook).
- **Need causal effect** ("what if we change price") — predictive model ≠ causal inference.
- **Adversarial inputs** — supervised accuracy doesn't guarantee robustness.

---

## Related

[[regression]] · [[binary classification]] · [[multiclass classification]] · [[data preprocessing]] · [[estimator]] · [[scikitlearn]]
