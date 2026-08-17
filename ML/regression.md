[[Model/Linear regression]] [[binary classification]] [[sigmoid]] [[supervised learning]] [[Visualization/Residual plot]] [[Model/Polynomial regression]] [[Gradient boosting]] [[data preprocessing]]

# Regression

> Predict a **continuous** target (price, latency, demand) — minimize squared or robust loss; diagnose with residuals — **Hastie et al. (ESL)**.

```txt
        Regression ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Why It Matters
- **Key signal:** Reviewers ask about Regression to check whether you can choose models/metr…

## Sources
- [scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html) — deep-dive
- [Google Machine Learning Crash Course](https://developers.google.com/machine-learning/crash-course) — overview
- [Linear regression — Wikipedia](https://en.wikipedia.org/wiki/Linear_regression) — overview

## Key Concepts
- **Note:** Supervised task where **y ∈ ℝ** (or bounded interval treated as regression)

```txt
Linear:     ŷ = β₀ + β₁x₁ + … + βₚxₚ
Polynomial: add xᵢ², xᵢxⱼ → [[Model/Polynomial regression]]
- **Note:** Nonlinear: [[Decision tree]], [[Gradient boosting]], [[ANN]]
```

- **Note:** **Explanatory versus predictive:** OLS coefficients interpret causally only u…

| Variant | Use when |
|---------|----------|
| **Ridge / Lasso** | Multicollinearity, feature selection |
| **Quantile regression** | Need P90 latency, not mean |
| **Log-target** | Skewed positive counts (price, revenue) |

## Technical Details
```python
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import cross_val_score

model = Ridge(alpha=1.0)
model.fit(X_train, y_train)
pred = model.predict(X_test)

print("MAE:", mean_absolute_error(y_test, pred))
print("R²:", r2_score(y_test, pred))  # weak alone; use with MAE/RMSE
```

### Log-transform skewed target

```python
y_train_log = np.log1p(y_train)
model.fit(X_train, y_train_log)
pred = np.expm1(model.predict(X_test))
```

### Multinomial logistic (classification, not regression)

- Despite the name, **multinomial logistic regression** predicts **class probab…

## Mistakes to Avoid
> [!WARNING]
> **R² alone** — can look good while MAE is unacceptable for SLA (e.g. p99 latency).

> [!WARNING]
> **Extrapolation** — linear models confidently predict nonsense outside training range.

| Symptom | Check | Fix |
|---------|-------|-----|
| Negative R² on test | Model worse than mean | Features, leakage, wrong split |
| Residual fan shape | Heteroscedasticity | Log transform; weighted least squares |
| Huge errors on tail | Outliers | MAE/Huber; RobustScaler; cap/winsorize (careful) |
| Predictions outside bounds | Unbounded linear head | Clip; beta regression; classify buckets |
| Train RMSE ↓, val flat | Overfit | Regularize; fewer features; simpler model |

Use [[Visualization/Residual plot]] and [[Visualization/predicated versus actual plot]] after every serious regression build.

## Pros/Cons or Trade-offs
- **Categorical unordered target**
- **Ranking quality**
- **Heavy zero-inflation** (counts with many zeros)
