[[MySQL Engines]] [[MySQL storage]] [[memory engine]] [[InnoDB]] [[mysql table]]

# MySQL Engines

> A MySQL storage engine is the pluggable backend that handles how a table stores rows, enforces transactions, and locks concurrent access — InnoDB is the production default for almost all durable OLTP data.

---

## Why It Matters

`CREATE TABLE … ENGINE=InnoDB` is not cosmetic — it determines whether you get row-level locking, crash recovery, foreign keys, and MVCC transactions. Legacy schemas sometimes contain MyISAM, CSV, or MEMORY tables from older defaults or quick prototypes. Auditing `SHOW ENGINES` before an HA migration or replication setup prevents surprises when a "table" turns out to have no transaction log.

---

## Sources

- [MySQL Reference Manual — Storage Engines](https://dev.mysql.com/doc/refman/en/storage-engines.html) — Complete list of engines, feature matrix, and when to use each.
- [MySQL Reference Manual — InnoDB Storage Engine](https://dev.mysql.com/doc/refman/en/innodb-storage-engine.html) — InnoDB architecture: buffer pool, redo log, MVCC, and row-level locking.
- [MySQL Reference Manual — Alternative Storage Engines](https://dev.mysql.com/doc/refman/en/storage-engines.html) — MEMORY, CSV, ARCHIVE, and other specialty engines with explicit limitations.

---

## Key Concepts

MySQL separates the SQL layer from storage via a **handler interface**. Each table declares its engine with `ENGINE=` at creation time. You can mix engines in one database — but mixed semantics under failure are hard to reason about.

| Engine | Transactions | Row locking | Crash recovery | Typical use |
|--------|-------------|-------------|----------------|-------------|
| **InnoDB** | Yes (ACID) | Yes | Yes (redo log) | Default OLTP — use unless documented exception |
| **MEMORY** | No | Table lock | No (data lost on restart) | Session caches, temp tables |
| **CSV** | No | Table lock | No | Data exchange via CSV files |
| **ARCHIVE** | No | Insert only | Limited | Compressed append-only logs |
| **MyISAM** | No | Table lock | No | Legacy — migrate to InnoDB |
| **BLACKHOLE** | No | N/A | N/A | Replication filtering (discards writes) |

```txt
SQL layer (parser, optimizer)
        │
        ▼
Storage engine API (handler)
        │
   ┌────┴────┬─────────┐
InnoDB   MEMORY   CSV …
```

---

## Technical Details

### Inspect available engines

```sql
SHOW ENGINES;
SELECT ENGINE, SUPPORT, COMMENT FROM information_schema.ENGINES;
-- SUPPORT: YES, DEFAULT, NO, DISABLED, MERGED
```

### Check engine per table

```sql
SELECT TABLE_NAME, ENGINE
FROM information_schema.TABLES
WHERE TABLE_SCHEMA = 'myapp'
  AND ENGINE != 'InnoDB';
```

### Convert legacy table to InnoDB

```sql
ALTER TABLE legacy_stats ENGINE=InnoDB;
-- Runs online in MySQL 8+ with ALGORITHM=INPLACE for many cases
-- Verify: SHOW TABLE STATUS LIKE 'legacy_stats';
```

### InnoDB highlights (why it is default)

- **MVCC** — readers do not block writers; consistent snapshots via undo log.
- **Row-level locking** — concurrent updates to different rows in the same table.
- **Crash recovery** — redo log replays committed transactions after power loss.
- **Foreign keys** — referential integrity enforced at storage layer.
- **Buffer pool** — caches data and index pages in memory.

### When specialty engines are justified

| Engine | Justified when |
|--------|----------------|
| MEMORY | Explicitly ephemeral data; acceptable data loss on restart |
| CSV | Interchange with spreadsheet tools; not for concurrent writes |
| ARCHIVE | Write-once compressed storage; no UPDATE/DELETE needed |
| BLACKHOLE | Replication topology testing; master accepts writes, slave receives none |

---

## Mistakes to Avoid

- Shipping CSV or MEMORY engines for durable user data.
- Ignoring `SHOW ENGINES` on managed MySQL (RDS, Cloud SQL) where some engines are disabled.
- Assuming ARCHIVE supports UPDATE — insert-only semantics.
- Mixing MyISAM and InnoDB in one transactional workflow — no cross-engine transactions.

---

## Pros/Cons or Trade-offs

| Pro | Con |
|-----|-----|
| Flexibility for niche table roles | Mixed engines = mixed durability semantics |
| InnoDB covers 99% of production needs | Specialty engines tempt shortcuts that become permanent |

---

## Comparison

| vs | Distinction |
|----|-------------|
| [[memory engine]] | Deep dive on MEMORY engine semantics |
| [[MySQL storage]] | Physical storage layout and tablespaces |
| PostgreSQL | No pluggable per-table engines — single storage engine |

---

## Use cases

- Schema audit before cloud migration: find non-InnoDB tables and convert.
- Session store in MEMORY for a read-heavy cache table — with acceptance of data loss on restart.
- ARCHIVE for compressed historical logs that are insert-only.
