[[Database]] [[mysql connection]] [[cli]] [[mysql query]] [[mysql dump]] [[mysql engine]] [[mysql ssl connection]] [[mysql table]] [[mysql index]]

# mysql

> MySQL server — relational database over TCP with [[SQL]], default transactional storage via InnoDB ([[mysql engine]]), and crash recovery through the redo log.

```txt
        mysql ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Baseline “what is MySQL?” plus namespace terminology (database ≡ schema) and …

## Sources
- [MySQL Reference Manual](https://dev.mysql.com/doc/refman/en/) — overview
- [InnoDB Storage Engine](https://dev.mysql.com/doc/refman/en/innodb-storage-engine.html) — deep-dive

## Key Concepts
- **Client → server TCP:** Optional TLS ([[mysql ssl connection]])
- **Database ≡ schema:** `CREATE DATABASE` / `CREATE SCHEMA` are synonyms; `USE db` sets default.
- **InnoDB path:** Buffer pool + redo/undo for [[ACID]] behavior.
- **Ops surfaces:** [[cli]], [[mysql dump]], [[Configuration]] / [[variables]].


- **Core:** mysqld accepts SQL from clients, plans access paths, and delegates durable st…

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

## Mistakes to Avoid
- **Mistake:** Treating MyISAM as a modern default
- **Mistake:** Confusing binlog with InnoDB redo
- **Mistake:** Skipping connection pooling and TLS on production paths

## Pros/Cons or Trade-offs
- **Pro:** Ubiquitous ecosystem, strong InnoDB OLTP story, managed offerings everywhere.
- **Con:** Historical engine/quirks landmines; online DDL still needs care at scale.
- **Trade-off:** MySQL vs [[SQL/postgres]] — tooling familiarity, JSON/index features, operational preference.

## Comparison
- vs [[SQL/postgres]]: different defaults (isolation, catalog/roles, extensions)


### Use cases
- Primary OLTP store for web apps, often with async replicas for reads and binl…
