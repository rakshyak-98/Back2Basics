[[partitioning]] [[mysql data partition]] [[Data access patterns]] [[mysql table]] [[MySQL Events]]

# mysql partitioning

> MySQL-specific partitioning rules — `PARTITION BY`, subpartitions, and the hard requirement that unique indexes include the partition expression columns.

```txt
        mysql partitioning ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** The unique-key-includes-partition-columns rule is a frequent gotcha question

## Sources
- [Partitioning Types](https://dev.mysql.com/doc/refman/en/partitioning-types.html) — deep-dive
- [Partitioning Limitations](https://dev.mysql.com/doc/refman/en/partitioning-limitations.html) — deep-dive

## Key Concepts
- **Unique keys rule:** Every unique index (including PRIMARY KEY) must include all columns used in t…
- **Subpartitioning:** RANGE/LIST outer with HASH/KEY inner for finer physical split.
- **Pruning dependency:** Queries must constrain the partition key ([[mysql data partition]]).
- **Alternatives:** History table + [[MySQL Events]]; replicas for [[OLAP]] reads.

## Technical Details
```sql
PARTITION BY RANGE (YEAR(created_at))
SUBPARTITION BY HASH (user_id)
SUBPARTITIONS 4 (...);
```

- Plan PK/UK design before partitioning

## Mistakes to Avoid
- **Mistake:** Designing a surrogate `id` PRIMARY KEY alone on a RANGE(`created…
- **Mistake:** Subpartitioning without a pruning story
- **Mistake:** Using partitions as a substitute for proper indexes

## Pros/Cons or Trade-offs
- **Pro:** Expresses retention and pruning in DDL MySQL understands.
- **Con:** Unique-key constraint reshapes schema; FK limitations apply.
- **Trade-off:** Subpartitions add complexity; measure before adopting.

## Comparison
- vs [[mysql data partition]]: examples and pruning ops live there


### Use cases
- Large `events` table RANGE-partitioned by year with HASH subpartitions on `us…
