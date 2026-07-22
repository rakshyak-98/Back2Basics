[[regression]] [[Visualization/Residual plot]] [[rank prediction]] [[Mean Average Precision (MAP)]]

# Predicted vs actual plot

> Scatter of **y_true vs ŷ** — quick visual for calibration, bias, and heteroscedasticity — standard regression QA.

---

## Mental model

Perfect predictions lie on the diagonal **y = x**:

```txt
ŷ
│     ╱ ideal
│   ╱
│ ╱  • points above → under-predict
│╱   • points below → over-predict
└──────── y_true
```

Patterns tell stories:

| Pattern | Likely issue |
|---------|--------------|
| Points fan out | Variance grows with y (heteroscedasticity) |
| Systematic curve below diagonal | Model underfits nonlinearity |
| Horizontal band at cap | Target clipped; model hits ceiling |
| Clusters off diagonal | Missing segment feature or wrong model per segment |

For **ranking** models, same plot compares predicted scores to graded relevance — use alongside [[Mean Average Precision (MAP)]].

---

## Standard config / commands

```python
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import mean_absolute_error, r2_score

pred = model.predict(X_test)

fig, ax = plt.subplots(figsize=(6, 6))
ax.scatter(y_test, pred, alpha=0.4, s=12)
lims = [min(y_test.min(), pred.min()), max(y_test.max(), pred.max())]
ax.plot(lims, lims, "r--", lw=1, label="y = x")
ax.set_xlabel("Actual")
ax.set_ylabel("Predicted")
ax.set_title(f"Actual vs Predicted (MAE={mean_absolute_error(y_test, pred):.3f})")
ax.legend()
plt.tight_layout()
plt.show()
```

### Hexbin for large n (readable density)

```python
plt.hexbin(y_test, pred, gridsize=40, cmap="Blues", mincnt=1)
plt.plot(lims, lims, "r--")
```

### Residual companion

Always pair with [[Visualization/Residual plot]] — actual vs predicted hides structure in errors when scale is large.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Tight cloud but bad business metric | Wrong aggregate metric | Segment plot by cohort |
| S-curve off diagonal | Log/normal target | Log transform; [[Model/Polynomial regression]] |
| Vertical stripe at one y | Class imbalance bucket | Classification not regression |
| Predictions constant | Dead model / leakage removed | Baseline check |
| Rank plot flat | Scores uncalibrated | Calibrate; check [[Visualization/Rank distribution]] |

---

## Gotchas

> [!WARNING]
> **Outliers compress the cloud** — use log axes or hexbin; don't overfit 3 points.

> [!WARNING]
> **Filename typo:** this note is `predicated vs actual plot.md` in the vault — link as `[[Visualization/predicated vs actual plot]]`.

---

## When NOT to use

- **Classification** — confusion matrix / ROC, not y vs ŷ scatter.
- **High-dimensional output** — per-target subplots or aggregate metrics.
- **Only ranking matters** — [[Normalized Discounted Cumulative Gain (NDCG)]] curves beat scatter.

---

## Related

[[Visualization/Residual plot]] · [[regression]] · [[rank prediction]] · [[Mean Average Precision (MAP)]] · [[Visualization/Rank distribution]]
