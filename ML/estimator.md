[[scikitlearn]] [[supervised learning]] [[data preprocessing]] [[Model/Linear regression]]

# Estimator (ML / statistics)

> An object that **learns parameters from data** via `fit` and **applies** them via `predict` / `transform` — scikit-learn's uniform API — **Pedregosa et al. (sklearn)**.

---

## Mental model

In sklearn, **Estimator** is the base contract:

```txt
estimator.fit(X, y)     # learns from training data
estimator.predict(X)    # inference (classifiers, regressors)
estimator.transform(X)  # preprocessing (scalers, encoders)
```

Statistical estimators (sample mean, MLE) **estimate population quantities** from a sample. Properties matter:

| Property | Meaning |
|----------|---------|
| **Unbiased** | E[θ̂] = θ on average |
| **Consistent** | θ̂ → θ as n → ∞ |
| **Efficient** | Low variance among unbiased estimators |

ML "estimators" prioritize **predictive loss** on held-out data, not unbiasedness of coefficients.

```txt
Pipeline: [Transformer₁ → Transformer₂ → Predictor]
          fit/transform only on train inside CV
```

---

## Standard config / commands

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.model_selection import cross_val_score

pipe = Pipeline([
    ("scale", StandardScaler()),
    ("model", Ridge(alpha=1.0)),
])

scores = cross_val_score(pipe, X, y, cv=5, scoring="neg_mean_squared_error")
pipe.fit(X_train, y_train)
y_pred = pipe.predict(X_test)
```

### Checklist before calling `.fit`

1. `X` shape `(n_samples, n_features)` — no object columns unless ColumnTransformer handles them.
2. Align `y` index with `X`.
3. No NaN unless imputer in pipeline.
4. Same random seed for reproducible estimators (`random_state=42`).

### Custom estimator skeleton

```python
from sklearn.base import BaseEstimator, ClassifierMixin

class MajorityClassifier(BaseEstimator, ClassifierMixin):
    def fit(self, X, y):
        self.classes_ = np.unique(y)
        self.majority_ = np.bincount(y).argmax()
        return self
    def predict(self, X):
        return np.full(len(X), self.majority_)
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `NotFittedError` | Called predict before fit | `fit` on train; persist with `joblib` |
| Different output same data | Unset seed, parallel race | `random_state`; `n_jobs=1` while debugging |
| CV worse than single split | Leakage in preprocessing | Pipeline wrapped in CV |
| `fit` hangs | Huge one-hot, dense matrix | Sparse matrices; feature selection |
| Coefficients "wrong sign" | Collinearity, scaling | Regularization; VIF review |

---

## Gotchas

> [!WARNING]
> **Fitting on test data** — even "just once" for scaling — invalidates all reported metrics.

> [!WARNING]
> **Pickle across sklearn versions** — model artifacts may not load; pin versions in prod.

---

## When NOT to use

- **One-off SQL aggregate** — not every computation needs a reusable Estimator class.
- **Online learning at high QPS** — sklearn estimators batch-fit; use streaming libraries (River, Vowpal) or serve frozen weights.

---

## Related

[[scikitlearn]] · [[data preprocessing]] · [[supervised learning]] · [[regression]] · [[binary classification]]
