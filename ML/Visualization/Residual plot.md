[[regression]] [[Visualization/predicated versus actual plot]] [[Model/Linear regression]] [[data preprocessing]] [[ordinal classification]] [[Model/Polynomial regression]]

# Residual plot

> Residual plot — residuals should look like random noise around zero:

## Interview Relevance

Interviewers ask about Residual plot to check whether you can choose models/metrics for the problem, explain bias-variance trade-offs, and avoid evaluation mistakes.

## Sources

- [scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html) — deep-dive
- [Google Machine Learning Crash Course](https://developers.google.com/machine-learning/crash-course) — overview

## Key Concepts

Residuals should look like **random noise** around zero:

```txt
Residual
│  • •  •   •
│ • • • • • •   ← random cloud = OK
│• • • • • • •
├────────────── Predicted ŷ
0
```

Structured patterns mean the model missed something:

| Pattern | Interpretation |
|---------|----------------|
| U-shape vs ŷ | Nonlinearity → [[Model/Polynomial regression]] or trees |
| Funnel (spread grows) | Heteroscedasticity → log y, weighted LS |
| Stripes / bands | Wrong family (classification labels as regression) |
| Trend vs feature | Missing interaction or wrong transform |

For **ordinal** models, off-by-k errors show as discrete bands — consider [[ordinal classification]] metrics too.

## Technical Details

```python
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

pred = model.predict(X_test)
residuals = y_test - pred

fig, axes = plt.subplots(1, 2, figsize=(10, 4))

axes[0].scatter(pred, residuals, alpha=0.4, s=12)
axes[0].axhline(0, color="r", linestyle="--")
axes[0].set_xlabel("Predicted")
axes[0].set_ylabel("Residual")

# Q-Q plot for normality of residuals (linear models)
stats.probplot(residuals, plot=axes[1])
axes[1].set_title("Normal Q-Q")
plt.tight_layout()
plt.show()
```

### Residuals vs a suspect feature

```python
plt.scatter(X_test["age"], residuals, alpha=0.4)
plt.axhline(0, color="r", linestyle="--")
plt.xlabel("age")
plt.ylabel("Residual")
```

### Standardized residuals (outlier hunt)

```python
std_res = residuals / residuals.std()
outliers = np.abs(std_res) > 3
print(f"Outlier count: {outliers.sum()}")
```

## Pros/Cons or Trade-offs

- **Classification** — use calibration curves / confusion matrix.
- **Huge datasets** — subsample scatter; use binned residual plots.
- **Ranking-only goals** — [[Normalized Discounted Cumulative Gain (NDCG)]] on ranked lists.

## Mistakes to Avoid

> [!WARNING]
> **Heteroscedasticity** violates OLS confidence intervals — predictions may still be OK; inference is wrong.

> [!WARNING]
> **Outliers drive visual scale** — plot standardized residuals or use robust regression.

| Symptom | Check | Fix |
|---------|-------|-----|
| U-curve | Linearity assumption | Add squared term or [[Gradient boosting]] |
| Funnel | Variance scales with y | `log1p(y)`; heteroscedastic models |
| Few huge residuals | Bad rows / leakage | Inspect outliers; data QA |
| Periodic pattern | Seasonality missing | Time features; SARIMA / separate model |
| Mean residual ≠ 0 | Systematic bias | Intercept issue; recalibrate |

Pair with [[Visualization/predicated versus actual plot]] for full picture.

