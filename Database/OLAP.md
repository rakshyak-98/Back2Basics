[[Database]] [[OLTP]] [[Data access patterns]] [[SQL]]

# OLAP

> Online Analytical Processing—large scans and aggregations over historical data where throughput and columnar compression beat single-row latency.

## Typical queries

```sql
SELECT region, SUM(revenue)
FROM sales_fact
WHERE sold_date BETWEEN '2024-01-01' AND '2024-12-31'
GROUP BY region;
```

These patterns stress **sequential I/O** and **CPU for aggregation**, not index point lookups.

## Architecture patterns

- **Columnar stores** (Parquet, ClickHouse, BigQuery) — read only needed columns
- **Star schema** — fact table + dimension tables; trades [[SQL normalization]] for scan speed
- **ETL/ELT** from [[OLTP]] source — eventual consistency acceptable ([[BASE]])

## Isolation from production

Never let ad-hoc analyst queries saturate the primary. Use read replicas with lag monitoring, or a dedicated warehouse fed by change-data-capture.

*What breaks first if OLAP and OLTP share one MySQL primary?* Buffer pool eviction of hot OLTP pages and replication lag on replicas used for reporting.

## Sources

- Kleppmann, *DDIA*, Ch. 3
- Wikipedia — [Online analytical processing](https://en.wikipedia.org/wiki/Online_analytical_processing)
