[[ML]] [[Normalized Discounted Cumulative Gain (NDCG)]] [[Mean Average Precision (MAP)]] [[xg boost]]

# rank prediction

> Rank prediction orders items by relevance — learning-to-rank, not just classify/regress one score in isolation.

## Interview Relevance

Interviewers ask about rank prediction to check whether you can choose models/metrics for the problem, explain bias-variance trade-offs, and avoid evaluation mistakes.

## Sources

- [scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html) — deep-dive
- [Google Machine Learning Crash Course](https://developers.google.com/machine-learning/crash-course) — overview

## Key Concepts

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

## Technical Details

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

## Pros/Cons or Trade-offs

- **Binary gate only** — plain classifier may suffice.
- **Tiny catalogs** — hand rules / editorial order.

## Mistakes to Avoid

> [!WARNING]
> **Offline NDCG ≠ online engagement** — A/B test the ranking change.

> [!WARNING]
> **Label noise** — implicit clicks ≠ true relevance.

| Symptom | Check | Fix |
|---------|-------|-----|
| High AUC, bad NDCG | wrong metric | Optimize ranking metric |
| Popularity bias | always head items | Diversify / debias features |
| Leakage | future features | Time-based split |
| Slow serving | huge candidate set | Two-stage retrieval + rank |

