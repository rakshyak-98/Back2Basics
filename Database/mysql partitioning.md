[[partitioning]] [[mysql data partition]] [[mysql/mysql partitioning]] [[mysql table]] [[OLAP]] [[Data access patterns]]

# mysql partitioning

> Split one MySQL table into segments (RANGE, LIST, HASH, KEY) so retention and pruning stay cheap — still one server, not a shard grid.

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
- **Key signal:** “Partition or shard?” and “when does pruning fail?” are common prompts

## Sources
- [MySQL Reference Manual — Partitioning Overview](https://dev.mysql.com/doc/refman/en/partitioning-overview.html) — overview
- [MySQL Reference Manual — Partition Management](https://dev.mysql.com/doc/refman/en/partitioning-management.html) — deep-dive
- [[mysql/mysql partitioning]] — deep-dive
- [[mysql data partition]] — deep-dive
- [[partitioning]] — overview

## Key Concepts
- **Core:** MySQL table partitioning stores one logical table as multiple physical segmen…

## Technical Details
- Why partition:

- Fast retention (`DROP PARTITION` vs `DELETE` millions of rows).
- Partition pruning when queries filter on the partition key.
- Manageable maintenance windows per time slice (rebuild, compress, archive).

- Start here in this vault:

| Depth | Note |
|-------|------|
| Decision frame | [[partitioning]] |
| DDL examples | [[mysql data partition]] |
| MySQL rules / unique keys | [[mysql/mysql partitioning]] |

- Design checklist:

1. Can every hot query include the partition key?
2. Can unique keys include those columns?
3. Is drop-partition retention the actual goal?

```sql
-- Conceptual RANGE by year (syntax details in sibling notes)
ALTER TABLE events
PARTITION BY RANGE (YEAR(created_at)) (
  PARTITION p2024 VALUES LESS THAN (2025),
  PARTITION p2025 VALUES LESS THAN (2026),
  PARTITION pmax VALUES LESS THAN MAXVALUE
);
```

- *What breaks first without the key in WHERE?* Full partition scan

## Mistakes to Avoid
- **Mistake:** Partitioning “to make it faster” without prune-friendly queries
- **Mistake:** Confusing partitions with shards
- **Mistake:** Creating thousands of tiny partitions (metadata and open-file pr…
- **Mistake:** Ignoring unique-key inclusion rules until `CREATE TABLE` fails i…

## Pros/Cons or Trade-offs
- **Pro:** Operationally strong retention and prune-friendly time-series.
- **Con:** Schema constraints (unique keys, limited foreign keys), metadata overhead, bad plans without the key.
- **Trade-off:** Partitions vs archive/history table + batch copy/delete without partition DDL.

## Comparison
- vs [[partitioning]]: that note is the decision frame


### Use cases
- Monthly partitions on telemetry or audit tables: keep 13 months online, `DROP…
