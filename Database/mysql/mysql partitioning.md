[[partitioning]] [[mysql data partition]] [[Data access patterns]] [[mysql table]] [[MySQL Events]] [[MySQL CLI]]

# mysql partitioning

> MySQL table partitioning splits one logical table into multiple physical segments on a single server — enabling partition pruning for queries that filter on the partition key and cheap retention by dropping old partitions.

---

## Why It Matters

Partitioning is not sharding — all partitions live on one MySQL instance. The payoff is **pruning** (the optimizer skips partitions that cannot contain matching rows) and **retention** (`DROP PARTITION` removes a year's data instantly vs `DELETE` scanning millions of rows). The cost is schema rigidity: every unique index must include the partition expression columns, foreign keys have limitations, and bulk loads fire per-row overhead on partitioned tables with triggers.

---

## Sources

- [MySQL Reference Manual — Partitioning Overview](https://dev.mysql.com/doc/refman/en/partitioning-overview.html) — When partitioning helps, supported engines, and high-level types.
- [MySQL Reference Manual — Partitioning Types](https://dev.mysql.com/doc/refman/en/partitioning-types.html) — RANGE, LIST, HASH, KEY, and subpartitioning syntax with examples.
- [MySQL Reference Manual — Partitioning Limitations](https://dev.mysql.com/doc/refman/en/partitioning-limitations.html) — The unique-key-must-include-partition-columns rule and FK restrictions.

---

## Key Concepts

### Partition types

| Type | Partition key | Use case |
|------|---------------|----------|
| **RANGE** | Continuous ranges (`YEAR(created_at)`, `TO_DAYS(date)`) | Time-series retention by month/year |
| **LIST** | Discrete values (`region IN ('us','eu')`) | Geographic or categorical split |
| **HASH** | `HASH(user_id)` or `KEY(column)` | Even distribution when range is unknown |
| **KEY** | MySQL internal hashing | Similar to HASH; uses server hashing function |

### The unique-key rule (critical)

**Every unique index (including PRIMARY KEY) must include all columns used in the partition expression.** You cannot have `PRIMARY KEY (id)` alone on a table `PARTITION BY RANGE (YEAR(created_at))` — the PK must be `(id, created_at)` or include the partition expression column.

### Pruning

Queries must constrain the partition key for the optimizer to skip partitions:

```sql
-- Prunes to 2024 partition only
SELECT * FROM events WHERE created_at BETWEEN '2024-01-01' AND '2024-12-31';

-- Scans ALL partitions — no pruning
SELECT * FROM events WHERE user_id = 42;  -- if partitioned by created_at
```

### Subpartitioning

```sql
PARTITION BY RANGE (YEAR(created_at))
SUBPARTITION BY HASH (user_id)
SUBPARTITIONS 4 (
  PARTITION p2023 VALUES LESS THAN (2024),
  PARTITION p2024 VALUES LESS THAN (2025)
);
```

Outer RANGE for retention; inner HASH for parallelism within a year.

---

## Technical Details

### RANGE partition by year

```sql
CREATE TABLE events (
  id BIGINT NOT NULL,
  created_at DATETIME NOT NULL,
  payload JSON,
  PRIMARY KEY (id, created_at)   -- PK includes partition key
) ENGINE=InnoDB
PARTITION BY RANGE (YEAR(created_at)) (
  PARTITION p2023 VALUES LESS THAN (2024),
  PARTITION p2024 VALUES LESS THAN (2025),
  PARTITION p_future VALUES LESS THAN MAXVALUE
);
```

### Drop old data (instant)

```sql
ALTER TABLE events DROP PARTITION p2023;   -- metadata operation, not row-by-row DELETE
```

### Inspect partitions

```sql
SELECT PARTITION_NAME, TABLE_ROWS, DATA_LENGTH
FROM information_schema.PARTITIONS
WHERE TABLE_NAME = 'events';

EXPLAIN PARTITIONS SELECT * FROM events WHERE created_at >= '2024-06-01';
```

### Alternatives when partitioning is wrong

| Need | Better approach |
|------|-----------------|
| Read scaling | Read replicas for [[OLAP]] queries |
| Write scaling beyond one server | [[database sharding]] — multiple MySQL instances |
| Simple time-based cleanup | Archive table + [[MySQL Events]] scheduled DELETE |
| Query performance | Proper indexes on [[mysql table]] — partitioning is not a substitute |

---

## Mistakes to Avoid

- Designing `PRIMARY KEY (id)` alone on a RANGE(`created_at`) table — DDL will fail or force a redesign.
- Subpartitioning without measuring pruning benefit — added complexity for marginal gain.
- Using partitions as a substitute for missing indexes on the partition key.
- Bulk `INSERT … SELECT` without accounting for per-partition index maintenance cost.
- Assuming partitioning works on all engines — only InnoDB and a few others support it.

---

## Pros/Cons or Trade-offs

| Pro | Con |
|-----|-----|
| Partition pruning on time-range queries | Unique-key constraint reshapes entire schema |
| `DROP PARTITION` for instant retention | FK limitations between partitioned tables |
| Expresses retention policy in DDL | Misleading if queries do not filter partition key |

---

## Comparison

| vs | Distinction |
|----|-------------|
| [[mysql data partition]] | Operational examples and pruning verification |
| [[partitioning]] | General database partitioning concepts |
| Sharding | Partitions = one server; shards = multiple servers |

---

## Use cases

- `events` table with billions of rows: RANGE by year, drop partitions older than 3 years monthly.
- SaaS audit log: LIST by `tenant_region` when queries always filter by region.
- Staging environment: HASH by `user_id` to spread load evenly when time-based retention is not needed.
