[[regression]] [[scikitlearn]] [[sigmoid]] [[data preprocessing]] [[supervised learning]]

# Linear regression

> Predict continuous target as weighted sum of features (+ intercept) — **Hastie ESL**; baseline every tabular regression problem should beat.

---

## Mental model

```txt
ŷ = β₀ + β₁x₁ + β₂x₂ + … + βₚxₚ
```

**Ordinary Least Squares (OLS)** picks β to minimize Σ(yᵢ − ŷᵢ)². Geometrically: orthogonal projection of **y** onto the column space of **X**.

**Assumptions (for classical inference):**
- Linearity in parameters (features can be nonlinear transforms)
- Independent rows (no leakage / duplicate rows inflating confidence)
- Homoscedastic errors (constant variance — check residual plot)
- Low multicollinearity (VIF > 5–10 → unstable β)

**Regularized variants:**

| Model | Penalty | Effect |
|-------|---------|--------|
| Ridge (L2) | Σβ² | Shrinks coefficients; keeps all features |
| Lasso (L1) | Σ\|β\| | Sparse β; feature selection |
| Elastic Net | L1 + L2 | Correlated groups + sparsity |

For classification boundaries, see [[sigmoid]] + logistic regression (not this note).

---

## Standard config / commands

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

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| High train R², awful val | Overfitting transforms / leakage | Audit features; hold out time; reduce polynomial degree |
| Negative R² on val | Wrong baseline, broken pipeline | Verify target not in X; check train/val split |
| Coefficients flip sign vs domain | Multicollinearity | Drop correlated cols; Ridge; PCA |
| Residual fan shape | Heteroscedasticity | Log-transform target; weighted least squares |
| Predictions clip at extremes | Linear extrapolation | Polynomial features; [[Gradient boosting]]; log target |
| `LinAlgError: singular matrix` | Perfect collinearity, p > n | Drop duplicate cols; Ridge; reduce features |

---

## Gotchas

> [!WARNING]
> **R² on skewed targets:** optimizing R² on heavy-tailed revenue can chase outliers — also track MAE / MAPE on business slices.

> [!WARNING]
> **One-hot trap:** dummy variables + intercept = collinearity — drop one category or use regularization.

> [!WARNING]
> **Time series:** random train/test split leaks future — use temporal split or walk-forward CV.

> [!WARNING]
> **Interpretability of raw coefficients** only holds when features are on comparable scales (or standardized).

---

## When NOT to use

- **Strong nonlinear interactions** without explicit feature crosses — [[Gradient boosting]] or GAM usually wins.
- **Target is count / rate with bounds** — Poisson, Gamma GLM, or beta regression.
- **Heavy outliers drive loss** — Huber / quantile regression, or robust tree models.
- **Need calibrated uncertainty in production** — Bayesian linear or conformal prediction on residuals.

---

## Related

[[regression]] · [[Model/Polynomial regression]] · [[Gradient boosting]] · [[Decision tree]] · [[Visualization/Residual plot]] · [[scikitlearn]]
