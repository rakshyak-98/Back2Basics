[[WAL (Write-Ahead Log)]] [[ACID]] [[write-ahead logging]] [[fsync]]

# ARIES

> One-line: industry-standard WAL recovery algorithm ( steal + no-force ) — analysis → redo → undo after crash; underpins SQL Server, Db2, and many enterprise engines.

## Mental model

**ARIES** (Algorithms for Recovery and Isolation Exploiting Semantics) defines how to recover after crash when the buffer pool uses **steal** (uncommitted pages may flush) and **no-force** (committed pages need not be on disk before commit ack). Safety comes from [[WAL (Write-Ahead Log)]]: log record before page change.

```
Crash recovery phases
1. Analysis   — scan WAL from last checkpoint → active tx set, dirty page table
2. Redo       — replay all logged updates (even aborted) from earliest needed LSN
3. Undo       — roll back uncommitted transactions (backward per tx)
```

**LSN (Log Sequence Number)** monotonically tags log records; each page stores `pageLSN` of last applied change. **CLR (Compensation Log Record)** logs undo actions so redo pass stays idempotent.

ARIES also supports **fuzzy checkpoints** — don't require all dirty pages flushed before checkpoint record.

## Standard config / commands

### Conceptual mapping (not one CLI)

| Concept | Postgres-ish | MySQL InnoDB-ish |
|---------|--------------|------------------|
| WAL | `pg_wal` | redo log |
| Checkpoint | `CHECKPOINT` | InnoDB checkpoint |
| Page LSN | page header | page LSN in FIL page |
| Undo | rollback segments / MVCC | undo tablespace |

### Inspect recovery-related state (Postgres)

```sql
SELECT pg_control_checkpoint();
SELECT pg_is_in_recovery();
-- after crash, logs show "database system was not properly shut down; automatic recovery in progress"
```

### MySQL InnoDB recovery

```bash
# my.cnf — never delete ib_logfile* manually while server running
innodb_force_recovery = 0   # 1-6 emergency read-only modes — last resort
```

### Verify WAL durability settings

See [[WAL (Write-Ahead Log)]] for `fsync`, `synchronous_commit`, `innodb_flush_log_at_trx_commit`.

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Long startup after crash | Expected redo volume | Regular checkpoints; adequate WAL size |
| Corrupt page after recovery | Media failure / partial write | Restore backup + replay WAL; `pg_checksums` |
| Stuck in recovery | Missing WAL segment | Restore from archive; PITR |
| InnoDB won't start | `innodb_force_recovery` needed | Level 1→6 read-only salvage; dump and rebuild |
| Replica divergence | Recovery applied different order | Reclone replica |
| "PANIC: could not write to WAL" | Disk full | Free space before restart completes |

## Gotchas

> [!WARNING]
> **`innodb_force_recovery > 0`** — can permanently corrupt if misused; dump data and rebuild clean.

> [!WARNING]
> **Deleting WAL/redo files manually** — breaks ARIES replay chain; total data loss risk.

> [!WARNING]
> **Steal/no-force requires WAL** — disabling fsync "for speed" breaks the algorithm's guarantees.

## When NOT to use

- **Not an app-level pattern** — you don't implement ARIES; you tune the engine that already does.
- **Embedded SQLite** — simpler recovery; still WAL-based but not full ARIES paper.

## Related

[[WAL (Write-Ahead Log)]] [[write-ahead logging]] [[ACID]] [[fsync]] [[Architectures/database/MVCC]]
