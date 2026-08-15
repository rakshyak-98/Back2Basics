[[Database]] [[ACID]] [[write-ahead logging]] [[ARIES]] [[mysql engine]] [[SQL/postgres]] [[MySQL storage]] [[SQL Configurations]]

# WAL (Write-Ahead Log)

> Append-only log of page changes written to stable storage before the data pages they describe — so a crash can replay committed work and discard incomplete transactions.

## Interview Relevance

Interviewers ask why dirty pages can flush after commit, what a checkpoint / LSN bounds, and how durability knobs trade fsync for speed. Signal: you separate “commit durable” from “heap pages on disk” and name the crash-loss risk of async commit.

## Sources

- [PostgreSQL Documentation — WAL Introduction](https://www.postgresql.org/docs/current/wal-intro.html) — deep-dive
- [MySQL Reference Manual — InnoDB Redo Log](https://dev.mysql.com/doc/refman/en/innodb-redo-log.html) — deep-dive
- Mohan, C. et al., "ARIES: A Transaction Recovery Method" (ACM TODS, 1992) — deep-dive
- Kleppmann, *Designing Data-Intensive Applications*, Ch. 3 — overview
- [[write-ahead logging]] — overview

## Core Definition

The write-ahead log is the durable, sequential record of changes: engines append redo (and related) records, harden them per policy before acknowledging commit, then flush data pages asynchronously — recovery replays from the last checkpoint.

## Key Concepts

- **Write-ahead rule:** log record reaches stable storage before the corresponding data-page write is required for durability of that change.
- **LSN (Log Sequence Number):** monotonic position in the log; checkpoints and flush progress are tracked by LSN.
- **Checkpoint:** bound that lets old log be recycled once dirty pages up to that LSN are on disk.
- **Redo:** reapply committed (and in-flight recoverable) changes after crash.
- **Durability policy:** full sync vs batched fsync — see [[SQL Configurations]].

## Technical Details

```txt
Transaction commit
    │
    ├─► append redo records to WAL (fsync per durability policy)
    └─► dirty pages flushed later by background writer / checkpointer

Crash ──► recovery replays WAL from checkpoint LSN
```

Why not only update pages in place? Random page writes are slow and not atomic at page granularity. Sequential log appends batch durability work and enable [[ARIES]]-style redo/undo recovery.

| System | WAL name | Key identifier |
|--------|----------|----------------|
| PostgreSQL | WAL (`pg_wal`) | LSN |
| MySQL InnoDB | Redo log | LSN in `#innodb_redo` |
| SQLite | Rollback journal or WAL mode | Frame numbers |

Durability versus performance:

- PostgreSQL `synchronous_commit=off` — commit returns before WAL flush completes; crash can lose recent commits.
- MySQL `innodb_flush_log_at_trx_commit=2` — flush to OS cache each commit; `1` waits for durable media.
- Money paths keep full sync enabled; bulk-load windows may relax with explicit risk acceptance.

Protocol-focused sibling: [[write-ahead logging]]. Storage layout for InnoDB: [[MySQL storage]].

## Real-World Applications

Payment primary: keep sync commit on; size WAL/redo for peak write bursts so checkpoints do not stall writers; monitor replication lag which also rides the same log stream.

## Pros/Cons or Trade-offs

- **Pro:** Crash safety with sequential log I/O instead of forcing every data page sync at commit.
- **Con:** Log volume, fsync latency on the commit path, and operational need to manage checkpoints.
- **Trade-off:** Full sync durability vs batched durability (throughput up; possible loss on OS crash).

## Comparison

vs [[write-ahead logging]]: this note is the log artifact and engine names; that note is the protocol and operational checks. vs [[ARIES]]: ARIES is a concrete recovery algorithm built on WAL ideas. vs shadow paging: alternate durability strategy — copy-on-write pages instead of redo logs.

## Mistakes to Avoid

- Believing committed data must already sit on heap/tablespace pages at commit time.
- Disabling sync on financial ledgers for benchmark glory.
- Starving checkpoints until the log fills and writers stall.
- Confusing “WAL archived for PITR” with “application-level backup of business data.”
