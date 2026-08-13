<!-- note-strategy: operational -->
[[mysql]] [[mysql index]] [[key Constraint]] [[mysql json]]

# mysql table

> Create, copy, alter, and constrain tables — `LIKE` vs `AS SELECT`, JSON columns, FKs, and `ON UPDATE` timestamps.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** A table is rows + indexes + constraints; cloning with `LIKE` keeps indexes; `AS SELECT` copies data but drops most constraints — pick deliberately.

```txt
CREATE TABLE …          ── define columns + keys
CREATE … LIKE old       ── structure + indexes, no data
CREATE … AS SELECT      ── data + weak structure
ALTER TABLE …           ── add columns / constraints
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **LIKE** | Clone DDL | “Indexes come along; data does not.” |
| **AS SELECT** | CTAS | “Fast copy; redo indexes/FKs after.” |
| **AUTO_INCREMENT PK** | Surrogate key | “InnoDB clusters on the PK.” |
| **ON UPDATE CURRENT_TIMESTAMP** | Auto bump column | “MySQL column attribute; Postgres needs a trigger.” |
| **JSON column** | Document in a cell | “Validate JSON; index generated paths.” |

---

## Standard config / commands

```sql
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  role VARCHAR(50) DEFAULT 'guest',
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE new_table LIKE old_table;
INSERT INTO new_table SELECT * FROM old_table;

CREATE TABLE new_table AS SELECT * FROM old_table;  -- no indexes/FKs

ALTER TABLE t ADD COLUMN content JSON NULL;
UPDATE t SET content = JSON_SET(content, '$.a', 'x') WHERE id = 1;

RENAME TABLE faqs TO hotel_faqs, rooms TO hotel_rooms;
```

| Knob | Why it matters |
|------|----------------|
| Engine (InnoDB) | FKs, transactions, crash safety |
| PK design | Clustering + secondary index payload |
| Online DDL | Large ALTER can lock; plan windows / OSC |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Missing indexes after copy | Used AS SELECT | `LIKE`+INSERT or recreate indexes |
| Can’t add FK | Orphans / type mismatch | Clean data; match types |
| ALTER locks forever | Table size / algorithm | pt-osc / instant DDL where supported |
| JSON update noop | Wrong path / type | `JSON_SET` path; verify with `->>` |
| renamed table breaks app | Hardcoded names | Migrate app + views together |

---

## Gotchas

> [!WARNING]
> **`AS SELECT` is not a full clone** — triggers, FKs, and indexes usually vanish.

> [!WARNING]
> **Wide ALTER on hot tables** — can block writes; treat as an incident-class change.

---

## When NOT to use

- **Document-only workloads** — a document store may fit better than giant JSON tables.
- **Unbounded growth without partition/archive plan** — design retention first ([[mysql data partition]]).

---

## Related

[[mysql index]] [[key Constraint]] [[mysql json]] [[mysql data partition]] [[mysql]]
