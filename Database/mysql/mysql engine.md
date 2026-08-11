[[mysql]] [[MySQL Engines]] [[ACID]] [[mysql lock]] [[write-ahead logging]]

# mysql engine

> A storage engine is how MySQL stores and locks a table — pick InnoDB unless you have a sharp reason not to.

---

## Mental model

**Say it in one breath:** `ENGINE=...` on a table chooses persistence, locking, transactions, and indexes — InnoDB is the production default.

```txt
SQL layer (parse / optimize)
        │
        ▼
   storage engine ──► InnoDB (default) | MyISAM | MEMORY | CSV | …
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **InnoDB** | Transactional engine | “Row locks, FK, crash recovery — default.” |
| **MyISAM** | Old table-lock engine | “No txns; legacy read-heavy only.” |
| **MEMORY** | RAM tables | “Fast and volatile — gone on restart.” |
| **MVCC** | Readers don’t block writers (versioned rows) | “Consistent reads without locking every row.” |
| **Clustered PK** | Data ordered by primary key | “Secondary indexes store the PK.” |
| **WAL / redo** | Crash safety for InnoDB | “Committed work survives process death.” |

### Comparison (keep short)

| Feature | InnoDB | MyISAM | MEMORY |
|---------|--------|--------|--------|
| Persistence | Yes | Yes | No (RAM) |
| Transactions | Yes | No | No |
| Locking | Row | Table | Table |
| Foreign keys | Yes | No | No |
| Crash recovery | Auto | Repair | Data lost |
| Index default | BTREE | BTREE | HASH |

---

## Standard config / commands

```mysql
CREATE TABLE t (
  id INT PRIMARY KEY,
  name VARCHAR(100)
) ENGINE=InnoDB;

SHOW TABLE STATUS WHERE Name = 't';
SELECT ENGINE FROM information_schema.TABLES
WHERE TABLE_SCHEMA = 'db' AND TABLE_NAME = 't';

ALTER TABLE t ENGINE=InnoDB;   -- convert (plan downtime / locks)
```

| Knob | Why it matters |
|------|----------------|
| Default engine | `default_storage_engine` — new tables inherit it |
| Per-table ENGINE | Mixed engines = mixed semantics (surprises) |
| Convert MyISAM→InnoDB | Gains txns/FK; check disk + rebuild time |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| No rollback / partial writes | `SHOW TABLE STATUS` → MyISAM | Convert to InnoDB |
| Whole table locks under load | Engine / `LOCK TABLES` | InnoDB + row locks |
| FK create rejected | Engine ≠ InnoDB | Use InnoDB both sides |
| Data gone after restart | MEMORY / tmp | Persist to InnoDB |
| HASH index “ignored” | InnoDB table | Expected — BTREE only |

---

## Gotchas

> [!WARNING]
> **Engine is per table** — one MyISAM table in an InnoDB app breaks transactional assumptions across joins.

> [!WARNING]
> **`ALTER ... ENGINE=` rebuilds the table** — size and locks matter in prod.

> [!WARNING]
> **MEMORY is not a cache tier you forget** — process restart empties it.

---

## When NOT to use

- **MyISAM for new apps** — no ACID; prefer InnoDB.
- **MEMORY for durable business data** — use InnoDB (or Redis with clear TTL semantics).
- **“One engine for everything exotic”** — CSV/ARCHIVE are niche export/archive tools, not OLTP.

---

## Related

[[MySQL Engines]] [[mysql]] [[ACID]] [[mysql lock]] [[mysql transaction]] [[mysql index]] [[write-ahead logging]] [[memory engine]]
