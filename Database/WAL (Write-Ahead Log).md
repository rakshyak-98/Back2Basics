[[Database]] [[ACID]] [[write-ahead logging]] [[ARIES]] [[mysql engine]] [[SQL/postgres]]

# WAL (Write-Ahead Log)

> Append-only log of page changes written to stable storage before the data pages they describe—so a crash can replay committed work and discard incomplete transactions.

## Core rule

**Write the log record first, then apply the change to data pages** (often in memory). On restart, the engine scans the log from the last checkpoint and reapplies any committed changes not yet on disk.

```txt
Transaction commit
    │
    ├─► append redo records to WAL (fsync per durability policy)
    └─► dirty pages flushed later by background writer

Crash ──► recovery replays WAL from checkpoint LSN
```

## Why not update pages in place only?

Random in-place disk writes are slow and not atomic at page granularity. Logging sequential appends batches durability work and enables [[ARIES]]-style redo/undo recovery.

## Engine implementations

| System | WAL name | Key identifier |
|--------|----------|------------------|
| PostgreSQL | WAL / pg_xlog | Log Sequence Number (LSN) |
| MySQL InnoDB | Redo log | LSN in `#innodb_redo` |
| SQLite | Rollback journal or WAL mode | Frame numbers |

## Durability versus performance

PostgreSQL `synchronous_commit=off` and MySQL `innodb_flush_log_at_trx_commit=2` batch fsyncs—faster, but committed transactions may be lost on OS crash. Money paths keep full sync enabled.

## Sources

- PostgreSQL Documentation — [WAL Internals](https://www.postgresql.org/docs/current/wal-intro.html)
- MySQL Reference Manual — [17.6.5 Redo Log](https://dev.mysql.com/doc/refman/en/innodb-redo-log.html)
- Mohan, C. et al., "ARIES: A Transaction Recovery Method" (ACM TODS, 1992)
- Kleppmann, *DDIA*, Ch. 3
