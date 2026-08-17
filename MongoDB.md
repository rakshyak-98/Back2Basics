[[mongosh]] [[mongoose/mongoose]] [[mongodb connection]] [[mognodb indexing]] [[mongodb replicaset]] [[mongodb sharding]] [[INDEX]] [[WiredTiger storage engine]]

# MongoDB

> MongoDB — a document database: JSON-like BSON docs, replica sets for failover, sharding for scale; production pain is often indexes, pools, or schema drift.

```txt
        MongoDB ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Expect document model vs relational, replica set elections, read preference, …

## Sources
- [MongoDB Manual — Introduction](https://www.mongodb.com/docs/manual/introduction/) — overview
- [MongoDB Manual — Replication](https://www.mongodb.com/docs/manual/replication/) — deep-dive
- [Wikipedia — MongoDB](https://en.wikipedia.org/wiki/MongoDB) — overview

## Key Concepts
- **Document model:** Nested docs and arrays; design for access patterns, not 3NF purity.
- **Indexes:** Without them, collection scans ([[mognodb indexing]]).
- **Replica set:** Primary + secondaries; automatic failover ([[mongodb replicaset]]).
- **Sharding:** Horizontal scale via shard key ([[mongodb sharding]]).
- **Drivers / ODM:** Connection pools ([[mongodb connection]]); [[mongoose/mongoose]] in Node.


- **Core:** MongoDB stores BSON documents in collections. Schemas can vary by document

## Technical Details
```txt
App ──► driver pool ──► mongod (primary)
                           │
                           ├── secondaries ([[mongodb replicaset]])
                           └── mongos + shards ([[mongodb sharding]])
```

| Symptom / need | Go to |
|----------------|-------|
| Slow queries | [[mognodb indexing]] · [[mongosh]] |
| Failover | [[mongodb replicaset]] |
| Connection storms | [[mongodb connection]] |
| Migrations | [[mongodb migration]] |
| Aggregation / `$lookup` | [[mongodb lookup query]] |

| Breakage | Check | Fix |
|----------|-------|-----|
| Server selection error | RS health; URI | Fix primary; `replicaSet` name |
| Timeouts / collscans | Explain plan | Compound index |
| Stale reads | Read preference | `primary` for read-your-writes |
| OOM | WiredTiger cache | RAM / cache sizing / shard |

## Mistakes to Avoid
- **Mistake:** Unbounded arrays / documents that grow forever
- **Mistake:** Secondary reads for read-your-writes correctness
- **Mistake:** Unique business keys without unique indexes
- **Mistake:** Connection-per-request without pooling

## Pros/Cons or Trade-offs
- **Pro:** Flexible documents; horizontal scale path; rich aggregation.
- **Con:** Easy to skip schema discipline; wrong shard key is painful; multi-doc transactions cost more than people expect.

## Comparison
- vs Postgres ([[postgres essential]]): stronger relational constraints and joi…


### Use cases
- Product catalog with varied attributes per SKU
