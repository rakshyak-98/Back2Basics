[[scikitlearn]] [[supervised learning]] [[data preprocessing]] [[Model/Linear regression]] [[regression]] [[binary classification]]

# Estimator (ML / statistics)

> Estimator (ML / statistics) — in sklearn, Estimator is the base contract:

```txt
        Estimator (ML / st ──┬── Why it matters
               ├── Sources
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Why It Matters
- **Key signal:** Reviewers ask about Estimator (ML / statistics) to check whether you can c…

## Sources
- [scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html) — deep-dive
- [Google Machine Learning Crash Course](https://developers.google.com/machine-learning/crash-course) — overview

## Technical Details
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

## Mistakes to Avoid
> [!WARNING]
> **Fitting on test data** — even "just once" for scaling — invalidates all reported metrics.

> [!WARNING]
> **Pickle across sklearn versions** — model artifacts may not load; pin versions in prod.

| Symptom | Check | Fix |
|---------|-------|-----|
| `NotFittedError` | Called predict before fit | `fit` on train; persist with `joblib` |
| Different output same data | Unset seed, parallel race | `random_state`; `n_jobs=1` while debugging |
| CV worse than single split | Leakage in preprocessing | Pipeline wrapped in CV |
| `fit` hangs | Huge one-hot, dense matrix | Sparse matrices; feature selection |
| Coefficients "wrong sign" | Collinearity, scaling | Regularization; VIF review |

## Pros/Cons or Trade-offs
- **One-off SQL aggregate**
- **Online learning at high QPS**
