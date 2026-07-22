[[OLTP]] [[Data access patterns]] [[ACID]] [[Database design]] [[mysql]]

# OLAP (Online Analytical Processing)

> **Read-heavy analytics** — scans, aggregates, GROUP BY across dimensions — optimized for dashboards and BI, not row-by-row checkout. Contrast [[OLTP]]: many small writes, index-point lookups, [[ACID]] transactions.

## Mental model

OLTP answers **"create this order now"** (few rows, ms latency). OLAP answers **"revenue by region last 36 months"** (millions–billions of rows, seconds OK). OLAP stores favor **columnar layout**, **compression**, **star/snowflake schemas**, **pre-aggregations**, and **eventual consistency** from ETL — not row locks on hot paths.

```
OLTP (Postgres/MySQL) ──ETL/CDC──► OLAP (BigQuery, Snowflake, ClickHouse, Redshift)
         │                                    │
    source of truth                      dashboards, ML features
```

Running heavy OLAP on primary OLTP **without isolation** is a classic prod outage ([[Database mistakes]]).

## Standard config / commands

### When to split OLTP vs OLAP

| Signal | Action |
|--------|--------|
| Reporting queries slow OLTP | Read replica + timeout, or warehouse |
| Full table scans on facts | Columnar warehouse |
| Cross-system metrics | ETL to single OLAP |
| Real-time-ish analytics | CDC stream (Debezium) → ClickHouse/Druid |

### Star schema (warehouse baseline)

```
fact_sales (date_key, product_key, customer_key, amount)
    ├── dim_date
    ├── dim_product
    └── dim_customer
```

- **Facts** = measurable events; **dims** = filter/group attributes.
- Denormalize dims for query simplicity; normalize OLTP separately.

### ETL patterns

```sql
-- nightly batch (idempotent load)
INSERT INTO warehouse.fact_orders
SELECT o.id, d.date_key, SUM(li.qty * li.price)
FROM oltp.orders o
JOIN oltp.line_items li ON ...
JOIN dim_date d ON d.date = DATE(o.created_at)
WHERE o.updated_at >= :watermark;
```

- **CDC** (preferred near-real-time): logical replication / Debezium → object storage → warehouse external tables.

### Engine cheat sheet

| Engine | Sweet spot |
|--------|------------|
| BigQuery / Snowflake | Managed, separate storage/compute |
| ClickHouse | Fast aggregations, high ingest |
| Redshift | AWS-native, spectrum to S3 |
| Postgres + Citus/columnar ext | Small team, moderate scale |
| Materialized views on replica | Lightweight stepping stone |

### Query habits

- Filter on **partition key** (date) first — partition pruning.
- Avoid `SELECT *` on wide fact tables.
- Pre-aggregate with **rollup tables** or MVs for dashboards hit every 30s.

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Dashboard timeout | Full scan; missing partition filter | Add date predicate; sort key; MV |
| OLTP prod slow during report | Report on primary | Move to replica/warehouse; kill query |
| ETL duplicate rows | Non-idempotent load | Merge/upsert on natural key; dedupe window |
| Stale numbers vs OLTP | Batch lag; failed job | Alert on watermark; rerun from checkpoint |
| Cost spike (BigQuery) | Bytes scanned | Partition/cluster; avoid SELECT *; slot caps |
| Schema drift break ETL | OLTP migration without pipeline update | Contract tests; versioned exports |

## Gotchas

> [!WARNING]
> **Materialized view on OLTP primary refreshed every minute** — still write/load pressure; prefer warehouse.

> [!WARNING]
> **COUNT(*) on billion-row fact without filter** — always bound time range in UI defaults.

> [!WARNING]
> **JOIN OLTP live in Metabase** — one analyst can lock or OOM small Postgres.

> [!WARNING]
> **Eventually consistent OLAP** — don't use warehouse balance for fraud check without sync guarantee.

## When NOT to use

- **Operational reads in user request path** — use OLTP + cache.
- **OLAP engine as primary app DB** — poor fit for high-frequency row updates ([[OLTP]]).
- **Premature Snowflake for 10GB** — replica + indexed aggregates may suffice ([[Data access patterns]]).

## Related

[[OLTP]] · [[Data access patterns]] · [[ACID]] · [[Database design]] · [[Database mistakes]] · [[connection pooling]]
