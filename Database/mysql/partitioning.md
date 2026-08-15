[[mysql partitioning]] [[mysql data partition]] [[mysql table]] [[mysql/mysql partitioning]]

# partitioning

> When MySQL table partitioning helps — and when a separate archive table is simpler — on one server (not the same as sharding).

## Interview Relevance
“Partition or shard?” and “when does partitioning hurt?” are common design prompts. Signal: pruning requirements and operational cost.

## Sources
- [Partitioning Overview](https://dev.mysql.com/doc/refman/en/partitioning-overview.html) — overview
- [[mysql data partition]] · [[mysql/mysql partitioning]] — deep-dive

## Key Concepts
- **Helps:** Time-series retention (`DROP PARTITION`), queries that always filter the partition key, maintenance per slice.
- **Hurts:** Queries without the key (scan all), too many partitions, FK restrictions on partitioned tables.
- **Partition vs shard:** Partitioning stays on one server; sharding splits across nodes.
- **Alternative:** Archive/history table without partition DDL constraints.

## Technical Details
Design checklist:
1. Can every hot query include the partition key?
2. Can unique keys include those columns?
3. Is drop-partition retention the actual goal?

If any answer is no, prefer indexes + archival jobs first.

## Real-World Applications
Monthly partitions on telemetry tables; skip partitioning on heavily FK-related OLTP graphs.

## Pros/Cons or Trade-offs
- **Pro:** Operationally strong retention story.
- **Con:** Schema and query constraints; metadata overhead.
- **Trade-off:** Partitions vs plain archival table + batch delete/copy.

## Comparison
vs [[mysql data partition]]: DDL examples; vs [[mysql/mysql partitioning]]: MySQL unique-key rules. This note is the decision frame.

## Mistakes to Avoid
- Partitioning to “make it faster” without prune-friendly queries.
- Confusing partitions with horizontal shards.
- Creating thousands of partitions for tiny date buckets.
