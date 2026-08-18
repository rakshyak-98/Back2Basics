[[Model/Linear regression]] [[binary classification]] [[sigmoid]] [[supervised learning]] [[Visualization/Residual plot]]

# Regression

> Predict a **number** (price, latency, demand). Fit a model, check errors with residual plots.

---

## Mental model

**Target is continuous** (a real number). The model outputs **ŷ = f(x)**.

Common loss functions:
- **MSE (L2)** — penalizes large errors heavily
- **MAE (L1)** — more robust to outliers
- **Huber** — mix of both

```txt
Linear:     ŷ = β₀ + β₁x₁ + … + βₚxₚ
Polynomial: add xᵢ², xᵢxⱼ → [[Model/Polynomial regression]]
Nonlinear:  [[Decision tree]], [[Gradient boosting]], [[ANN]]
```

**Explain vs predict:** Linear models are easy to explain; tree/boosting models often predict better but are harder to interpret.

| Variant | Use when |
|---------|----------|
| **Ridge / Lasso** | Multicollinearity, feature selection |
| **Quantile regression** | Need P90 latency, not mean |
| **Log-target** | Skewed positive counts (price, revenue) |

---

## Standard config / commands

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

Despite the name, **multinomial logistic regression** predicts **class probabilities** — see [[multiclass classification]], not this note.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Negative R² on test | Model worse than mean | Features, leakage, wrong split |
| Residual fan shape | Heteroscedasticity | Log transform; weighted least squares |
| Huge errors on tail | Outliers | MAE/Huber; RobustScaler; cap/winsorize (careful) |
| Predictions outside bounds | Unbounded linear head | Clip; beta regression; classify buckets |
| Train RMSE ↓, val flat | Overfit | Regularize; fewer features; simpler model |

Use [[Visualization/Residual plot]] and [[Visualization/predicted vs actual plot]] after every serious regression build.

---

## Gotchas

> [!WARNING]
> **R² alone** — can look good while MAE is unacceptable for SLA (e.g. p99 latency).

> [!WARNING]
> **Extrapolation** — linear models confidently predict nonsense outside training range.

---

## When NOT to use

- **Categorical unordered target** — [[binary classification]] / [[multiclass classification]].
- **Ranking quality** — use ranking metrics ([[Normalized Discounted Cumulative Gain (NDCG)]]).
- **Heavy zero-inflation** (counts with many zeros) — Poisson/negative binomial or two-part models.

---

## Related

[[Model/Linear regression]] · [[Model/Polynomial regression]] · [[Gradient boosting]] · [[Visualization/Residual plot]] · [[data preprocessing]]
