[[mysql]] [[MySQL Engines]] [[MySQL storage]] [[mysql transaction]] [[memory engine]]

# mysql engine

> MySQL pluggable storage engine layer—**InnoDB** is the default and production choice for transactional [[ACID]] workloads; others serve niche roles.

## InnoDB (default)

- Row-level locking, [[MVCC]], foreign keys
- Clustered primary key, redo/undo logs
- Crash recovery via redo log ([[write-ahead logging]])

## Other engines (know they exist)

| Engine | Use |
|--------|-----|
| [[memory engine]] | Volatile RAM tables |
| MyISAM | Legacy non-transactional (avoid for new work) |
| ARCHIVE | Compressed append-only |

```sql
SHOW ENGINES;
CREATE TABLE t (...) ENGINE=InnoDB;
```

## Sources

- MySQL Reference Manual — [InnoDB Introduction](https://dev.mysql.com/doc/refman/en/innodb-introduction.html)
- MySQL Reference Manual — [Alternative Storage Engines](https://dev.mysql.com/doc/refman/en/alter-table.html)
