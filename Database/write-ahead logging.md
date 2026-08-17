[[WAL (Write-Ahead Log)]] [[ACID]] [[ARIES]] [[mysql engine]] [[SQL/postgres]] [[MySQL storage]]

# write-ahead logging

> Protocol: append change records to a log and harden them before acknowledging commit — the foundation of crash-safe [[ACID]] durability in PostgreSQL, InnoDB, and most relational engines.

```txt
        write-ahead loggin ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Explain why dirty pages can flush later than commit, what a checkpoint LSN do…

## Sources
- [PostgreSQL WAL](https://www.postgresql.org/docs/current/wal.html) — deep-dive
- [InnoDB Recovery](https://dev.mysql.com/doc/refman/en/innodb-recovery.html) — deep-dive
- [Write-ahead logging (Wikipedia)](https://en.wikipedia.org/wiki/Write-ahead_logging) — overview
- [[ARIES]] — deep-dive

## Key Concepts
- **Core:** WAL separates “make commit durable” from “write data pages.” Recovery replays…

## Technical Details
1. Transaction modifies pages in the **buffer pool**.
2. Engine appends **redo** to the [[WAL (Write-Ahead Log)]].
3. On `COMMIT`, log reaches durable media (policy-dependent).
4. Dirty pages flush asynchronously later.

```sql
-- PostgreSQL
SELECT pg_current_wal_lsn();

-- MySQL InnoDB
SHOW ENGINE INNODB STATUS\G
```

- Long checkpoints or tiny log capacity increase write amplification and stall …

## Mistakes to Avoid
- **Mistake:** Believing committed data is on the heap pages at commit time
- **Mistake:** Disabling sync on financial ledgers for benchmark glory
- **Mistake:** Starving checkpoints until the log fills and writers stall

## Pros/Cons or Trade-offs
- **Pro:** Crash safety with sequential log I/O instead of only random page writes.
- **Con:** Log I/O and fsync latency on the commit path; operational need to manage log volume.
- **Trade-off:** Full sync commit vs batched durability (possible loss on OS crash).

## Comparison
- vs [[WAL (Write-Ahead Log)]]: that note is the log artifact/LSN view


### Use cases
- Tuning `synchronous_commit` / `innodb_flush_log_at_trx_commit` for money path…
