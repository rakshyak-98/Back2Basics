[[ACID]] [[WAL (Write-Ahead Log)]] [[OLTP]] [[OLAP]] [[Database design]] [[connection pooling]] [[SQL]] [[mysql]] [[SQL/postgres]]

# Database

> Shared durable storage with a query language and transaction rules — the engine's job is to turn concurrent clients and bytes on disk into atomic commits that survive crashes.

## What a database is responsible for

Applications need **persistent structured state** that many clients can read and write safely. A relational database engine provides:

- **Storage layout** — tables, indexes, logs on disk or memory-mapped files ([[MMAP]])
- **Query execution** — parse [[SQL]], plan access paths, return rows
- **Concurrency control** — [[ACID]] isolation so transactions do not corrupt each other ([[MVCC]] in PostgreSQL, InnoDB row locks + MVCC in MySQL)
- **Crash recovery** — [[WAL (Write-Ahead Log)]] replay after power loss

```txt
Clients ──► [[connection pooling]] ──► SQL planner ──► buffer pool
                                           │
                                           ├── indexes / heap pages
                                           ├── redo / WAL ([[write-ahead logging]])
                                           └── commit / rollback ([[ACID]])
```

## Workload shapes

| Pattern | Access style | Typical engine role |
|---------|--------------|---------------------|
| [[OLTP]] | Short reads/writes, many concurrent sessions | PostgreSQL or MySQL primary |
| [[OLAP]] | Large scans, aggregates, reporting | Column store, warehouse, or replica |
| Cache | Ephemeral, loss tolerable | Redis, memcached ([[BASE]] tradeoffs) |

*When would you route analytics to the primary versus a replica?* When stale reads are acceptable and you need to protect [[OLTP]] latency.

## Routing by symptom

| Symptom or need | Start here |
|-----------------|------------|
| Data missing after crash | [[ACID]] · [[WAL (Write-Ahead Log)]] · [[ARIES]] |
| Connection timeouts under load | [[connection pooling]] · [[mysql pool connection]] |
| Slow queries | [[mysql index]] · [[covering index]] · [[Data access patterns]] |
| Schema change in production | [[database migration]] · [[migration]] · [[Alter table]] |
| Wrong balances / duplicate charges | [[ACID]] · [[mysql transaction]] · [[mysql lock]] |
| PostgreSQL type errors | [[postgres parameter type error]] · [[psql essential]] |
| Scaling beyond one node | [[mysql partitioning]] · [[Horizontal vs Vertical Scaling]] |

## Engines and ecosystems

- **MySQL** — [[mysql]] hub; default [[mysql engine]] is InnoDB ([[MySQL storage]])
- **PostgreSQL** — [[SQL/postgres]]; extensible types, [[GIN]] indexes, strong [[ACID]] defaults
- **Document / blob** — [[GridFS]] (MongoDB), not a substitute for relational invariants
- **Vectors** — [[Vector database]] for similarity search alongside an OLTP store

## Design and operations

- **Modeling:** [[Database design]] · [[SQL normalization]] · [[relocatable schema]]
- **Migrations:** [[database migration]] · [[database seeding]] · [[mysql data migrations]]
- **Foot-guns:** [[Database mistakes]] · [[SQL error]] · [[MySQL Error]]

## Sources

- Martin Kleppmann, *Designing Data-Intensive Applications* (O'Reilly, 2017), Ch. 3 (storage), Ch. 7 (transactions)
- PostgreSQL Documentation — [Chapter 13: Concurrency Control](https://www.postgresql.org/docs/current/mvcc.html)
- MySQL Reference Manual — [InnoDB Storage Engine](https://dev.mysql.com/doc/refman/en/innodb-storage-engine.html)
