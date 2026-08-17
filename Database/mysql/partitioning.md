[[mysql partitioning]] [[mysql data partition]] [[mysql table]] [[mysql/mysql partitioning]]

# partitioning

> When MySQL table partitioning helps — and when a separate archive table is simpler — on one server (not the same as sharding).

```txt
        partitioning ──┬── Interview
               ├── Sources
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** “Partition or shard?” and “when does partitioning hurt?” are common design pr…

## Sources
- [Partitioning Overview](https://dev.mysql.com/doc/refman/en/partitioning-overview.html) — overview
- [[mysql data partition]] · [[mysql/mysql partitioning]] — deep-dive

## Technical Details
- Design checklist:

1. Can every hot query include the partition key?
2. Can unique keys include those columns?
3. Is drop-partition retention the actual goal?

- If any answer is no, prefer indexes + archival jobs first.

## Mistakes to Avoid
- **Mistake:** Partitioning to “make it faster” without prune-friendly queries
- **Mistake:** Confusing partitions with horizontal shards
- **Mistake:** Creating thousands of partitions for tiny date buckets

## Pros/Cons or Trade-offs
- **Pro:** Operationally strong retention story.
- **Con:** Schema and query constraints; metadata overhead.
- **Trade-off:** Partitions vs plain archival table + batch delete/copy.

## Comparison
- vs [[mysql data partition]]: DDL examples


### Use cases
- Monthly partitions on telemetry tables
