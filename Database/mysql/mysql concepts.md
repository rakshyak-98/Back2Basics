[[mysql]] [[mysql engine]] [[mysql transaction]] [[SQL]]

# mysql concepts

> Core MySQL ideas—schema as database, storage engines, replication topology, and binary log—that frame every operational decision.

## Schema = database

`CREATE DATABASE app` creates a namespace for tables. Unlike PostgreSQL, there is no separate "schema" layer inside a database (except naming synonym).

## Logical replication ingredients

- **Binary log (binlog)** — logical change stream for replicas and CDC
- **Redo log** — InnoDB physical crash recovery ([[MySQL storage]])

## Replication roles

```txt
Primary (read/write) ──► Replica(s) (async read)
```

Replicas can lag—do not assume read-your-writes on replica without routing logic.

## Sources

- MySQL Reference Manual — [MySQL Replication](https://dev.mysql.com/doc/refman/en/replication.html)
- MySQL Reference Manual — [Binary Log](https://dev.mysql.com/doc/refman/en/binary-log.html)
