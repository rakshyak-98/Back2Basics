[[ML]] [[scikitlearn]] [[data preprocessing]]

# model tranning

> Training fits model parameters on labeled data — split, fit, validate, then lock the test set.

---

## How it works

```txt
raw → preprocess (fit on train only) → train → validate → test once
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Train/val/test** | Fit / tune / report | “Never tune on test.” |
| **Overfit** | Memorize train | “Val gap means regularize.” |
| **Cross-validation** | Rotate folds | “Small data honesty.” |
| **Early stopping** | Halt on val plateau | “Stop before overfit.” |

---


## Configuration and commands

```python
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y)
# fit preprocessors on X_train only, then transform X_test
model.fit(X_train, y_train)
print(model.score(X_test, y_test))
```

| Knob | Why it matters |
|------|----------------|
| Stratify | Preserve class ratios |
| Random seed | Reproducible splits |
| Pipeline | Prevent leakage |

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| Amazing metrics, bad prod | test leakage | Rebuild honest split |
| Underfit | high train error | Richer model / features |
| Overfit | train≫val | Regularize; more data |
| Unstable scores | tiny test | Cross-val; bigger holdout |

---


## Gotchas

> [!WARNING]
> **Scaling fit on all data** — classic leakage; fit scaler on train only.

> [!WARNING]
> **Peeking at test repeatedly** — test becomes validation in disguise.

---


## When not to use

- **No labels** — unsupervised / pretrained embeddings first.
- **One-shot demo** — still keep a holdout if you’ll claim accuracy.


## Related

[[scikitlearn]] [[data preprocessing]] [[supervised learning]]

## Sources

- [Wikipedia — model tranning](https://en.wikipedia.org/wiki/model_tranning)
