[[ACID]] [[WAL (Write-Ahead Log)]] [[OLTP]] [[OLAP]] [[Database design]] [[connection pooling]] [[SQL]] [[mysql]] [[SQL/postgres]] [[BASE]] [[ARIES]] [[MMAP]] [[MVCC]] [[write-ahead logging]] [[GIN]] [[GridFS]] [[Vector database]] [[Database mistakes]]

# Database

> Shared durable storage with a query language and transaction rules — the engine's job is to turn concurrent clients and bytes on disk into atomic commits that survive crashes.

```txt
        Database ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** This is the domain hub: interviewers expect you to map symptoms (crash loss, …

## Sources
- Martin Kleppmann, *Designing Data-Intensive Applications* (O'Reilly, 2017), Ch. 3, 7 — deep-dive
- [PostgreSQL Documentation — Concurrency Control](https://www.postgresql.org/docs/current/mvcc.html) — deep-dive
- [MySQL Reference Manual — InnoDB Storage Engine](https://dev.mysql.com/doc/refman/en/innodb-storage-engine.html) — overview

## Key Concepts
- **Storage layout:** tables, indexes, logs on disk or memory-mapped files ([[MMAP]]).
- **Query execution:** parse [[SQL]], plan access paths, return rows.
- **Concurrency control:** [[ACID]] isolation ([[MVCC]] in PostgreSQL; InnoDB row locks + MVCC in MySQL).
- **Crash recovery:** [[WAL (Write-Ahead Log)]] replay after power loss ([[ARIES]] mental model).


- **Core:** A relational database engine provides persistent structured state that many c…

## Technical Details
```txt
Clients ──► [[connection pooling]] ──► SQL planner ──► buffer pool
                                           │
                                           ├── indexes / heap pages
                                           ├── redo / WAL ([[write-ahead logging]])
                                           └── commit / rollback ([[ACID]])
```

| Pattern | Access style | Typical engine role |
|---------|--------------|---------------------|
| [[OLTP]] | Short reads/writes, many concurrent sessions | PostgreSQL or MySQL primary |
| [[OLAP]] | Large scans, aggregates, reporting | Column store, warehouse, or replica |
| Cache | Ephemeral, loss tolerable | Redis, memcached ([[BASE]] tradeoffs) |

- *When would you route analytics to the primary versus a replica?* When stale …

- Symptom routing:

| Symptom or need | Start here |
|-----------------|------------|
| Data missing after crash | [[ACID]] · [[WAL (Write-Ahead Log)]] · [[ARIES]] |
| Connection timeouts under load | [[connection pooling]] · [[mysql pool connection]] |
| Slow queries | [[mysql index]] · [[covering index]] · [[Data access patterns]] |
| Schema change in production | [[database migration]] · [[migration]] · [[Alter table]] |
| Wrong balances / duplicate charges | [[ACID]] · [[mysql transaction]] · [[mysql lock]] |
| PostgreSQL type errors | [[postgres parameter type error]] · [[psql essential]] |
| Scaling beyond one node | [[mysql partitioning]] · [[Horizontal vs Vertical Scaling]] |

- Engines and ecosystems:

- **MySQL:** — [[mysql]] hub; default [[mysql engine]] is InnoDB ([[MySQL storage]])
- **PostgreSQL:** — [[SQL/postgres]]
- **Document / blob:** — [[GridFS]] (MongoDB), not a substitute for relational invariants
- **Vectors:** — [[Vector database]] for similarity search alongside an OLTP store

- Design and operations:

- **Modeling:** [[Database design]] · [[SQL normalization]] · [[relocatable schema]]
- **Migrations:** [[database migration]] · [[database seeding]] · [[mysql data migrations]]
- **Foot-guns:** [[Database mistakes]] · [[SQL error]] · [[MySQL Error]]

## Mistakes to Avoid
- **Mistake:** Treating the database as a dumb key-value file without transacti…
- **Mistake:** Running heavy analytics on the [[OLTP]] primary until checkout t…
- **Mistake:** Skipping leaf notes—hand-waving “just use a database” without is…

## Pros/Cons or Trade-offs
- **Pro:** Strong invariants, rich query languages, mature operational tooling.
- **Con:** Scaling writes beyond one primary is hard; wrong workload on the primary (heavy analytics) destroys latency.

## Comparison
- vs [[BASE]] caches: databases prioritize durable correct commits


### Use cases
- Primary store for SaaS [[OLTP]], reporting replicas for [[OLAP]], and special…
