[[Model/Linear regression]] [[regression]] [[data preprocessing]] [[Visualization/Residual plot]] [[scikitlearn]] [[Visualization/predicated versus actual plot]]

# Polynomial regression

> Extend linear models with **x, x², x³, interactions** to capture curvature — still linear in coefficients, nonlinear in features — **ESL**.

```txt
        Polynomial regress ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Interview Relevance
- **Interview probes:** Interviewers ask about Polynomial regression to check whether you can choose …

## Sources
- [scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html) — deep-dive
- [Google Machine Learning Crash Course](https://developers.google.com/machine-learning/crash-course) — overview

## Key Concepts
- **Note:** Start with [[Model/Linear regression]]: ŷ = β₀ + β₁x

```txt
ŷ = β₀ + β₁x + β₂x² + β₃x₁x₂
```

- **Note:** "Polynomial" refers to **feature engineering**, not a different optimizer

```txt
Degree 1 → line
Degree 2 → parabola (one feature)
Degree 5 → wiggly (overfit risk)
```

- **Note:** High degree + unregularized OLS **overfits** wildly between points (Runge phe…

## Technical Details
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

- Always pair with [[Visualization/Residual plot]]

## Mistakes to Avoid
> [!WARNING]
> **PolynomialFeatures on all columns** — 20 features at degree=3 → thousands of terms.

> [!WARNING]
> **Extrapolation** — polynomials diverge fast outside training min/max x.

| Symptom | Check | Fix |
|---------|-------|-----|
| Wild predictions outside train range | High degree extrapolation | Lower degree; clip; [[Gradient boosting]] |
| Numerical overflow | x large, x⁶ features | StandardScaler; reduce degree |
| Feature count explosion | degree on many columns | Interaction-only; manual terms |
| Better than trees on train only | Overfit | Ridge alpha CV; holdout |
| Negative R² on test | Wrong basis | Try splines/GAM or tree models |

## Pros/Cons or Trade-offs
- **Many categorical / high-dimensional tabular**
- **Sharp discontinuities** — trees handle better than smooth polynomials.
- **Need interpretable single slope**
