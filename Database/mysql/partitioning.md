[[mysql partitioning]] [[mysql data partition]] [[mysql table]] [[mysql/mysql partitioning]]

# partitioning

> When MySQL table partitioning helps — and when a separate archive table is simpler — on one server (not the same as sharding).





## Interview Relevance
“Partition or shard?” and “when does partitioning hurt?” are common design prompts. Signal: pruning requirements and operational cost.

## Sources
- [Partitioning Overview](https://dev.mysql.com/doc/refman/en/partitioning-overview.html) — overview
- [[mysql data partition]] · [[mysql/mysql partitioning]] — deep-dive

## Recall Cues
- Why do interviewers care about “Partition or shard?” and “when does partitioning hurt?” are common design prompts?
- Why do interviewers care about Signal: pruning requirements and operational cost?
- What is step 1: Can every hot query include the partition key??
- What is step 2: Can unique keys include those columns??
- What is step 3: Is drop-partition retention the actual goal??
- What mistake is **Partitioning to “make it faster” without prune-friendly queries**?
- What mistake is **Confusing partitions with horizontal shards**?
- What mistake is **Creating thousands of partitions for tiny date buckets**?

## Technical Details
Design checklist:
1. Can every hot query include the partition key?
2. Can unique keys include those columns?
3. Is drop-partition retention the actual goal?

If any answer is no, prefer indexes + archival jobs first.

## Mistakes to Avoid
- Partitioning to “make it faster” without prune-friendly queries.
- Confusing partitions with horizontal shards.
- Creating thousands of partitions for tiny date buckets.

## Comparison
vs [[mysql data partition]]: DDL examples; vs [[mysql/mysql partitioning]]: MySQL unique-key rules. This note is the decision frame.

## Real-World Applications
Monthly partitions on telemetry tables; skip partitioning on heavily FK-related OLTP graphs.

## Pros/Cons or Trade-offs
- **Pro:** Operationally strong retention story.
- **Con:** Schema and query constraints; metadata overhead.
- **Trade-off:** Partitions vs plain archival table + batch delete/copy.
