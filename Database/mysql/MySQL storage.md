[[mysql engine]] [[write-ahead logging]] [[mysql index]] [[Configuration]] [[WAL (Write-Ahead Log)]] [[ACID]] [[mysql transaction]] [[SQL Configurations]] [[MMAP]]

# MySQL storage

> How InnoDB lays out tablespaces, buffer pool pages, redo/undo, and the doublewrite buffer on disk — the physical layer behind [[mysql transaction]] durability.

```txt
        MySQL storage ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers ask what `innodb_buffer_pool_size` does, why redo exists beside …

## Sources
- [MySQL Reference Manual — InnoDB Disk Layout](https://dev.mysql.com/doc/refman/en/innodb-disk-layout.html) — deep-dive
- [MySQL Reference Manual — InnoDB Buffer Pool](https://dev.mysql.com/doc/refman/en/innodb-buffer-pool.html) — deep-dive
- [MySQL Reference Manual — InnoDB Redo Log](https://dev.mysql.com/doc/refman/en/innodb-redo-log.html) — overview
- [MySQL Reference Manual — Doublewrite Buffer](https://dev.mysql.com/doc/refman/en/innodb-doublewrite-buffer.html) — overview
- Kleppmann, *Designing Data-Intensive Applications*, Ch. 3 — overview

## Key Concepts
- **Buffer pool:** RAM cache of data and index pages; primary memory knob.
- **Tablespace (`.ibd`):** on-disk pages for table/index data (file-per-table common).
- **Redo log:** sequential [[WAL (Write-Ahead Log)]] for crash recovery.
- **Undo:** old row versions for rollback and consistent reads.
- **Doublewrite buffer:** torn-page protection before writing pages to tablespaces.
- **Checkpoint:** progress point allowing redo reuse once dirty pages are flushed.


- **Core:** InnoDB storage is a buffer-pooled page cache over tablespace files, with redo…

## Technical Details
```txt
Buffer pool (RAM) ──► dirty pages ──► .ibd tablespace files
        │
        ├── redo log (#innodb_redo) ──► crash recovery
        └── undo ──► rollback / MVCC reads
```

- Tablespaces:

- **File-per-table:** (`innodb_file_per_table=ON`) — each table (typically) gets its own `.ibd`.
- **System tablespace:** — data dictionary and historically undo (version-dependent layouts).

- Tuning (see also [[SQL Configurations]]):

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

- Contrast: relational engines usually use explicit buffer pools + WAL, not sol…

## Mistakes to Avoid
- **Mistake:** Tiny buffer pool on a large working set (chronic I/O)
- **Mistake:** Disabling doublewrite without understanding partial-page write r…
- **Mistake:** Setting flush-at-commit to `0` on ledgers for benchmark wins
- **Mistake:** Assuming “committed” means the `.ibd` page is already flushed

## Pros/Cons or Trade-offs
- **Pro:** Crash-safe durability with sequential redo and mature page management.
- **Con:** Many moving parts (pool, redo, undo, doublewrite); mis-sizing causes stalls or OOM.
- **Trade-off:** Full sync commit vs batched flush (throughput vs possible loss on OS crash).

## Comparison
- vs [[mysql engine]] / [[MySQL Engines]]: engine choice (InnoDB vs others); th…


### Use cases
- Size buffer pool to most of dedicated DB RAM on an [[OLTP]] primary
