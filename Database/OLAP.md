[[Database]] [[OLTP]] [[Data access patterns]] [[SQL]] [[SQL normalization]] [[BASE]] [[mysql]] [[SQL/postgres]]

# OLAP

> Online Analytical Processing — large scans and aggregations over historical data where throughput and columnar compression beat single-row latency.

```txt
        OLAP ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers contrast OLAP with [[OLTP]]: schema shape, storage (row vs colum…

## Sources
- Kleppmann, *Designing Data-Intensive Applications*, Ch. 3 — deep-dive
- [Wikipedia — Online analytical processing](https://en.wikipedia.org/wiki/Online_analytical_processing) — overview
- [Google BigQuery docs — columnar storage concepts](https://cloud.google.com/bigquery/docs/storage_overview) — overview
- Codd, E.F., OLAP-related papers / star schema practice — overview

## Key Concepts
- **Scan-heavy queries:** millions of rows, few columns, heavy aggregation.
- **Columnar storage:** read only needed columns (Parquet, ClickHouse, BigQuery).
- **Star / snowflake schema:** fact table + dimensions — often denormalized vs [[SQL normalization]].
- **ETL / ELT:** copy from [[OLTP]] sources; lag and [[BASE]]-style freshness are acceptable.
- **Isolation from primary:** ad-hoc SQL must not evict hot OLTP pages from the buffer pool.


- **Core:** OLAP workloads answer aggregate questions over wide time ranges and dimension…

## Technical Details
- Typical query shape:

```sql
SELECT region, SUM(revenue)
FROM sales_fact
WHERE sold_date BETWEEN '2024-01-01' AND '2024-12-31'
GROUP BY region;
```

- These patterns stress **sequential I/O** and **CPU for aggregation**, not ind…

- Architecture patterns:

| Pattern | Why |
|---------|-----|
| Columnar stores | Skip unread columns; compress well |
| Star schema | Fast joins from facts to dimensions for BI |
| CDC / batch ETL | Feed warehouse without locking OLTP writers |
| Materialized views | Pre-aggregate hot dashboards |

```txt
OLTP primary ──CDC/ETL──► warehouse / column store ──► BI / notebooks
                 │
                 └── optional: reporting replica (monitor lag)
```

- *What breaks first if OLAP and OLTP share one MySQL primary?* Buffer pool evi…

## Mistakes to Avoid
- **Mistake:** Running ad-hoc year-long `GROUP BY` on the OLTP primary at peak …
- **Mistake:** Treating warehouse tables as authoritative for inventory deducti…
- **Mistake:** Ignoring replica lag when “live” dashboards read from a replica
- **Mistake:** Over-normalizing a warehouse until every report becomes a ten-wa…

## Pros/Cons or Trade-offs
- **Pro:** Cheap large aggregates; schema tuned for questions, not write paths.
- **Con:** Stale data; complex pipelines; not suitable as system of record for money movement.
- **Trade-off:** Freshness (near-real-time CDC) vs batch cost and simplicity.

## Comparison
- vs [[OLTP]]: few rows / high concurrency / normalized vs many rows / scan thr…


### Use cases
- Nightly load of orders into a star schema for finance dashboards
