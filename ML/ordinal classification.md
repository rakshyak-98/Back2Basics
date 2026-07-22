[[multiclass classification]] [[binary classification]] [[ML Classifiers]] [[regression]]

# Ordinal classification

> Classes have a **natural order** (1★–5★, mild/moderate/severe) — respect ordering in loss and metrics, don't treat as nominal — **ordinal regression literature**.

---

## Mental model

Nominal multiclass treats "medium" vs "large" as equally wrong as "small" vs "large". Ordinal models encode **rank structure**:

```txt
Ratings: 1 < 2 < 3 < 4 < 5
Predicting 4 when truth is 5  →  small error
Predicting 1 when truth is 5  →  catastrophic error
```

Approaches:

| Approach | Idea |
|----------|------|
| **Ordinal regression / cumulative link** | K−1 binary thresholds (P(y > k)) |
| **Regression + round/clip** | Predict continuous, map to bucket |
| **Weighted loss multiclass** | Penalize far-off classes more |
| **Corn loss / coral** | Neural ordinal heads (modern) |

**Ordinal cross-entropy** (sometimes used) applies class weights by distance from true rank — not standard softmax CE.

---

## Standard config / commands

```python
import numpy as np
from sklearn.metrics import mean_absolute_error, cohen_kappa_score
from sklearn.ensemble import HistGradientBoostingRegressor

# Baseline: treat labels as numeric, regress, clip
y_train_ord = y_train.astype(float)
reg = HistGradientBoostingRegressor(max_iter=200, random_state=42)
reg.fit(X_train, y_train_ord)
pred = np.clip(np.rint(reg.predict(X_test)), 1, 5).astype(int)

print("MAE (ordinal):", mean_absolute_error(y_test, pred))
print("Quadratic weighted kappa:", cohen_kappa_score(y_test, pred, weights="quadratic"))
```

### mord library (ordinal logistic)

```python
from mord import LogisticAT  # All-Threshold variant

clf = LogisticAT()
clf.fit(X_train, y_train)  # y must be 0..K-1 ordered integers
pred = clf.predict(X_test)
```

Use **quadratic weighted kappa** or **MAE on ranks** — not plain accuracy.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Treating as multiclass, odd errors | Loss ignores distance | Switch to ordinal/regression |
| Regression predicts 3.7 | Unbounded head | Round + clip; ordinal logistic |
| Classes collapsed to middle | Imbalance | Class weights; focal loss variants |
| Good accuracy, bad user UX | Far-off errors hidden | Report MAE / off-by-2 rate |
| Label order ambiguous | Domain definition | Lock encoding doc (low=0 vs low=1) |

---

## Gotchas

> [!WARNING]
> **Standard softmax** on star ratings wastes order information and treats all misclassifications equally in the loss (unless you post-hoc weight).

> [!WARNING]
> **Shuffling class IDs** — ordinal requires consistent integer order 0…K−1.

---

## When NOT to use

- **Unordered categories** (cat/dog/bird) — [[multiclass classification]].
- **True continuous measurement** — [[regression]] without bucketing.
- **Binary decision** — [[binary classification]].

---

## Related

[[multiclass classification]] · [[regression]] · [[ML Classifiers]] · [[Mean Average Precision (MAP)]] · [[Visualization/Residual plot]]
