[[partitioning]] [[mysql data partition]] [[Data access patterns]] [[mysql table]] [[MySQL Events]]

# mysql partitioning

> MySQL-specific partitioning rules — `PARTITION BY`, subpartitions, and the hard requirement that unique indexes include the partition expression columns.

## Interview Relevance
The unique-key-includes-partition-columns rule is a frequent gotcha question. Also: when subpartitioning helps versus when an archive table is simpler.

## Sources
- [Partitioning Types](https://dev.mysql.com/doc/refman/en/partitioning-types.html) — deep-dive
- [Partitioning Limitations](https://dev.mysql.com/doc/refman/en/partitioning-limitations.html) — deep-dive

## Key Concepts
- **Unique keys rule:** Every unique index (including PRIMARY KEY) must include all columns used in the partition expression.
- **Subpartitioning:** RANGE/LIST outer with HASH/KEY inner for finer physical split.
- **Pruning dependency:** Queries must constrain the partition key ([[mysql data partition]]).
- **Alternatives:** History table + [[MySQL Events]]; replicas for [[OLAP]] reads.

## Technical Details
```sql
PARTITION BY RANGE (YEAR(created_at))
SUBPARTITION BY HASH (user_id)
SUBPARTITIONS 4 (...);
```

Plan PK/UK design before partitioning — retrofits often force composite primary keys like `(id, created_at)`.

## Real-World Applications
Large `events` table RANGE-partitioned by year with HASH subpartitions on `user_id` to spread hot months — only after confirming prune-friendly query patterns.

## Pros/Cons or Trade-offs
- **Pro:** Expresses retention and pruning in DDL MySQL understands.
- **Con:** Unique-key constraint reshapes schema; FK limitations apply.
- **Trade-off:** Subpartitions add complexity; measure before adopting.

## Comparison
vs [[mysql data partition]]: examples and pruning ops live there; this note stresses MySQL rules and subpartition syntax. vs sharding: still one server.

## Mistakes to Avoid
- Designing a surrogate `id` PRIMARY KEY alone on a RANGE(`created_at`) table.
- Subpartitioning without a pruning story.
- Using partitions as a substitute for proper indexes.
