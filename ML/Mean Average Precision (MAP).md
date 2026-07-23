[[Normalized Discounted Cumulative Gain (NDCG)]] [[rank prediction]] [[binary classification]] [[multiclass classification]]

# Mean Average Precision (MAP)

> Ranking metric: average of **per-query Average Precision** — rewards relevant items ranked high — **IR evaluation (Manning, Raghavan, Schütze)**.

---

## Mental model

For each query, you have a ranked list of items. **Relevance** is binary (or graded in nDCG). **Precision@k** = relevant in top k / k. **Average Precision (AP)** integrates precision at each rank where a relevant item appears.

```txt
AP = (1/R) Σₖ Precision@k · rel(k)     # R = number of relevant docs
MAP = mean(AP over all queries)
```

MAP cares about **order**: putting all relevant items at the top scores higher than burying one relevant doc at rank 50.

| Metric | Granularity |
|--------|-------------|
| **Precision@K** | Fixed cutoff (homepage shows 10) |
| **Recall@K** | Coverage in top K |
| **AP / MAP** | Full ranked list, query-averaged |
| **[[Normalized Discounted Cumulative Gain (NDCG)]]** | Graded relevance + position discount |

---

## Standard config / commands

```python
from sklearn.metrics import average_precision_score, label_ranking_average_precision_score

# Binary relevance, single score per item
y_true = [0, 1, 1, 0, 1]      # relevance labels
y_scores = [0.1, 0.9, 0.4, 0.2, 0.8]  # model scores (higher = more relevant)

ap = average_precision_score(y_true, y_scores)
print("AP:", ap)

# Multi-query: compute AP per query, then mean
map_score = np.mean([
    average_precision_score(y_true_q, scores_q)
    for y_true_q, scores_q in zip(y_true_by_query, scores_by_query)
])
```

### Recommendation / search eval loop

1. Hold out queries with labeled relevant set (clicks, purchases, human grades).
2. Score all candidates; sort descending.
3. Report MAP @ full list and **Precision@5 / Recall@20** for product SLAs.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| MAP = 1.0 suspiciously | Single relevant doc, trivial rank | More queries; harder negatives |
| MAP flat despite "better" model | Wrong labels (implicit vs explicit) | Define relevance from business event |
| Offline MAP ↑, revenue flat | Position bias in logs | Inverse propensity scoring; interleaving |
| AP undefined | No relevant items in query | Skip query or define fallback metric |
| Compares unfairly across systems | Different candidate pools | Same corpus per query |

---

## Gotchas

> [!WARNING]
> **MAP with binary relevance** ignores **how** relevant (marginally vs perfect match) — use [[Normalized Discounted Cumulative Gain (NDCG)]] for graded labels.

> [!WARNING]
> **Click data is biased** toward top ranks — raw clicks overestimate MAP of the old ranker.

---

## When NOT to use

- **Single-label classification** — use precision/recall/F1 ([[binary classification]]).
- **Regression** — use MAE/RMSE ([[regression]]).
- **Clustering** — no query-level ranking.

---

## Related

[[Normalized Discounted Cumulative Gain (NDCG)]] · [[rank prediction]] · [[Visualization/Rank distribution]] · [[Visualization/predicated vs actual plot]]
