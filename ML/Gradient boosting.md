[[Decision tree]] [[Random forest]] [[xg boost]] [[scikitlearn]] [[regression]] [[binary classification]] [[Model/Linear regression]] [[multiclass classification]]

# Gradient boosting

> Sequential ensemble: each new tree fits the **residual errors** of the ensemble so far — **Friedman (1999)** + modern GBDT libraries.

```txt
        Gradient boosting ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Interview Relevance
- **Interview probes:** Boosting interviews cover sequential residual fitting, learning rate, and ove…

## Sources
- [scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html) — deep-dive
- [Google Machine Learning Crash Course](https://developers.google.com/machine-learning/crash-course) — overview
- [Gradient boosting — Wikipedia](https://en.wikipedia.org/wiki/Gradient_boosting) — overview

## Key Concepts
Boosting builds an additive model:

```txt
F₀(x) = constant (e.g. log-odds base rate)
- **Note:** Fₘ(x) = Fₘ₋₁(x) + η · hₘ(x) # hₘ = shallow tree on negative gradient
```

- **Note:** Each stage **hₘ** is a weak learner (usually a shallow [[Decision tree]]) tra…

```txt
Round 1: tree fixes biggest errors
Round 2: tree fixes what round 1 missed
...
Final: weighted sum of M small trees
```

- **Note:** **versus [[Random forest]]:** RF trains trees **in parallel** on bootstrap sa…

- **Note:** **Loss linkage:** regression → MSE residuals

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

- See [[xg boost]].
- Typical starting grid:

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

## Pros/Cons or Trade-offs
- **Tiny tabular data (< few hundred rows)**
- **Need online learning**
- **Strict interpretability for regulators**
- **Already at latency budget with RF**
