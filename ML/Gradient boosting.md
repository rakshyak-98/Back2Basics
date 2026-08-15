[[Decision tree]] [[Random forest]] [[xg boost]] [[scikitlearn]] [[regression]] [[binary classification]] [[Model/Linear regression]] [[multiclass classification]]

# Gradient boosting

> Sequential ensemble: each new tree fits the **residual errors** of the ensemble so far — **Friedman (1999)** + modern GBDT libraries.

## Interview Relevance

Boosting interviews cover sequential residual fitting, learning rate, and overfit versus random forests.

## Sources

- [scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html) — deep-dive
- [Google Machine Learning Crash Course](https://developers.google.com/machine-learning/crash-course) — overview
- [Gradient boosting — Wikipedia](https://en.wikipedia.org/wiki/Gradient_boosting) — overview

## Key Concepts

Boosting builds an additive model:

```txt
F₀(x) = constant (e.g. log-odds base rate)
Fₘ(x) = Fₘ₋₁(x) + η · hₘ(x)     # hₘ = shallow tree on negative gradient
```

Each stage **hₘ** is a weak learner (usually a shallow [[Decision tree]]) trained on the **pseudo-residuals** of the loss (gradient of loss w.r.t. current prediction). Learning rate **η** shrinks each tree's contribution to reduce overfit.

```txt
Round 1: tree fixes biggest errors
Round 2: tree fixes what round 1 missed
...
Final: weighted sum of M small trees
```

**versus [[Random forest]]:** RF trains trees **in parallel** on bootstrap samples + random features (bagging). GBDT trains **sequentially**, each tree correcting prior bias — often higher accuracy, more tuning sensitivity.

**Loss linkage:** regression → MSE residuals; binary classification → log-loss → residuals on log-odds; ranking → LambdaRank-style gradients.

## Technical Details

### scikit-learn `HistGradientBoosting*` (preferred in sklearn ≥1.0)

```python
from sklearn.ensemble import HistGradientBoostingClassifier

clf = HistGradientBoostingClassifier(
    max_iter=200,           # boosting rounds (n_estimators equivalent)
    learning_rate=0.05,     # η — lower + more trees = smoother
    max_depth=6,
    min_samples_leaf=20,
    l2_regularization=1.0,  # leaf value shrinkage
    early_stopping=True,
    validation_fraction=0.1,
    n_iter_no_change=15,
    random_state=42,
)
clf.fit(X_train, y_train)
```

### XGBoost / LightGBM / CatBoost (production scale)

See [[xg boost]]. Typical starting grid:

| Param | Start | Notes |
|-------|-------|-------|
| `n_estimators` / `num_boost_round` | 500–2000 | Use early stopping |
| `learning_rate` | 0.03–0.1 | ↓ rate → ↑ trees |
| `max_depth` | 4–8 | Interaction depth |
| `subsample` | 0.7–0.9 | Row subsampling (stochastic GB) |
| `colsample_bytree` | 0.6–0.9 | Column subsampling |
| `min_child_weight` / `min_data_in_leaf` | tune on val | Overfit control |

```python
import xgboost as xgb

dtrain = xgb.DMatrix(X_train, label=y_train)
model = xgb.train(
    {"objective": "binary:logistic", "max_depth": 6, "eta": 0.05,
     "subsample": 0.8, "colsample_bytree": 0.8},
    dtrain,
    num_boost_round=2000,
    evals=[(dval, "val")],
    early_stopping_rounds=50,
)
```

## Pros/Cons or Trade-offs

- **Tiny tabular data (< few hundred rows)** — linear/logistic + strong regularization often generalizes better with less tuning.
- **Need online learning** — GBDT retrains are batch-heavy; consider linear models or incremental learners.
- **Strict interpretability for regulators** — single [[Decision tree]] or GAM may be required; explain boosted models with documented SHAP limits.
- **Already at latency budget with RF** — boosting gains may not justify 2–5× inference cost.

## Mistakes to Avoid

> [!WARNING]
> **Leakage through early stopping:** validation set must be truly held out; don't peek at test for round selection.

> [!WARNING]
> **Categorical handling differs by library:** CatBoost native; LightGBM `categorical_feature`; XGBoost needs encoding — inconsistent pipelines cause silent metric drops.

> [!WARNING]
> **Boosting amplifies label noise:** mislabeled rows get repeatedly emphasized; audit labels before heavy tuning.

> [!WARNING]
> **Interaction ≠ causation:** high feature importance on correlated features splits credit arbitrarily — use SHAP with care.

| Symptom | Check | Fix |
|---------|-------|-----|
| Train great, val collapses | `learning_rate` too high, too many rounds | Lower η; enable early stopping; ↑ `min_child_weight` / `min_samples_leaf` |
| Underfitting (both weak) | Too few rounds, depth too shallow | More estimators + early stop; slightly deeper trees |
| Training very slow | Dense wide matrix | `HistGradientBoosting`; LightGBM histogram; reduce features |
| Predictions all one class | Base rate skew, wrong objective | Check `scale_pos_weight`; class weights; PR curve |
| Wild variance across CV folds | Small data + high capacity | Stronger regularization; fewer features; nested CV |
| Serving latency high | Tree count × depth | Limit rounds; model distillation; ONNX + treelite |

