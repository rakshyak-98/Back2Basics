[[ML Classifiers]] [[binary classification]] [[regression]] [[Model/Linear regression]] [[scikitlearn]]

# Support Vector Machines (SVM)

> Find the **maximum-margin** separating hyperplane (or ε-tube for regression) — kernel trick maps to high-D implicitly — **Cortes & Vapnik (1995)**.

---

## Mental model

**Hard margin:** separate classes with widest gap. **Soft margin (C):** allow slack ξᵢ — trade misclassification vs margin width.

```txt
min  ½‖w‖² + C Σ ξᵢ
s.t. yᵢ(w·φ(xᵢ) + b) ≥ 1 − ξᵢ
```

**Kernel K(x,x')** replaces explicit φ — common **RBF** (Gaussian) for nonlinear boundaries. Support vectors are training points on or inside the margin — prediction depends mostly on them, not all data.

| Mode | sklearn class | Key param |
|------|---------------|-----------|
| Binary classify | `SVC` | `C`, `gamma` (RBF) |
| Multiclass | `SVC` (OvO/OvR) | same |
| Regression | `SVR` | `C`, `epsilon` |

SVMs shine on **medium-sized, dense** data; struggle on **large sparse text** unless linear kernel + careful scaling.

---

## Standard config / commands

```python
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV

pipe = Pipeline([
    ("scale", StandardScaler()),  # mandatory for RBF
    ("svc", SVC(kernel="rbf", class_weight="balanced", probability=False)),
])

param_grid = {
    "svc__C": [0.1, 1, 10],
    "svc__gamma": ["scale", 0.01, 0.1],
}
search = GridSearchCV(pipe, param_grid, cv=5, scoring="f1_macro", n_jobs=-1)
search.fit(X_train, y_train)
```

### Linear SVM (large sparse text-like)

```python
from sklearn.svm import LinearSVC
clf = LinearSVC(C=1.0, class_weight="balanced", max_iter=10_000)
```

### SVR for regression

```python
from sklearn.svm import SVR
svr = SVR(kernel="rbf", C=10, epsilon=0.1)
```

`probability=True` on `SVC` wraps Platt scaling — slow; use `decision_function` + calibrate separately if needed.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Training never finishes | n > 100k, RBF | `LinearSVC` or [[Random forest]] |
| All one class | C too high/low, scaling | Grid search C; StandardScaler |
| Test perf random | Unscaled features | Pipeline with scaler |
| Memory blowup | RBF on 500k rows | Subsample; linear kernel |
| Platt probs miscalibrated | `probability=True` | CalibratedClassifierCV |

---

## Gotchas

> [!WARNING]
> **RBF γ too large** — overfits every point (memorization). Too small — underfits (linear-ish).

> [!WARNING]
> **No native missing values** — impute in [[data preprocessing]] pipeline.

---

## When NOT to use

- **Huge datasets (millions+ rows)** — [[Gradient boosting]] / linear models scale better.
- **Need feature importances for compliance** — prefer [[Decision tree]] or linear models.
- **Image/audio deep learning** — CNNs / transformers dominate.

---

## Related

[[ML Classifiers]] · [[binary classification]] · [[regression]] · [[Model/Linear regression]] · [[data preprocessing]]
