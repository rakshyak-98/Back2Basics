[[mysql]] [[MySQL Engines]] [[MySQL storage]] [[mysql transaction]] [[memory engine]] [[write-ahead logging]] [[MVCC]]

# mysql engine

> MySQL pluggable storage engine layer—**InnoDB** is the default and production choice for transactional [[ACID]] workloads; others serve niche roles.

```txt
        mysql engine ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Engine choice questions expect InnoDB as default, awareness of MEMORY/MyISAM …

## Sources
- [MySQL Reference Manual — InnoDB Introduction](https://dev.mysql.com/doc/refman/en/innodb-introduction.html) — deep-dive
- [MySQL Reference Manual — Alternative Storage Engines](https://dev.mysql.com/doc/refman/en/storage-engines.html) — overview

## Key Concepts
- **Pluggable engines:** per-table `ENGINE=` selects implementation.
- **InnoDB default:** row-level locking, [[MVCC]], foreign keys, clustered PK, redo/undo.
- **Niche engines:** [[memory engine]], MyISAM (legacy), ARCHIVE

## Technical Details
- InnoDB (default):

- Row-level locking, [[MVCC]], foreign keys
- Clustered primary key, redo/undo logs
- Crash recovery via redo log ([[write-ahead logging]])

| Engine | Use |
|--------|-----|
| [[memory engine]] | Volatile RAM tables |
| MyISAM | Legacy non-transactional (avoid for new work) |
| ARCHIVE | Compressed append-only |

```sql
SHOW ENGINES;
CREATE TABLE t (...) ENGINE=InnoDB;
```

## Mistakes to Avoid
- **Mistake:** Creating new MyISAM tables “for speed”
- **Mistake:** Assuming all engines support foreign keys
- **Mistake:** Forgetting to specify/verify ENGINE after restores from mixed du…

## Pros/Cons or Trade-offs
- **Pro:** InnoDB delivers transactional semantics and crash recovery expected by modern apps.
- **Con:** Non-InnoDB engines surprise with missing transactions/FKs; mixing engines in one logical design complicates backups and consistency.

## Comparison
- vs [[MySQL Engines]]: that note is the comparison table hub


### Use cases
- Creating all new application tables as InnoDB and migrating leftover MyISAM
