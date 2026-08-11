[[Model/Linear regression]] [[regression]] [[data preprocessing]] [[Visualization/Residual plot]] [[scikitlearn]]

# Polynomial regression

> Extend linear models with **x, x², x³, interactions** to capture curvature — still linear in coefficients, nonlinear in features — **ESL**.

---

## Mental model

Start with [[Model/Linear regression]]: ŷ = β₀ + β₁x. Add powers and cross-terms:

```txt
ŷ = β₀ + β₁x + β₂x² + β₃x₁x₂
```

"Polynomial" refers to **feature engineering**, not a different optimizer — still fit with OLS/Ridge/Lasso on expanded matrix.

```txt
Degree 1 → line
Degree 2 → parabola (one feature)
Degree 5 → wiggly (overfit risk)
```

High degree + unregularized OLS **overfits** wildly between points (Runge phenomenon). Prefer **Ridge** or low degree + cross-validation.

---

## Standard config / commands

```python
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score

pipe = Pipeline([
    ("poly", PolynomialFeatures(degree=2, include_bias=False)),
    ("scale", StandardScaler()),   # critical for high powers
    ("model", Ridge(alpha=1.0)),
])

scores = cross_val_score(pipe, X_train, y_train, cv=5, scoring="neg_mean_squared_error")
pipe.fit(X_train, y_train)
```

### Manual interaction only (safer than full degree-3)

```python
PolynomialFeatures(degree=2, interaction_only=True, include_bias=False)
```

### Choose degree by validation

```python
for d in [1, 2, 3]:
    p = Pipeline([("poly", PolynomialFeatures(d)), ("ridge", Ridge())])
    print(d, cross_val_score(p, X, y, cv=5).mean())
```

Always pair with [[Visualization/Residual plot]] — U-shaped residuals hint missing quadratic term.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Wild predictions outside train range | High degree extrapolation | Lower degree; clip; [[Gradient boosting]] |
| Numerical overflow | x large, x⁶ features | StandardScaler; reduce degree |
| Feature count explosion | degree on many columns | Interaction-only; manual terms |
| Better than trees on train only | Overfit | Ridge alpha CV; holdout |
| Negative R² on test | Wrong basis | Try splines/GAM or tree models |

---

## Gotchas

> [!WARNING]
> **PolynomialFeatures on all columns** — 20 features at degree=3 → thousands of terms.

> [!WARNING]
> **Extrapolation** — polynomials diverge fast outside training min/max x.

---

## When NOT to use

- **Many categorical / high-dimensional tabular** — [[Decision tree]] / [[Gradient boosting]] find interactions automatically.
- **Sharp discontinuities** — trees handle better than smooth polynomials.
- **Need interpretable single slope** — stick to degree-1 [[Model/Linear regression]].

---

## Related

[[Model/Linear regression]] · [[regression]] · [[Visualization/Residual plot]] · [[Visualization/predicated vs actual plot]] · [[data preprocessing]]
