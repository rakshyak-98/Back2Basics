[[Architectures]] [[Database]] [[ACID]] [[WAL (Write-Ahead Log)]]

# MVCC

> MVCC (Multi-Version Concurrency Control) keeps old row versions so readers see a snapshot — reads don’t block writers.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Instead of locking every reader while a writer updates in place, MVCC keeps old versions so a transaction reads the world as of its snapshot.

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

versus locking: fewer read/write stalls; cost is version storage + cleanup (VACUUM / undo purge).

---

## Standard config / commands

```sql
-- Postgres: bloat / dead tuples
SELECT relname, n_dead_tup, last_vacuum, last_autovacuum
FROM pg_stat_user_tables ORDER BY n_dead_tup DESC LIMIT 20;

VACUUM (VERBOSE) my_table;
```

MySQL/InnoDB: undo logs + purge thread play the cleanup role.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Table bloat / disk climb | dead tuples / vacuum lag | Tune autovacuum; vacuum freeze |
| Long query sees old data | snapshot age | Shorter txns; avoid idle-in-transaction |
| Update storms slow | many versions per row | Batch updates; vacuum more often |
| Serialization failure | isolation level | Retry txn; or lower isolation if safe |
| Wraparound risk (PG) | txid age alerts | Aggressive vacuum freeze |

---

## Gotchas

> [!WARNING]
> **Idle in transaction** — holds a snapshot; blocks vacuum; causes bloat.

> [!WARNING]
> **MVCC ≠ no locks** — writers still conflict on the same row; DDL and some ops take locks.

---

## When NOT to use

- **Engine without versions** — some embedded DBs use locks only.
- **You need strict serial locking semantics** — understand isolation first; don’t “turn off” MVCC casually.

---

## Related

[[ACID]] [[WAL (Write-Ahead Log)]] [[OCC]] [[Database]] [[connection pooling]]
