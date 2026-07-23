[[Python/wheel]] [[Data structure/dsa genera formula]]

# pandas

> Columnar DataFrame library for load → transform → analyze → export workflows in Python.

## Mental model

A **DataFrame** is labeled columns (Series) with a shared index. Operations are vectorized (C-backed) when possible. Missing data is `NaN`. Dtype matters: object vs int vs category affects memory and speed. Prefer explicit dtypes on ingest for prod pipelines.

## Standard config / commands

### Load and inspect

```python
import pandas as pd

df = pd.read_csv("data.csv", dtype={"id": str})  # keep leading zeros
df.info()
df.describe()
df.head()
```

### Safe numeric coercion

```python
df = df.apply(pd.to_numeric, errors="coerce").fillna(0).astype(int)
# errors='coerce' → invalid becomes NaN, then fillna
```

### Common transforms

```python
df.groupby("region")["sales"].sum()
df.merge(other, on="id", how="left")
df.query("age > 30")
df.to_parquet("out.parquet", index=False)   # faster reread than CSV
```

### Performance habits

```python
df["col"].astype("category")     # low-cardinality strings
df.filter(regex="^metric_")      # column subset early
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `SettingWithCopyWarning` | Chained indexing | Use `.loc[]` assignment |
| Memory blowup | `df.memory_usage(deep=True)` | Downcast dtypes; read columns subset |
| Merge explosion | Key duplicates | `validate="m:1"`; dedupe keys |
| NaN after math | Dtype object | Coerce numeric first |
| Slow loop over rows | `iterrows` | Vectorize or `.apply` axis=0 sparingly |

## Gotchas

> [!WARNING]
> **`fillna(0)` after coerce** — hides bad data; log/coerce count first in ETL.
>
> **CSV locale commas** — specify `decimal=','` for EU files.
>
> **Timezone-naive datetimes** — always UTC in storage.

## When NOT to use

- Don't use pandas for row-by-row OLTP — use SQL/ORM.
- Don't load 100GB CSV on a laptop — use DuckDB/Polars/spark for out-of-core.

## Related

[[Python/wheel]] [[Database/OLAP]] [[Database/mysql/mysql dump]]
