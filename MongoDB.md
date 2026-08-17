[[mongosh]] [[mongoose/mongoose]] [[mongodb connection]] [[mognodb indexing]] [[mongodb replicaset]] [[mongodb sharding]] [[INDEX]] [[WiredTiger storage engine]]

# MongoDB

> MongoDB — a document database: JSON-like BSON docs, replica sets for failover, sharding for scale; production pain is often indexes, pools, or schema drift.





## Interview Relevance
Expect document model vs relational, replica set elections, read preference, and index design (ESR rule, compound keys). Signal: you know when flexibility becomes unqueryable chaos.

## Sources
- [MongoDB Manual — Introduction](https://www.mongodb.com/docs/manual/introduction/) — overview
- [MongoDB Manual — Replication](https://www.mongodb.com/docs/manual/replication/) — deep-dive
- [Wikipedia — MongoDB](https://en.wikipedia.org/wiki/MongoDB) — overview

## Core Definition
MongoDB stores BSON documents in collections. Schemas can vary by document; indexes make query paths fast; replica sets provide HA; sharding partitions data across nodes.

## Key Concepts
- **Document model:** Nested docs and arrays; design for access patterns, not 3NF purity.
- **Indexes:** Without them, collection scans ([[mognodb indexing]]).
- **Replica set:** Primary + secondaries; automatic failover ([[mongodb replicaset]]).
- **Sharding:** Horizontal scale via shard key ([[mongodb sharding]]).
- **Drivers / ODM:** Connection pools ([[mongodb connection]]); [[mongoose/mongoose]] in Node.

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

## Real-World Applications
Product catalog with varied attributes per SKU; session or event data with high write rates; multi-region apps using replica sets and careful read concern/write concern.

## Pros/Cons or Trade-offs
- **Pro:** Flexible documents; horizontal scale path; rich aggregation.
- **Con:** Easy to skip schema discipline; wrong shard key is painful; multi-doc transactions cost more than people expect.

## Comparison
vs Postgres ([[postgres essential]]): stronger relational constraints and joins by default; Mongo favors document locality. vs [[Redis]]: Redis is in-memory structures/cache; Mongo is durable document storage. Engine note: [[WiredTiger storage engine]].

## Mistakes to Avoid
- Unbounded arrays / documents that grow forever.
- Secondary reads for read-your-writes correctness.
- Unique business keys without unique indexes.
- Connection-per-request without pooling.
