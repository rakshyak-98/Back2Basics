[[regression]] [[scikitlearn]] [[sigmoid]] [[data preprocessing]] [[supervised learning]] [[Model/Polynomial regression]] [[Gradient boosting]] [[Decision tree]] [[Visualization/Residual plot]]

# Linear regression

> Predict continuous target as weighted sum of features (+ intercept) — **Hastie ESL**; baseline every tabular regression problem should beat.

```txt
        Linear regression ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Why It Matters
- **Key signal:** Reviewers ask about Linear regression to check whether you can choose mode…

## Sources
- [scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html) — deep-dive
- [Google Machine Learning Crash Course](https://developers.google.com/machine-learning/crash-course) — overview
- [Linear regression — Wikipedia](https://en.wikipedia.org/wiki/Linear_regression) — overview

## Key Concepts
```txt
ŷ = β₀ + β₁x₁ + β₂x₂ + … + βₚxₚ
```

- **Note:** **Ordinary Least Squares (OLS)** picks β to minimize Σ(yᵢ − ŷᵢ)²

**Assumptions (for classical inference):**
- **Linearity in:** Linearity in parameters (features can be nonlinear transforms)
- **Independent rows:** Independent rows (no leakage / duplicate rows inflating confidence)
- **Homoscedastic errors:** Homoscedastic errors (constant variance — check residual plot)
- **Low multicollinearity:** Low multicollinearity (VIF > 5–10 → unstable β)

**Regularized variants:**

| Model | Penalty | Effect |
|-------|---------|--------|
| Ridge (L2) | Σβ² | Shrinks coefficients; keeps all features |
| Lasso (L1) | Σ\|β\| | Sparse β; feature selection |
| Elastic Net | L1 + L2 | Correlated groups + sparsity |

- **Note:** For classification boundaries, see [[sigmoid]] + logistic regression (not thi…

## Technical Details
### sklearn baseline

```python
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score

pipe = Pipeline([
    ("scale", StandardScaler()),   # OLS scale-invariant; Ridge/Lasso need it
    ("model", Ridge(alpha=1.0)),
])
pipe.fit(X_train, y_train)
scores = cross_val_score(pipe, X_train, y_train, cv=5, scoring="neg_root_mean_squared_error")
```

### Diagnostics

```python
from sklearn.metrics import mean_squared_error, r2_score

y_pred = pipe.predict(X_val)
rmse = mean_squared_error(y_val, y_pred, squared=False)
r2 = r2_score(y_val, y_pred)
```

### Statsmodels (inference: p-values, CIs)

```python
import statsmodels.api as sm

X_sm = sm.add_constant(X_train)
ols = sm.OLS(y_train, X_sm).fit()
print(ols.summary())  # coef, std err, t, p-value, R²
```

### Feature scaling rule

- **OLS:** scaling doesn't change predictions (only coefficient scale).
- **Ridge/Lasso:** **always scale** — penalty is not rotation-invariant.

## Mistakes to Avoid
> [!WARNING]
> **R² on skewed targets:** optimizing R² on heavy-tailed revenue can chase outliers — also track MAE / MAPE on business slices.

> [!WARNING]
> **One-hot trap:** dummy variables + intercept = collinearity — drop one category or use regularization.

> [!WARNING]
> **Time series:** random train/test split leaks future — use temporal split or walk-forward CV.

> [!WARNING]
> **Interpretability of raw coefficients** only holds when features are on comparable scales (or standardized).

| Symptom | Check | Fix |
|---------|-------|-----|
| High train R², awful val | Overfitting transforms / leakage | Audit features; hold out time; reduce polynomial degree |
| Negative R² on val | Wrong baseline, broken pipeline | Verify target not in X; check train/val split |
| Coefficients flip sign vs domain | Multicollinearity | Drop correlated cols; Ridge; PCA |
| Residual fan shape | Heteroscedasticity | Log-transform target; weighted least squares |
| Predictions clip at extremes | Linear extrapolation | Polynomial features; [[Gradient boosting]]; log target |
| `LinAlgError: singular matrix` | Perfect collinearity, p > n | Drop duplicate cols; Ridge; reduce features |

## Pros/Cons or Trade-offs
- **Strong nonlinear interactions** without explicit feature crosses
- **Target is count / rate with bounds**
- **Heavy outliers drive loss**
- **Need calibrated uncertainty in production**
