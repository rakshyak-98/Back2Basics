[[Architectures]] [[Database]] [[ACID]] [[WAL (Write-Ahead Log)]] [[OCC]] [[connection pooling]]

# MVCC

> MVCC (Multi-Version Concurrency Control) keeps old row versions so readers see a snapshot — reads don’t block writers.

```txt
        MVCC ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Interview Relevance
- **Interview probes:** MVCC is the Postgres/InnoDB concurrency story

## Sources
- [PostgreSQL — Concurrency Control](https://www.postgresql.org/docs/current/mvcc.html) — deep-dive
- [Wikipedia — Multiversion concurrency control](https://en.wikipedia.org/wiki/Multiversion_concurrency_control) — overview

## Key Concepts
```txt
Writer updates row  →  new version (xmin=TxW)
Reader with older snapshot  →  still sees previous version
VACUUM / purge  →  removes versions no one can see
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Snapshot** | Which versions this txn may see | “My read sees data committed before my snapshot.” |
| **xmin / xmax** | Postgres hidden create/delete tx ids | “xmax marks a row version dead for new readers.” |
| **Tuple version** | One physical row edition | “Updates append a version; they don’t overwrite in place.” |
| **VACUUM** | Reclaim dead versions | “Without vacuum, tables bloat.” |
| **Writers vs readers** | Don’t block each other (usually) | “Readers don’t block writers under MVCC.” |

- **Note:** versus locking: fewer read/write stalls

## Technical Details
```sql
-- Postgres: bloat / dead tuples
SELECT relname, n_dead_tup, last_vacuum, last_autovacuum
FROM pg_stat_user_tables ORDER BY n_dead_tup DESC LIMIT 20;

VACUUM (VERBOSE) my_table;
```

- MySQL/InnoDB: undo logs + purge thread play the cleanup role.

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| Table bloat / disk climb | dead tuples / vacuum lag | Tune autovacuum; vacuum freeze |
| Long query sees old data | snapshot age | Shorter txns; avoid idle-in-transaction |
| Update storms slow | many versions per row | Batch updates; vacuum more often |
| Serialization failure | isolation level | Retry txn; or lower isolation if safe |
| Wraparound risk (PG) | txid age alerts | Aggressive vacuum freeze |

## Mistakes to Avoid
- **Mistake:** Idle in transaction
- **Mistake:** MVCC ≠ no locks

## Pros/Cons or Trade-offs
- **Trade-off:** Engine without versions — some embedded DBs use locks only.
- **Trade-off:** You need strict serial locking semantics — understand isolation first; don’t “turn off” MVCC casually.
