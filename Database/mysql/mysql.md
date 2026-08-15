[[Database]] [[mysql connection]] [[cli]] [[mysql query]] [[mysql dump]] [[mysql engine]] [[mysql ssl connection]] [[mysql table]] [[mysql index]]

# mysql

> MySQL server — relational database over TCP with [[SQL]], default transactional storage via InnoDB ([[mysql engine]]), and crash recovery through the redo log.

## Interview Relevance
Baseline “what is MySQL?” plus namespace terminology (database ≡ schema) and the request path from client to InnoDB. Use leaf notes for depth.

## Sources
- [MySQL Reference Manual](https://dev.mysql.com/doc/refman/en/) — overview
- [InnoDB Storage Engine](https://dev.mysql.com/doc/refman/en/innodb-storage-engine.html) — deep-dive

## Core Definition
mysqld accepts SQL from clients, plans access paths, and delegates durable storage/concurrency to a storage engine — almost always InnoDB in modern deployments.

## Key Concepts
- **Client → server TCP:** Optional TLS ([[mysql ssl connection]]); sessions via [[mysql connection]] / pools.
- **Database ≡ schema:** `CREATE DATABASE` / `CREATE SCHEMA` are synonyms; `USE db` sets default.
- **InnoDB path:** Buffer pool + redo/undo for [[ACID]] behavior.
- **Ops surfaces:** [[cli]], [[mysql dump]], [[Configuration]] / [[variables]].

## Technical Details
```txt
mysql client / app driver
        │  TCP (+ optional TLS)
        ▼
   mysqld ──► parse ──► optimizer ──► executor
                    │
                    └── InnoDB buffer pool + redo log
```

| Topic | Note |
|-------|------|
| Connections | [[mysql connection]] · [[mysql pool connection]] |
| Queries | [[mysql query]] · [[show query]] |
| Schema | [[mysql table]] · [[mysql columns]] |
| Performance | [[mysql index]] · [[covering index]] |
| Operations | [[mysql dump]] · [[Configuration]] |

## Real-World Applications
Primary OLTP store for web apps, often with async replicas for reads and binlog CDC into warehouses.

## Pros/Cons or Trade-offs
- **Pro:** Ubiquitous ecosystem, strong InnoDB OLTP story, managed offerings everywhere.
- **Con:** Historical engine/quirks landmines; online DDL still needs care at scale.
- **Trade-off:** MySQL vs [[SQL/postgres]] — tooling familiarity, JSON/index features, operational preference.

## Comparison
vs [[SQL/postgres]]: different defaults (isolation, catalog/roles, extensions). vs non-relational stores: MySQL wins when joins, transactions, and mature ops matter.

## Mistakes to Avoid
- Treating MyISAM as a modern default.
- Confusing binlog with InnoDB redo.
- Skipping connection pooling and TLS on production paths.
