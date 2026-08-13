[[partitioning]] [[mysql data partition]] [[Data access patterns]]

# mysql partitioning

> MySQL-specific partitioning syntax and limitations—`PARTITION BY`, subpartitions, and interaction with unique indexes requiring partition key inclusion.

## Unique keys rule

Every unique index (including PRIMARY KEY) must include all columns in the partition expression.

## Subpartitioning

```sql
PARTITION BY RANGE (YEAR(created_at))
SUBPARTITION BY HASH (user_id)
SUBPARTITIONS 4 (...);
```

## Alternatives

- Archive old rows to history table via [[MySQL Events]]
- Read replicas for reporting ([[OLAP]])

## Sources

- MySQL Reference Manual — [Partitioning Types](https://dev.mysql.com/doc/refman/en/partitioning-types.html)
