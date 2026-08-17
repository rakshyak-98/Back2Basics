[[Python]] [[wheel]] [[Database/OLAP]] [[GIL (Global interpreter lock)]]

# pandas

> Tabular data library for Python — load, clean, join, aggregate, and export DataFrames for analysis.

```txt
        pandas ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Data/backend interviews test vectorized thinking: groupby/merge correctness, …

## Sources
- [pandas documentation](https://pandas.pydata.org/docs/) — deep-dive
- [pandas user guide — 10 minutes to pandas](https://pandas.pydata.org/docs/user_guide/10min.html) — overview
- [Wikipedia — pandas (software)](https://en.wikipedia.org/wiki/Pandas_(software)) — overview

## Key Concepts
- **Labels matter:** index/columns drive joins and alignment
- **dtypes + memory:** object columns and 64-bit defaults blow RAM
- **Split-apply-combine:** `groupby` → aggregate/transform/filter — core analysis pattern.
- **Copy vs view:** chained indexing can return views or copies


- **Core:** pandas centers on `Series` (1-D) and `DataFrame` (2-D labeled columns). Opera…

## Technical Details
```python
import pandas as pd

df = pd.read_csv("data.csv", dtype={"id": str})
df.info()
df.describe()
df.head()

df = df.apply(pd.to_numeric, errors="coerce")  # bad cells → NaN
df.groupby("region")["sales"].sum()
df.merge(other, on="id", how="left", validate="m:1")
df.query("age > 30")
df.to_parquet("out.parquet", index=False)

df["col"] = df["col"].astype("category")  # low-cardinality strings
```

| Symptom | Check | Fix |
|---------|-------|-----|
| `SettingWithCopyWarning` | Chained `df[...][...] =` | `.loc[row, col] = value` |
| Memory blowup | `df.memory_usage(deep=True)` | Downcast; read usecols; categories |
| Merge row explosion | Duplicate keys | `validate=`; dedupe |
| Slow `iterrows` | Row Python loop | Vectorize / boolean masks |

## Mistakes to Avoid
- **Mistake:** `fillna(0)` after coerce without counting how many values you in…
- **Mistake:** Timezone-naive timestamps in storage — standardize on UTC
- **Mistake:** Loading a huge CSV on a laptop when an out-of-core engine fits t…

## Pros/Cons or Trade-offs
- **Pro:** Fast path from messy files to aggregates; huge ecosystem.
- **Con:** Single-machine memory ceiling — multi-GB+ often wants Polars/DuckDB/Spark; not for OLTP request paths.

## Comparison
- vs SQL: SQL shines in-database; pandas shines in-process glue and ad-hoc exploration.
- vs NumPy: NumPy is homogeneous arrays; pandas adds labels, missing data, heterogeneous columns.


### Use cases
- Nightly finance ETL: read CSVs with explicit dtypes, coerce numerics, aggrega…
