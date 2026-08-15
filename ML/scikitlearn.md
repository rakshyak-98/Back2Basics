[[ML]] [[model tranning]] [[data preprocessing]] [[Random forest]] [[Gradient boosting]]

# scikitlearn

> scikit-learn is the go-to Python library for classical ML — estimators, pipelines, and metrics with a fit/predict API.

## Interview Relevance

sklearn literacy covers estimators, pipelines, cross-validation, and avoiding leakage in preprocessing.

## Sources

- [scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html) — deep-dive
- [Google Machine Learning Crash Course](https://developers.google.com/machine-learning/crash-course) — overview

## Key Concepts

```txt
Pipeline([preprocess, model]).fit(X_train, y_train).predict(X_test)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Estimator** | Objects with fit | “Classifier/regressor API.” |
| **Transformer** | fit/transform | “Scaler, encoder.” |
| **Pipeline** | Chain steps | “One fit for all.” |
| **CV** | Cross-validate | “`cross_val_score` / GridSearch.” |

## Technical Details

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
pipe = Pipeline([
  ('scale', StandardScaler()),
  ('clf', LogisticRegression(max_iter=1000)),
])
pipe.fit(X_train, y_train)
pipe.score(X_test, y_test)
```

| Knob | Why it matters |
|------|----------------|
| Pipeline | Scaler stats from train only |
| `n_jobs` | Parallel CV |
| `class_weight` | Imbalance |

## Pros/Cons or Trade-offs

- **Deep learning on GPU** — PyTorch/TF.
- **Huge distributed training** — Spark/XGBoost distributed stacks.

## Mistakes to Avoid

> [!WARNING]
> **fit on full dataset then split** — leaks; always split first.

> [!WARNING]
> **sparse vs dense** — some models need one or the other after encoding.

| Symptom | Check | Fix |
|---------|-------|-----|
| Shape errors | column mismatch | Same columns; ColumnTransformer |
| ConvergenceWarning | max_iter / scale | Scale features; raise iters |
| Leakage | preprocess outside pipeline | Put all steps inside |
| Slow GridSearch | huge grid | RandomSearch; fewer params |

