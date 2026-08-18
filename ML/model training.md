# Model training

## Evaluation

Common metrics:
- **Classification:** accuracy, precision, recall, F1 score
- **Regression:** mean squared error (MSE)

### How to tell if the model is underfitting or overfitting?

- **K-fold cross-validation** — if scores swing a lot between folds, the model may be unstable or overfitting.
- **Regularization (L1/L2)** — if test score drops when you add regularization, the model was likely overfitting.

### F1 score

- One number that balances precision and recall.
- Useful when classes are imbalanced (e.g. 95% negative, 5% positive).

## Test size

`test_size` sets how much data goes to the test set.

| Value | When to use |
|-------|-------------|
| `0.2` | Default — good split for most datasets |
| `0.25` | Large dataset — still enough train data |
| `0.1` | Very large dataset — small % still means many test rows |

> [!NOTE] Small dataset? Use a bigger test split (e.g. 30%) so evaluation has enough samples.

> [!NOTE] Complex models need more training data — consider a smaller test split.

## Random state

`random_state` controls how rows are shuffled before train/test split.

- Use the **same value** for splitting and for any random steps in training.
- Different splits can hide weak spots — try a few values to check stability.
- Same seed → same split every run (good for debugging).

Why it matters:
- Mimics real-world variation in train and test data.
- Surfaces hidden weaknesses from odd data patterns.
- Reduces luck from one lucky split.

### Data features and labels

- If features or labels are too similar, the model learns little.
- Same number of features and labels is normal — what matters is **variation** in the data.
- Too many correlated or useless features → model underperforms.
- **Feature engineering:** pick useful features; transform data when it helps.
