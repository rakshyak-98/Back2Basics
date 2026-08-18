# Rank prediction

Predict a student's **rank** (or similar ordered score) from exam marks or other features.

## Key ideas

- Ranks are **ordered** — 1st beats 2nd, but gaps between ranks are not always equal.
- Scores are often **dense** in the middle — small changes near the top can move rank a lot.
- Top buckets (top 1%, top 5%) can be treated as **classification** instead of pure regression.

## Example: NEET marks → rank

This is usually **regression** (predict a number) with an **ordinal** target (order matters).

> [!NOTE] The model maps marks (and other features) to a rank value. Order matters more than exact distance between ranks.

## Models

[[Model/Linear regression]] · [[ordinal classification]]

- **Linear regression** — simple baseline; assumes a straight-line link.
- **Ordinal regression** — respects order without equal steps between ranks.

### Other options

- **Plain classification** — treat each rank as a class. Usually weak because it ignores order.
- **Learning to rank** — order a list of items (search, recommendations). Use when ranking many items per query, not one rank per student.

## Metrics (example targets)

| Metric | Example goal |
|--------|----------------|
| MAE | ~250 |
| RMSE | ~300 |
| R² | ~0.85 |

Also use **rank correlation** and **[[Mean Average Precision (MAP)]]** / **[[Normalized Discounted Cumulative Gain (NDCG)]]** when order is what you care about.

## Visualization

- **Histogram** — score spread per bin (bin size changes the picture).
- **Density plot** — smooth curve; harder to read on huge datasets.
- **Box plot** — outliers and spread; good for comparing groups.

> [!INFO] Start with histogram or density for shape. Use box plots to compare groups or spot outliers.

- **[[Visualization/predicted vs actual plot]]** — how far off predicted ranks are.
- **[[Visualization/Rank distribution]]** — compare predicted vs true rank spread.

## Why neural networks?

- Capture **non-linear** mark → rank patterns.
- Scale with more layers for harder problems.
- Can target continuous rank (regression) or ordered buckets (classification).

## Model training checklist

- Clean labels and features.
- Normalize or scale numeric features.
- Try linear / ordinal regression, then **[[Gradient boosting]]** (XGBoost, LightGBM).
- Pick a ranking-aware loss when order matters.
- Tune on validation — watch overfitting on small cohorts.

## Common questions

| Question | Short answer |
|----------|--------------|
| How do marks relate to rank? | Plot marks vs rank; check correlation and non-linearity. |
| What drives rank? | Feature importance, SHAP, or ablation on past scores, activities, etc. |
| Why not unsupervised? | You need labeled ranks — unsupervised finds clusters, not rank labels. |
| Can RAG help? | Only if you retrieve useful text features (essays, notes) — not for marks alone. |

## References

- [Rank predictor errors (video)](https://www.youtube.com/watch?v=5ZtCh0k9jd0)
- [Learning to rank (Stanford)](https://web.stanford.edu/class/cs276/handouts/lecture14-learning-ranking.pdf)
- [Student performance prediction (paper)](https://www.ijraset.com/best-journal/student-performance-prediction-using-ml-and-ai)
- [Survey paper](https://link.springer.com/article/10.1007/s10462-022-10155-y)
- [Entrance exam ranks (article)](https://www.ai.codersarts.com/post/predicting-entrance-exam-ranks-and-college-admissions-with-machine-learning)
- [Learning to rank guide](https://towardsdatascience.com/learning-to-rank-a-complete-guide-to-ranking-using-machine-learning-4c9688d370d4)
- [arXiv paper](http://arxiv.org/pdf/1811.12808)

## Related

[[regression]] · [[ordinal classification]] · [[model training]] · [[Mean Average Precision (MAP)]]
