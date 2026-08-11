[[Mean Average Precision (MAP)]] [[rank prediction]] [[Visualization/Rank distribution]]

# Normalized Discounted Cumulative Gain (NDCG)

> Graded ranking metric — relevant items higher in the list score more; normalized to [0,1] vs ideal ranking — **Järvelin & Kekäläinen (2002)**.

---

## Mental model

**DCG** sums relevance with a **logarithmic position discount** (top ranks matter most):

```txt
DCG@k = Σᵢ₌₁ᵏ (2^relᵢ − 1) / log₂(i + 1)
NDCG@k = DCG@k / IDCG@k        # IDCG = DCG of perfect ranking
```

Relevance **rel** can be 0–3 (not relevant → perfect). NDCG = 1 only when the list matches the ideal order up to k.

```txt
Rank 1 relevant (grade 3)  → large gain
Rank 10 same item          → heavily discounted
```

vs [[Mean Average Precision (MAP)]]: MAP is binary relevance; NDCG handles **graded** judgment (somewhat relevant vs exact match).

---

## Standard config / commands

```python
import numpy as np

def dcg_at_k(relevances, k):
    rel = np.asarray(relevances)[:k]
    if rel.size == 0:
        return 0.0
    discounts = np.log2(np.arange(2, rel.size + 2))
    return np.sum((2**rel - 1) / discounts)

def ndcg_at_k(relevances, k):
    dcg = dcg_at_k(relevances, k)
    ideal = dcg_at_k(sorted(relevances, reverse=True), k)
    return dcg / ideal if ideal > 0 else 0.0

# Example: predicted order relevances [3, 2, 0, 1, 0]
print("NDCG@5:", ndcg_at_k([3, 2, 0, 1, 0], k=5))
```

### sklearn (binary relevance as 0/1)

```python
from sklearn.metrics import ndcg_score
# y_true shape (n_queries, n_items), y_score shape same
ndcg = ndcg_score(y_true, y_score, k=10)
```

Report **NDCG@5** and **NDCG@10** separately — product surfaces differ.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| NDCG always ~1 | Tiny candidate sets | Expand pool; harder negatives |
| NDCG drops after reranker | Graded labels inconsistent | Harmonize label guidelines |
| Compare @k across teams | Different k | Fix k in SLA (e.g. @10) |
| IDCG = 0 | No relevant items | Exclude query from aggregate |
| sklearn shape errors | Query matrix layout | `(n_queries, n_items)` 2D arrays |

---

## Gotchas

> [!WARNING]
> **Position bias in logged data** — users rarely see rank 20; NDCG on biased logs favors old rankers.

> [!WARNING]
> **Exponential gain 2^rel − 1** — high grades dominate; one "3" at rank 1 can mask many rank-10 failures.

---

## When NOT to use

- **Binary classification without ranking** — [[binary classification]] metrics.
- **Continuous score prediction** — [[regression]] + [[Visualization/predicated vs actual plot]].
- **Uniform relevance only** — [[Mean Average Precision (MAP)]] may be simpler to explain.

---

## Related

[[Mean Average Precision (MAP)]] · [[rank prediction]] · [[Visualization/Rank distribution]] · [[Gradient boosting]]
