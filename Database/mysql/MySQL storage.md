[[mysql engine]] [[write-ahead logging]] [[mysql index]] [[Configuration]] [[WAL (Write-Ahead Log)]] [[ACID]] [[mysql transaction]] [[SQL Configurations]] [[MMAP]]

# MySQL storage

> How InnoDB lays out tablespaces, buffer pool pages, redo/undo, and the doublewrite buffer on disk — the physical layer behind [[mysql transaction]] durability.





## Interview Relevance
Interviewers ask what `innodb_buffer_pool_size` does, why redo exists beside data files, and what doublewrite prevents. Signal: you can sketch buffer pool → dirty pages → `.ibd` plus redo for crash recovery, and name durability knobs.

## Sources
- [MySQL Reference Manual — InnoDB Disk Layout](https://dev.mysql.com/doc/refman/en/innodb-disk-layout.html) — deep-dive
- [MySQL Reference Manual — InnoDB Buffer Pool](https://dev.mysql.com/doc/refman/en/innodb-buffer-pool.html) — deep-dive
- [MySQL Reference Manual — InnoDB Redo Log](https://dev.mysql.com/doc/refman/en/innodb-redo-log.html) — overview
- [MySQL Reference Manual — Doublewrite Buffer](https://dev.mysql.com/doc/refman/en/innodb-doublewrite-buffer.html) — overview
- Kleppmann, *Designing Data-Intensive Applications*, Ch. 3 — overview

## Core Definition
InnoDB storage is a buffer-pooled page cache over tablespace files, with redo for write-ahead durability and undo for rollback/MVCC — crash recovery replays redo from the last checkpoint rather than trusting only heap pages on disk.

## Key Concepts
- **Buffer pool:** RAM cache of data and index pages; primary memory knob.
- **Tablespace (`.ibd`):** on-disk pages for table/index data (file-per-table common).
- **Redo log:** sequential [[WAL (Write-Ahead Log)]] for crash recovery.
- **Undo:** old row versions for rollback and consistent reads.
- **Doublewrite buffer:** torn-page protection before writing pages to tablespaces.
- **Checkpoint:** progress point allowing redo reuse once dirty pages are flushed.

## Technical Details
```txt
Buffer pool (RAM) ──► dirty pages ──► .ibd tablespace files
        │
        ├── redo log (#innodb_redo) ──► crash recovery
        └── undo ──► rollback / MVCC reads
```

Tablespaces:

- **File-per-table** (`innodb_file_per_table=ON`) — each table (typically) gets its own `.ibd`.
- **System tablespace** — data dictionary and historically undo (version-dependent layouts).

Tuning (see also [[SQL Configurations]]):

| Knob | Role |
|------|------|
| `innodb_buffer_pool_size` | Cache hit rate vs RAM pressure |
| `innodb_redo_log_capacity` | Write burst absorption vs checkpoint frequency |
| `innodb_flush_log_at_trx_commit` | `1` = full durability; `2`/`0` trade safety for speed |
| Doublewrite | Leave enabled unless you fully understand torn-page risk |

```sql
SHOW VARIABLES LIKE 'innodb_buffer_pool_size';
SHOW VARIABLES LIKE 'innodb_redo_log_capacity';
SHOW ENGINE INNODB STATUS\G
```

Contrast: relational engines usually use explicit buffer pools + WAL, not sole reliance on [[MMAP]] for durability.

## Real-World Applications
Size buffer pool to most of dedicated DB RAM on an [[OLTP]] primary; keep `innodb_flush_log_at_trx_commit=1` for payments; grow redo capacity before Black Friday write spikes so checkpoints do not stall commits.

## Pros/Cons or Trade-offs
- **Pro:** Crash-safe durability with sequential redo and mature page management.
- **Con:** Many moving parts (pool, redo, undo, doublewrite); mis-sizing causes stalls or OOM.
- **Trade-off:** Full sync commit vs batched flush (throughput vs possible loss on OS crash).

## Comparison
vs [[mysql engine]] / [[MySQL Engines]]: engine choice (InnoDB vs others); this note is InnoDB’s on-disk/memory anatomy. vs [[WAL (Write-Ahead Log)]]: general WAL idea; here redo is the InnoDB instance. vs [[WiredTiger storage engine]]: MongoDB’s document engine — different concurrency and checkpoint model.

## Mistakes to Avoid
- Tiny buffer pool on a large working set (chronic I/O).
- Disabling doublewrite without understanding partial-page write risk.
- Setting flush-at-commit to `0` on ledgers for benchmark wins.
- Assuming “committed” means the `.ibd` page is already flushed — redo is what made commit durable.
