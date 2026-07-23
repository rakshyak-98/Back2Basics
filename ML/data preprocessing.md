[[scikitlearn]] [[estimator]] [[supervised learning]] [[Model/Linear regression]] [[Decision tree]]

# Data preprocessing

> Turn raw tables into **leak-safe, scaled, encoded** matrices estimators can fit — garbage in → un-debuggable models — **scikit-learn Pipeline docs**.

---

## Mental model

Preprocessing runs **before** the learner sees data. Order matters:

```txt
load → clean types → handle missing → encode categoricals → scale (if needed) → split → fit
```

Fit transformers on **training data only**; apply same params to val/test. Putting `fit` on full dataset before split = **leakage** (val scores lie).

| Step | Tree models | Linear / SVM / NN |
|------|-------------|-------------------|
| Missing values | Native or impute | Usually impute |
| Categoricals | Ordinal / target enc (careful) | One-hot / target enc |
| Scaling | Skip | StandardScaler / RobustScaler |
| Outliers | Robust to some | Clip or RobustScaler |

---

## Standard config / commands

```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier

num_cols = ["age", "income"]
cat_cols = ["region"]

preprocess = ColumnTransformer([
    ("num", Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scale", StandardScaler()),
    ]), num_cols),
    ("cat", Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("oh", OneHotEncoder(handle_unknown="ignore")),
    ]), cat_cols),
])

pipe = Pipeline([
    ("prep", preprocess),
    ("clf", RandomForestClassifier(random_state=42)),
])

X_train, X_test, y_train, y_test = train_test_split(
    df.drop("target", axis=1), df["target"], test_size=0.2, stratify=df["target"], random_state=42
)
pipe.fit(X_train, y_train)
```

### Outliers (exploratory — don't delete blindly)

```python
from scipy import stats
z = np.abs(stats.zscore(df[num_cols], nan_policy="omit"))
# flag rows where any |z| > 3 — investigate domain validity before drop
```

### Missingness indicator (often helps)

```python
for c in num_cols:
    df[f"{c}_was_missing"] = df[c].isna().astype(int)
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Great CV, bad prod | Fit on full data before split | Pipeline inside CV; `fit` only on train fold |
| `ValueError: unknown category` | New category in prod | `handle_unknown="ignore"` or fallback bucket |
| Exploding coefficients | Unscaled features | StandardScaler in Pipeline |
| All NaN after join | Merge keys, dtypes | Assert row counts; `df.info()` |
| Model worse after "cleaning" | Removed signal (outliers = fraud) | Domain review; RobustScaler vs drop |

---

## Gotchas

> [!WARNING]
> **Target encoding on full dataset** leaks label statistics — encode inside CV folds only (`CategoryEncoders` + pipeline).

> [!WARNING]
> **Mean imputation on skewed data** — use median; consider missingness flags.

---

## When NOT to use

- **Raw deep learning on images/text** — use domain-specific augmentations, not tabular imputers.
- **Streaming features with strict SLA** — precompute offline features in a feature store; don't refit heavy pipelines per request.

---

## Related

[[scikitlearn]] · [[estimator]] · [[supervised learning]] · [[Visualization/Residual plot]] · [[Model/Linear regression]]
