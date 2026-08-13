[[mysql partitioning]] [[partitioning]] [[mysql table]] [[OLAP]]

# mysql data partition

> Splitting one logical table into physical partitions by RANGE, LIST, HASH, or KEY—pruning limits scans to relevant partitions for time-series and archival.

## Range by month

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

## Partition pruning

Queries with partition key in `WHERE` skip irrelevant partitions—verify with `EXPLAIN PARTITIONS`.

## Management

```sql
ALTER TABLE measurements DROP PARTITION p202301;
ALTER TABLE measurements ADD PARTITION (...);
```

## Sources

- MySQL Reference Manual — [Partitioning](https://dev.mysql.com/doc/refman/en/partitioning.html)
- MySQL Reference Manual — [Partition Pruning](https://dev.mysql.com/doc/refman/en/partitioning-pruning.html)
