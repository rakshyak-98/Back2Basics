[[Database]] [[OLTP]] [[Data access patterns]] [[SQL]] [[SQL normalization]] [[BASE]] [[mysql]] [[SQL/postgres]]

# OLAP

> Online Analytical Processing — large scans and aggregations over historical data where throughput and columnar compression beat single-row latency.





## Interview Relevance
Interviewers contrast OLAP with [[OLTP]]: schema shape, storage (row vs column), and where to run heavy reports. Signal: you protect the primary with replicas or a warehouse and accept eventual consistency for analytics.

## Sources
- Kleppmann, *Designing Data-Intensive Applications*, Ch. 3 — deep-dive
- [Wikipedia — Online analytical processing](https://en.wikipedia.org/wiki/Online_analytical_processing) — overview
- [Google BigQuery docs — columnar storage concepts](https://cloud.google.com/bigquery/docs/storage_overview) — overview
- Codd, E.F., OLAP-related papers / star schema practice — overview

## Core Definition
OLAP workloads answer aggregate questions over wide time ranges and dimensions. Engines optimize sequential I/O, compression, and CPU for GROUP BY — not millisecond point updates.

## Key Concepts
- **Scan-heavy queries:** millions of rows, few columns, heavy aggregation.
- **Columnar storage:** read only needed columns (Parquet, ClickHouse, BigQuery).
- **Star / snowflake schema:** fact table + dimensions — often denormalized vs [[SQL normalization]].
- **ETL / ELT:** copy from [[OLTP]] sources; lag and [[BASE]]-style freshness are acceptable.
- **Isolation from primary:** ad-hoc SQL must not evict hot OLTP pages from the buffer pool.

## Technical Details
Typical query shape:

```sql
SELECT region, SUM(revenue)
FROM sales_fact
WHERE sold_date BETWEEN '2024-01-01' AND '2024-12-31'
GROUP BY region;
```

These patterns stress **sequential I/O** and **CPU for aggregation**, not index point lookups.

Architecture patterns:

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

*What breaks first if OLAP and OLTP share one MySQL primary?* Buffer pool eviction of hot OLTP pages and replication lag on replicas used for reporting.

## Real-World Applications
Nightly load of orders into a star schema for finance dashboards; analysts query BigQuery/Snowflake/ClickHouse while checkout stays on PostgreSQL/MySQL. Read replicas with lag SLOs for lighter internal reports.

## Pros/Cons or Trade-offs
- **Pro:** Cheap large aggregates; schema tuned for questions, not write paths.
- **Con:** Stale data; complex pipelines; not suitable as system of record for money movement.
- **Trade-off:** Freshness (near-real-time CDC) vs batch cost and simplicity.

## Comparison
vs [[OLTP]]: few rows / high concurrency / normalized vs many rows / scan throughput / denormalized. vs [[Data access patterns]]: OLAP is the analytics end of the access spectrum. vs [[Vector database]]: similarity search is another specialized store — not a substitute for dimensional analytics.

## Mistakes to Avoid
- Running ad-hoc year-long `GROUP BY` on the OLTP primary at peak traffic.
- Treating warehouse tables as authoritative for inventory deduction.
- Ignoring replica lag when “live” dashboards read from a replica.
- Over-normalizing a warehouse until every report becomes a ten-way join tax.
