[[mysql]] [[mysql table]] [[mysql index]] [[OLTP]]

# MySQL table partitioning

> Split one logical table into physical partitions (by RANGE/LIST/HASH/KEY) — prune scans on time/tenant keys; **not** a substitute for indexing or sharding.

## Mental model

Partitioning divides rows by a **partition key** expression. Optimizer **partition pruning** skips irrelevant partitions on queries that constrain the key.

```
TABLE orders (partitioned by RANGE YEAR(order_date))
├── p2024  (rows 2024)
├── p2025  (rows 2025)
└── pmax   (catch-all)
```

Storage: one `.ibd` per partition (InnoDB file-per-table). Primary key **must include all columns used in partition expression** (MySQL 8 rules).

**Critical:** partitioning is defined at **CREATE TABLE** time. You cannot `ALTER TABLE t PARTITION BY …` on an arbitrary existing table without rebuild.

## Standard config / commands

### Create partitioned table (RANGE by date)

```sql
CREATE TABLE orders (
  id BIGINT NOT NULL,
  order_date DATE NOT NULL,
  customer_id INT NOT NULL,
  amount DECIMAL(12,2),
  PRIMARY KEY (id, order_date)  -- PK must include partition key
)
PARTITION BY RANGE (TO_DAYS(order_date)) (
  PARTITION p2024 VALUES LESS THAN (TO_DAYS('2025-01-01')),
  PARTITION p2025 VALUES LESS THAN (TO_DAYS('2026-01-01')),
  PARTITION pmax  VALUES LESS THAN MAXVALUE
);
```

### LIST partitioning (region)

```sql
PARTITION BY LIST COLUMNS(region) (
  PARTITION p_us VALUES IN ('US','CA'),
  PARTITION p_eu VALUES IN ('DE','FR','UK'),
  PARTITION p_rest VALUES IN (DEFAULT)  -- MySQL 8.0.23+ DEFAULT partition
);
```

### HASH / KEY (even spread, no range prune)

```sql
PARTITION BY HASH(customer_id) PARTITIONS 8;
```

### Add / drop partition (RANGE)

```sql
ALTER TABLE orders REORGANIZE PARTITION pmax INTO (
  PARTITION p2026 VALUES LESS THAN (TO_DAYS('2027-01-01')),
  PARTITION pmax  VALUES LESS THAN MAXVALUE
);

ALTER TABLE orders DROP PARTITION p2024;  -- deletes data in partition!
```

### Migrate existing non-partitioned table

```sql
-- 1. New partitioned empty table (DDL above)
-- 2. Copy data in batches
INSERT INTO orders_new SELECT * FROM orders_old WHERE order_date >= '2024-01-01';

-- 3. Atomic rename (maintenance window)
RENAME TABLE orders TO orders_old, orders_new TO orders;

-- Or pt-online-schema-change / gh-ost for large tables
```

### Verify pruning

```sql
EXPLAIN SELECT * FROM orders
WHERE order_date BETWEEN '2025-06-01' AND '2025-06-30';
-- partitions: p2025 only
```

### Constraints

- Unique indexes must include partition key columns.
- Foreign keys referencing partitioned tables were limited (check version).
- Subpartitioning available but increases operational complexity.

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Full table scan all partitions | WHERE missing partition key | Add key to query; fix app filters |
| Cannot add PRIMARY KEY | PK doesn't include partition expr | Redesign PK `(id, order_date)` |
| ALTER to partition fails | Existing table | Create new partitioned table + migrate |
| One partition huge | pmax catch-all absorbing everything | REORGANIZE; add future partitions proactively |
| DROP PARTITION data loss | DROP ≠ archive | Exchange partition to archive table first |
| Queries slower after partition | Wrong key (HASH on low-cardinality) | Use RANGE/LIST on time/tenant; index within partition |
| Replication lag on partition maintenance | DDL rewrites table | Online schema tool; off-peak REORGANIZE |

## Gotchas

> [!WARNING]
> **Can't partition existing table in place** — plan migration downtime or online schema change; see migration steps above.

> [!WARNING]
> **`MAXVALUE` partition** — if all new rows land in pmax, pruning fails for historical queries hitting pmax only.

> [!WARNING]
> **Global indexes don't exist** — secondary indexes are per-partition tree; very wide partitions hurt index efficiency.

> [!WARNING]
> **Partitioning ≠ sharding** — still one server; for write scale-out use application sharding or MySQL Cluster / Vitess.

## When NOT to use

- **Small tables (< tens of millions rows)** — index + archive job is simpler.
- **Queries without partition key in WHERE** — every partition scanned; worse than non-partitioned.
- **Heavy cross-partition joins** — design avoids joining partitioned fact without key alignment.

## Related

[[partitioning]] [[mysql]] [[mysql table]] [[mysql index]] [[mysql data migrations]]
