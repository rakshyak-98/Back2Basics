[[Normalized Discounted Cumulative Gain (NDCG)]] [[rank prediction]] [[binary classification]] [[multiclass classification]] [[Visualization/Rank distribution]] [[Visualization/predicated versus actual plot]]

# Mean Average Precision (MAP)

> Mean Average Precision (MAP) — for each query, you have a ranked list of items. Relevance is binary (or graded in nDCG). Precision@k = relevant in top k

```txt
        Mean Average Preci ──┬── Interview
               ├── Sources
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Interview Relevance
- **Interview probes:** Interviewers ask about Mean Average Precision (MAP) to check whether you can …

## Sources
- [scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html) — deep-dive
- [Google Machine Learning Crash Course](https://developers.google.com/machine-learning/crash-course) — overview

## Technical Details
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

## Mistakes to Avoid
> [!WARNING]
> **MAP with binary relevance** ignores **how** relevant (marginally vs perfect match) — use [[Normalized Discounted Cumulative Gain (NDCG)]] for graded labels.

> [!WARNING]
> **Click data is biased** toward top ranks — raw clicks overestimate MAP of the old ranker.

| Symptom | Check | Fix |
|---------|-------|-----|
| MAP = 1.0 suspiciously | Single relevant doc, trivial rank | More queries; harder negatives |
| MAP flat despite "better" model | Wrong labels (implicit vs explicit) | Define relevance from business event |
| Offline MAP ↑, revenue flat | Position bias in logs | Inverse propensity scoring; interleaving |
| AP undefined | No relevant items in query | Skip query or define fallback metric |
| Compares unfairly across systems | Different candidate pools | Same corpus per query |

## Pros/Cons or Trade-offs
- **Single-label classification**
- **Regression** — use MAE/RMSE ([[regression]]).
- **Clustering** — no query-level ranking.
