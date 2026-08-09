[[ML]] [[Normalized Discounted Cumulative Gain (NDCG)]] [[Mean Average Precision (MAP)]]

# rank prediction

> Rank prediction orders items by relevance — learning-to-rank, not just classify/regress one score in isolation.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** For each query/user, score candidates and sort; optimize ranking metrics (NDCG/MAP), not only pointwise MSE.

```txt
query → candidates → score → sort → top-K
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Pointwise** | Predict relevance score | “Regression/classification per item.” |
| **Pairwise** | Prefer A over B | “Learning-to-rank losses.” |
| **Listwise** | Optimize whole list | “Closer to NDCG.” |
| **NDCG / MAP** | Ranking quality | “Top ranks matter more.” |

---

## Standard config / commands

```python
# sketch: score then sort
scores = model.predict(candidate_features)
ranked = candidates.iloc[scores.argsort()[::-1]]
# evaluate with NDCG@K / MAP@K
```

| Knob | Why it matters |
|------|----------------|
| K | Business cares about top of list |
| Group by query | Metrics are per-list |
| Candidate gen | Ranker can’t fix a bad funnel |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| High AUC, bad NDCG | wrong metric | Optimize ranking metric |
| Popularity bias | always head items | Diversify / debias features |
| Leakage | future features | Time-based split |
| Slow serving | huge candidate set | Two-stage retrieval + rank |

---

## Gotchas

> [!WARNING]
> **Offline NDCG ≠ online engagement** — A/B test the ranking change.

> [!WARNING]
> **Label noise** — implicit clicks ≠ true relevance.

---

## When NOT to use

- **Binary gate only** — plain classifier may suffice.
- **Tiny catalogs** — hand rules / editorial order.

## Related

[[Normalized Discounted Cumulative Gain (NDCG)]] [[Mean Average Precision (MAP)]] [[xg boost]]
