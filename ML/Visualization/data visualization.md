[[ML]] [[model tranning]]

# data visualization

> Viz checks whether the data and model make sense — plots before metrics, residual plots after fit.

---

## Mental model

**Say it in one breath:** Look at distributions, class balance, and errors — a bad chart beats a wrong AUC story.

```txt
EDA plots → train → residual / pred-vs-actual → decide next feature
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Histogram / KDE** | Distribution shape | “Skew, outliers, multimodality.” |
| **Scatter** | Relationship | “Non-linear? clusters?” |
| **Confusion matrix** | Class errors | “Which classes confuse.” |
| **Residual** | y − ŷ | “Structure left = missing signal.” |

---

## Standard config / commands

```python
import matplotlib.pyplot as plt
plt.hist(y, bins=30); plt.title('label distribution')
plt.scatter(y_true, y_pred, alpha=0.3); plt.xlabel('actual'); plt.ylabel('pred')
plt.scatter(y_pred, y_true - y_pred, alpha=0.3); plt.axhline(0)
```

| Knob | Why it matters |
|------|----------------|
| Alpha / sample | Huge N overplots |
| Log scales | Heavy tails |
| Color by segment | Hidden cohorts |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Metric high, plot ugly | leakage / wrong target | Inspect preds |
| One bar dominates | imbalance | Resample / other metric |
| Fan-shaped residuals | heteroscedasticity | Transform target / model |
| Overplot ink | millions of points | Hexbin / sample |

---

## Gotchas

> [!WARNING]
> **Default axes lie** — truncated y-axis exaggerates tiny effects.

> [!WARNING]
> **Chart without sample size** — pretty nonsense.

---

## When NOT to use

- **Automated nightly metrics only** — still sample-plot failures.
- **Huge dashboards nobody reads** — fewer sharper plots.

## Related

[[Visualization/Residual plot]] [[Visualization/predicated vs actual plot]] [[model tranning]]
