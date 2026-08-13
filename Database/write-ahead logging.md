[[WAL (Write-Ahead Log)]] [[ACID]] [[ARIES]] [[mysql engine]] [[SQL/postgres]]

# write-ahead logging

> The protocol that appends change records to a log and fsyncs them before acknowledging commit—foundation of crash-safe [[ACID]] durability in PostgreSQL, InnoDB, and most relational engines.

## Mechanism

1. Transaction modifies pages in the **buffer pool** (memory).
2. Engine appends **redo records** describing the change to the [[WAL (Write-Ahead Log)]].
3. On `COMMIT`, log records reach durable media (policy-dependent).
4. Dirty data pages are written asynchronously; order does not matter because redo can reconstruct them.

## Checkpointing

Periodically the engine writes dirty pages and records a **checkpoint LSN**. Log segments before the checkpoint can be recycled. Long checkpoints or tiny logs increase write amplification.

## Read path interaction

Readers use buffer pool pages; they do not wait for WAL replay unless recovery is in progress. [[MVCC]] provides consistent snapshots independent of page flush timing.

## Operational checks

```sql
-- PostgreSQL: current WAL insert position
SELECT pg_current_wal_lsn();

-- MySQL: InnoDB status includes log sequence number
SHOW ENGINE INNODB STATUS\G
```

## Sources

- PostgreSQL Documentation — [Reliability and the Write-Ahead Log](https://www.postgresql.org/docs/current/wal.html)
- MySQL Reference Manual — [InnoDB Recovery](https://dev.mysql.com/doc/refman/en/innodb-recovery.html)
- Wikipedia — [Write-ahead logging](https://en.wikipedia.org/wiki/Write-ahead_logging)
