[[Database]] [[ACID]] [[write-ahead logging]] [[ARIES]] [[MySQL Engines]] [[SQL/postgres]] [[MySQL storage]] [[SQL Configurations]]

# WAL (Write-Ahead Log)

> Append-only log of page changes written to stable storage before the data pages they describe — so a crash can replay committed work and discard incomplete transactions.

```txt
        WAL (Write-Ahead L ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers ask why dirty pages can flush after commit, what a checkpoint / …

## Sources
- [PostgreSQL Documentation — WAL Introduction](https://www.postgresql.org/docs/current/wal-intro.html) — deep-dive
- [MySQL Reference Manual — InnoDB Redo Log](https://dev.mysql.com/doc/refman/en/innodb-redo-log.html) — deep-dive
- Mohan, C. et al., "ARIES: A Transaction Recovery Method" (ACM TODS, 1992) — deep-dive
- Kleppmann, *Designing Data-Intensive Applications*, Ch. 3 — overview
- [[write-ahead logging]] — overview

## Key Concepts
- **Write-ahead rule:** log record reaches stable storage before the corresponding data-page write is…
- **LSN (Log Sequence Number):** monotonic position in the log
- **Checkpoint:** bound that lets old log be recycled once dirty pages up to that LSN are on di…
- **Redo:** reapply committed (and in-flight recoverable) changes after crash.
- **Durability policy:** full sync vs batched fsync — see [[SQL Configurations]].


- **Core:** The write-ahead log is the durable, sequential record of changes: engines app…

## Technical Details
```txt
Transaction commit
    │
    ├─► append redo records to WAL (fsync per durability policy)
    └─► dirty pages flushed later by background writer / checkpointer

Crash ──► recovery replays WAL from checkpoint LSN
```

- Why not only update pages in place?
- Random page writes are slow and not atomic at page granularity.
- Sequential log appends batch durability work and enable [[ARIES]]-style redo/…

| System | WAL name | Key identifier |
|--------|----------|----------------|
| PostgreSQL | WAL (`pg_wal`) | LSN |
| MySQL InnoDB | Redo log | LSN in `#innodb_redo` |
| SQLite | Rollback journal or WAL mode | Frame numbers |

- Durability versus performance:

- PostgreSQL `synchronous_commit=off`
- MySQL `innodb_flush_log_at_trx_commit=2`
- Money paths keep full sync enabled

- Protocol-focused sibling: [[write-ahead logging]].
- Storage layout for InnoDB: [[MySQL storage]].

## Mistakes to Avoid
- **Mistake:** Believing committed data must already sit on heap/tablespace pag…
- **Mistake:** Disabling sync on financial ledgers for benchmark glory
- **Mistake:** Starving checkpoints until the log fills and writers stall
- **Mistake:** Confusing “WAL archived for PITR” with “application-level backup…

## Pros/Cons or Trade-offs
- **Pro:** Crash safety with sequential log I/O instead of forcing every data page sync at commit.
- **Con:** Log volume, fsync latency on the commit path, and operational need to manage checkpoints.
- **Trade-off:** Full sync durability vs batched durability (throughput up; possible loss on OS crash).

## Comparison
- vs [[write-ahead logging]]: this note is the log artifact and engine names; t…


### Use cases
- Payment primary: keep sync commit on
