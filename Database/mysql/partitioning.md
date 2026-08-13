[[mysql partitioning]] [[mysql data partition]] [[mysql table]]

# partitioning

> Table partitioning concepts in MySQL—same as [[mysql data partition]]; focuses on when partitioning helps versus when a separate archive table is simpler.

## When it helps

- Time-series retention (drop old partitions fast)
- Very large tables where queries always filter on partition key

## When it hurts

- No partition key in query — scans all partitions
- Too many partitions — metadata overhead
- Foreign keys referencing partitioned tables (restrictions apply)

*When would you partition versus shard?* Partitioning stays on one server; sharding splits across nodes.

## Sources

- MySQL Reference Manual — [Partitioning Overview](https://dev.mysql.com/doc/refman/en/partitioning-overview.html)
