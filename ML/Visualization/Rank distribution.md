[[Normalized Discounted Cumulative Gain (NDCG)]] [[Mean Average Precision (MAP)]] [[rank prediction]] [[Visualization/predicated vs actual plot]]

# Rank distribution

> Histogram/KDE of **predicted scores or ranks** — detect collapse, saturation, and train/serve skew in ranking systems.

---

## Mental model

A ranker should produce a **spread** of scores so sorting separates good from bad items. Healthy distribution:

```txt
Frequency
│    ╱╲
│   ╱  ╲
│  ╱    ╲___
└──────────── Score
```

Failure modes:

| Shape | Meaning |
|-------|---------|
| Spike at one value | Model degenerate (all same score) |
| Bimodal | Two regimes merged — check features or calibration |
| Train vs serve mismatch | Different preprocessing or missing features |
| Heavy tail | Few extreme scores dominate top-k |

Compare **train, val, and prod** score distributions — drift here precedes [[Normalized Discounted Cumulative Gain (NDCG)]] drops.

---

## Standard config / commands

```python
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

predictions = model.predict(X_test)  # or decision_function scores

fig, axes = plt.subplots(1, 2, figsize=(10, 4))

sns.histplot(predictions, kde=True, ax=axes[0], bins=50)
axes[0].set_title("Predicted score distribution")
axes[0].set_xlabel("Predicted score")

# Rank within query (search/recsys)
ranks = []
for qid, idx in df.groupby("query_id").groups.items():
    scores = predictions[idx]
    order = np.argsort(-scores)
    ranks.extend(np.argsort(order) + 1)  # 1 = best
sns.histplot(ranks, ax=axes[1], bins=20)
axes[1].set_title("Within-query rank of top item (sanity)")
plt.tight_layout()
plt.show()
```

### Percentile report (prod monitoring)

```python
for p in [50, 90, 99]:
    print(f"p{p}:", np.percentile(predictions, p))
```

Alert if p50 jumps week-over-week without redeploy explanation.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| All scores identical | Model not trained / wrong column | Verify `predict` output variance |
| Scores all 0–1 but flat | Sigmoid saturation | Feature scale; deeper model |
| Prod distribution shifted | Feature null rate | Schema tests; default imputation |
| Top-k always same items | Popularity bias | Negative sampling; diversify |
| Bimodal after deploy | A/B bucket mixing | Split metrics by variant |

---

## Gotchas

> [!WARNING]
> **Global histogram hides per-query effects** — search quality is per-query; always check within-query rank stats too.

> [!WARNING]
> **Calibrated probability ≠ good rank spread** — you need relative ordering, not just 0–1 density.

---

## When NOT to use

- **Pure classification** without scores — use confusion matrix ([[binary classification]]).
- **Regression error analysis** — [[Visualization/Residual plot]] instead.
- **Small offline sets** — histograms noisy; rely on [[Mean Average Precision (MAP)]] with confidence intervals.

---

## Related

[[Mean Average Precision (MAP)]] · [[Normalized Discounted Cumulative Gain (NDCG)]] · [[Visualization/predicated vs actual plot]] · [[rank prediction]]
