[[Database]] [[mysql connection]] [[cli]] [[mysql query]] [[mysql dump]] [[mysql engine]]

# mysql

> MySQL server—relational database accessed over TCP with [[SQL]], default transactional storage via InnoDB ([[mysql engine]]) and crash recovery through the redo log.

## Request path

```txt
mysql client / app driver
        │  TCP (+ optional TLS: [[mysql ssl connection]])
        ▼
   mysqld ──► parse ──► optimizer ──► executor
                    │
                    └── InnoDB buffer pool + redo log
```

## Namespace terminology

In MySQL, **database** and **schema** are synonyms (`CREATE DATABASE` = `CREATE SCHEMA`). Tables live inside a schema; `USE dbname` sets the default.

## Where to go next

| Topic | Note |
|-------|------|
| Connections | [[mysql connection]] · [[mysql pool connection]] |
| Queries | [[mysql query]] · [[show query]] |
| Schema | [[mysql table]] · [[mysql columns]] |
| Performance | [[mysql index]] · [[covering index]] |
| Operations | [[mysql dump]] · [[Configuration]] |

## Sources

- MySQL Reference Manual — [https://dev.mysql.com/doc/refman/en/](https://dev.mysql.com/doc/refman/en/)
- Oracle MySQL — [InnoDB Storage Engine](https://dev.mysql.com/doc/refman/en/innodb-storage-engine.html)
