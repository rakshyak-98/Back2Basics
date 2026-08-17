[[ML]] [[model tranning]] [[Visualization/Residual plot]] [[Visualization/predicated versus actual plot]]

# data visualization

> Viz checks whether the data and model make sense — plots before metrics, residual plots after fit.

```txt
        data visualization ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Why It Matters
- **Key signal:** Reviewers ask about data visualization to check whether you can choose mod…

## Sources
- [scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html) — deep-dive
- [Google Machine Learning Crash Course](https://developers.google.com/machine-learning/crash-course) — overview

## Key Concepts
```txt
- **Note:** EDA plots → train → residual / pred-vs-actual → decide next feature
```

### Review map (words you can say)

| Word | Plain meaning | Say in review |
|------|---------------|------------------|
| **Histogram / KDE** | Distribution shape | “Skew, outliers, multimodality.” |
| **Scatter** | Relationship | “Non-linear? clusters?” |
| **Confusion matrix** | Class errors | “Which classes confuse.” |
| **Residual** | y − ŷ | “Structure left = missing signal.” |

## Technical Details
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

## Mistakes to Avoid
> [!WARNING]
> **Default axes lie** — truncated y-axis exaggerates tiny effects.

> [!WARNING]
> **Chart without sample size** — pretty nonsense.

| Symptom | Check | Fix |
|---------|-------|-----|
| Metric high, plot ugly | leakage / wrong target | Inspect preds |
| One bar dominates | imbalance | Resample / other metric |
| Fan-shaped residuals | heteroscedasticity | Transform target / model |
| Overplot ink | millions of points | Hexbin / sample |

## Pros/Cons or Trade-offs
- **Automated nightly metrics only** — still sample-plot failures.
- **Huge dashboards nobody reads** — fewer sharper plots.
