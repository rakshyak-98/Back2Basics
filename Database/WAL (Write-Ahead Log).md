[[ACID]] [[ARIES]] [[write-ahead logging]] [[fsync]] [[MMAP]]

# WAL (Write-Ahead Log)

> Append-only durability journal: log the intent **before** mutating data pages — **Designing Data-Intensive Applications** (Kleppmann, Ch. 3).

## Mental model

Every durable DB must survive crash mid-write. WAL is the contract: **log record hits stable storage first**, then in-memory/dirty pages may change. On restart, replay log from last checkpoint forward; undo incomplete transactions.

```
Client COMMIT
    │
    ▼
Append WAL record ──► fsync WAL file     ◄── durability boundary
    │
    ▼
Return success to client
    │
    ▼
(later) Dirty pages flushed to data files   ◄── may lag; crash-safe via replay
```

- **Log sequence number (LSN)** — monotonic pointer; pages record *last WAL applied* so recovery knows what's stale.
- **Checkpoint** — periodic marker: "all changes before LSN X are on disk." Truncates replay window.
- **Steal / no-force** (see [[ARIES]]): pages may be flushed before commit (steal); committed pages need not be flushed before ack (no-force). WAL makes this safe.

Postgres: `pg_wal/` (formerly `pg_xlog`). MySQL InnoDB: redo log files. MongoDB WiredTiger: journal. SQLite: `-wal` file.

## Standard config / commands

### PostgreSQL (defaults are sane; tune under heavy write load)

```ini
# postgresql.conf
wal_level = replica          # logical decoding needs logical; replicas need replica+
fsync = on                   # NEVER off in prod except disposable dev
synchronous_commit = on      # off/local = faster, risk last ~few commits on crash
wal_compression = on         # PG14+; less I/O on wide rows
max_wal_size = 1GB           # checkpoint pressure; too low = write spikes
checkpoint_timeout = 15min
```

```sql
-- Inspect WAL pressure
SELECT pg_current_wal_lsn(), pg_walfile_name(pg_current_wal_lsn());
SELECT * FROM pg_stat_wal;

-- Force checkpoint (maintenance window only)
CHECKPOINT;
```

### MySQL InnoDB redo log

```ini
# my.cnf — redo log size affects checkpoint frequency
innodb_log_file_size = 1G
innodb_flush_log_at_trx_commit = 1   # 1 = full ACID; 2 = OS buffer, crash may lose ~1s
innodb_flush_method = O_DIRECT       # avoid double cache with FS cache
```

### fsync policy cheat sheet

| Setting | Durability | Throughput |
|---------|------------|--------------|
| PG `synchronous_commit=on` + `fsync=on` | Strong | Baseline |
| PG `synchronous_commit=off` | Last txs may vanish on crash | Higher |
| InnoDB `flush_log_at_trx_commit=2` | OS crash may lose ~1s | Higher |
| InnoDB `flush_log_at_trx_commit=0` | ~1s window always | Highest risk |

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Disk fills; `pg_wal` huge | `pg_stat_replication`; lagging replica/slot | Drop stale replication slot; fix replica; increase `max_wal_size` temporarily |
| Spiky write latency every N min | Checkpoint / WAL recycle | Raise `max_wal_size` (PG) or `innodb_log_file_size` (MySQL); spread checkpoints |
| "could not write to WAL" / PANIC | `df`; inode exhaustion; RO mount | Free disk; remount RW; restore from backup if WAL corrupt |
| Replica never catches up | `pg_stat_wal_receiver`; network; `wal_keep_size` | Fix network; increase retention; resync replica |
| After crash, long startup | Expected replay | Reduce replay window via regular checkpoints; don't disable fsync |
| MongoDB journal dir on slow disk | `db.serverStatus().wiredTiger.log` | Move journal to fast SSD; tune `storage.journal.commitIntervalMs` |

## Gotchas

> [!WARNING]
> **`fsync=off` or `innodb_flush_log_at_trx_commit=0` on prod** — you traded durability for benchmarks. One power loss = silent data loss + possible corruption.

> [!WARNING]
> **Replication slots without consumers** — Postgres retains WAL indefinitely; disk death spiral. Monitor `pg_replication_slots` + `pg_stat_replication`.

- **Group commit** batches multiple commits into one fsync — latency looks fine until fsync stalls (full disk, bad SSD firmware).
- **WAL on same spindle as data** — correlated failure + I/O contention; separate volumes on serious deployments.
- **`COMMIT` ≠ data file flush** — committed rows may live only in WAL + buffer pool until checkpoint; backup tools must be WAL-aware (PG: base backup + WAL archive; use `pg_backup_start`/`pg_basebackup`).
- **Logical decoding / CDC** holds WAL — treat slots like long-running transactions.

## When NOT to use

- **Ephemeral caches** (Redis default) — no WAL; that's by design.
- **Batch analytics where loss is OK** — consider async commit or unlogged tables (PG) with eyes open.
- **Replacing backups with WAL** — WAL is for crash recovery, not DR; you still need PITR archives and tested restores.

## Related

[[ACID]] [[ARIES]] [[write-ahead logging]] [[fsync]] [[MVCC]] [[connection pooling]] [[postgres essential]] [[MySQL storage]]
