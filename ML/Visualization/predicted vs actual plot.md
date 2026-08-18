[[regression]] [[Visualization/Residual plot]] [[rank prediction]] [[Mean Average Precision (MAP)]]

# Predicted vs actual plot

> Scatter plot of **actual vs predicted** values — quick check for bias and bad fits in regression.

---

## Mental model

Perfect predictions sit on the line **y = x**:

```txt
ŷ
│     ╱ ideal
│   ╱
│ ╱  • above line → under-predicted
│╱   • below line → over-predicted
└──────── y_true
```

What the shape tells you:

| Pattern | Likely cause |
|---------|--------------|
| Points spread wider as y grows | Errors grow with target size |
| Curve below the line | Model misses non-linear pattern |
| Flat band at top/bottom | Target was capped; model hits a ceiling |
| Cluster off the line | Missing feature or wrong model for that group |

For **ranking** models, compare predicted scores to true grades — use with [[Mean Average Precision (MAP)]].

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

Always also plot [[Visualization/Residual plot]] — this scatter can hide error patterns when values are large.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Tight cloud but bad business score | Wrong metric for the job | Plot by user segment |
| S-curve off the line | Target needs log/normal transform | Log target; try [[Model/Polynomial regression]] |
| Vertical stripe at one y | Really a classification bucket | Use classification metrics |
| Flat predictions | Broken model or leaked features removed | Compare to a simple baseline |
| Rank scores all similar | Scores not calibrated | Calibrate; check [[Visualization/Rank distribution]] |

---

## Gotchas

> [!WARNING]
> **Outliers squash the plot** — use log axes or hexbin; do not overfit a handful of points.

---

## When NOT to use

- **Classification** — use confusion matrix / ROC, not this scatter.
- **Many output dimensions** — one subplot per target or use summary metrics.
- **Ranking only** — [[Normalized Discounted Cumulative Gain (NDCG)]] curves are clearer.

---

## Related

[[Visualization/Residual plot]] · [[regression]] · [[rank prediction]] · [[Mean Average Precision (MAP)]] · [[Visualization/Rank distribution]]
