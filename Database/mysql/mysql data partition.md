[[mysql partitioning]] [[partitioning]] [[mysql table]] [[OLAP]]

# mysql data partition

> Splitting one logical table into physical partitions by RANGE, LIST, HASH, or KEY—pruning limits scans to relevant partitions for time-series and archival.

```txt
        mysql data partiti ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Partitioning interviews ask RANGE by time, partition pruning, and DROP PARTIT…

## Sources
- [MySQL Reference Manual — Partitioning](https://dev.mysql.com/doc/refman/en/partitioning.html) — deep-dive
- [MySQL Reference Manual — Partition Pruning](https://dev.mysql.com/doc/refman/en/partitioning-pruning.html) — deep-dive

## Key Concepts
- **Physical split, logical table:** one name, many segments.
- **Methods:** RANGE, LIST, HASH, KEY.
- **Pruning:** `WHERE` on partition key skips irrelevant partitions (`EXPLAIN PARTITIONS`).
- **Lifecycle:** ADD/DROP PARTITION for retention windows.

## Technical Details
- Range by month:

```sql
CREATE TABLE measurements (
  id BIGINT NOT NULL,
  measured_at DATE NOT NULL,
  value DOUBLE,
  PRIMARY KEY (id, measured_at)
)
PARTITION BY RANGE (TO_DAYS(measured_at)) (
  PARTITION p202401 VALUES LESS THAN (TO_DAYS('2024-02-01')),
  PARTITION p202402 VALUES LESS THAN (TO_DAYS('2024-03-01'))
);
```

- Partition pruning: queries with partition key in `WHERE` skip irrelevant part…

```sql
ALTER TABLE measurements DROP PARTITION p202301;
ALTER TABLE measurements ADD PARTITION (...);
```

- Primary keys must include the partition expression columns in MySQL.

## Mistakes to Avoid
- **Mistake:** Partitioning without putting the partition key in hot `WHERE` cl…
- **Mistake:** Expecting partitions to fix missing indexes alone
- **Mistake:** Forgetting PK must include partition columns

## Pros/Cons or Trade-offs
- **Pro:** Fast purge, smaller scans when pruned, manageable archival.
- **Con:** Poor pruning without partition key in queries; more DDL ops; PK design constraints.

## Comparison
- vs [[mysql partitioning]] / [[partitioning]]: sibling notes on the same featu…


### Use cases
- Time-series metrics and log tables where monthly DROP PARTITION is cheaper th…
