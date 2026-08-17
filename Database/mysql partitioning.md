[[partitioning]] [[mysql data partition]] [[mysql/mysql partitioning]] [[mysql table]] [[OLAP]] [[Data access patterns]]

# mysql partitioning

> Split one MySQL table into segments (RANGE, LIST, HASH, KEY) so retention and pruning stay cheap — still one server, not a shard grid.





## Interview Relevance
“Partition or shard?” and “when does pruning fail?” are common prompts. Signal: every hot query must include the partition key, unique keys must include it, and drop-partition retention is often the real win — not magic speedups.

## Sources
- [MySQL Reference Manual — Partitioning Overview](https://dev.mysql.com/doc/refman/en/partitioning-overview.html) — overview
- [MySQL Reference Manual — Partition Management](https://dev.mysql.com/doc/refman/en/partitioning-management.html) — deep-dive
- [[mysql/mysql partitioning]] — deep-dive
- [[mysql data partition]] — deep-dive
- [[partitioning]] — overview

## Core Definition
MySQL table partitioning stores one logical table as multiple physical segments chosen by a partition expression. Queries that filter on that expression can prune; `DROP PARTITION` removes a whole slice without row-by-row delete.

## Recall Cues
- Why do interviewers care about “Partition or shard?” and “when does pruning fail?” are common prompts?
- Why do interviewers care about Signal: every hot query must include the partition key, unique keys must include it, and drop-partition retention is often the real win — not magic speedups?
- What is step 1: Can every hot query include the partition key??
- What is step 2: Can unique keys include those columns??
- What is step 3: Is drop-partition retention the actual goal??
- What mistake is **Partitioning “to make it faster” without prune-friendly queries**?
- What mistake is **Confusing partitions with shards**?
- What mistake is **Creating thousands of tiny partitions (metadata and open-file pressure)**?

## Technical Details
Why partition:

- Fast retention (`DROP PARTITION` vs `DELETE` millions of rows).
- Partition pruning when queries filter on the partition key.
- Manageable maintenance windows per time slice (rebuild, compress, archive).

Start here in this vault:

| Depth | Note |
|-------|------|
| Decision frame | [[partitioning]] |
| DDL examples | [[mysql data partition]] |
| MySQL rules / unique keys | [[mysql/mysql partitioning]] |

Design checklist:

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

*What breaks first without the key in WHERE?* Full partition scan — often slower than a well-indexed non-partitioned table.

## Mistakes to Avoid
- Partitioning “to make it faster” without prune-friendly queries.
- Confusing partitions with shards.
- Creating thousands of tiny partitions (metadata and open-file pressure).
- Ignoring unique-key inclusion rules until `CREATE TABLE` fails in production migration.

## Comparison
vs [[partitioning]]: that note is the decision frame; this note is the MySQL-focused routing and checklist. vs [[mysql/mysql partitioning]]: deep syntax and engine rules. vs horizontal sharding: shards split across nodes; partitions do not add nodes.

## Real-World Applications
Monthly partitions on telemetry or audit tables: keep 13 months online, `DROP PARTITION` for the oldest month nightly. Skip partitioning on heavily FK-related [[OLTP]] order graphs where unique-key rules fight the model.

## Pros/Cons or Trade-offs
- **Pro:** Operationally strong retention and prune-friendly time-series.
- **Con:** Schema constraints (unique keys, limited foreign keys), metadata overhead, bad plans without the key.
- **Trade-off:** Partitions vs archive/history table + batch copy/delete without partition DDL.
