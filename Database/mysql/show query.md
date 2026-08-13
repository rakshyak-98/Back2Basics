[[mysql]] [[cli]] [[mysql query]]

# show query

> `SHOW …` and `INFORMATION_SCHEMA` — inspect databases, tables, grants, processlist, and engine status fast.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** `SHOW` is the quick human-facing catalog; for scripting/filters use `INFORMATION_SCHEMA` (or `performance_schema` for runtime).

```txt
SHOW DATABASES / TABLES / COLUMNS / INDEX / GRANTS / PROCESSLIST
INFORMATION_SCHEMA.* ──► same facts, SQL-filterable
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **SHOW** | Snapshot of metadata | “First tool when I don’t know the schema.” |
| **PROCESSLIST** | Running threads | “Find stuck queries / who holds locks.” |
| **VARIABLES / STATUS** | Config vs counters | “STATUS for rates; VARIABLES for knobs.” |
| **INFORMATION_SCHEMA** | SQL catalog | “Automate what SHOW prints.” |

---

## Standard config / commands

```sql
SHOW DATABASES;
SHOW CREATE DATABASE dbname;
SHOW TABLES;
SHOW FULL TABLES;                 -- BASE TABLE vs VIEW
SHOW CREATE TABLE tablename;
SHOW TABLE STATUS LIKE 'table%';
SHOW COLUMNS FROM tablename;
SHOW INDEX FROM tablename;
SHOW GRANTS FOR 'user'@'host';
SHOW PROCESSLIST;
SHOW GLOBAL VARIABLES LIKE 'innodb%';
SHOW GLOBAL STATUS LIKE 'Threads%';
SHOW ENGINES;
SHOW BINARY LOGS;
SHOW MASTER STATUS;
SHOW EVENTS;

SELECT TABLE_NAME FROM INFORMATION_SCHEMA.VIEWS
WHERE TABLE_SCHEMA = DATABASE();
```

| Knob | Why it matters |
|------|----------------|
| `SHOW FULL …` | Extra type/collation/priv columns |
| `LIKE` filters | Cut noise on big instances |
| `\G` in cli | Vertical format for wide rows |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Don’t know schema | `SHOW TABLES` / `SHOW CREATE` | Read DDL; fix wrong DB (`USE`) |
| Who is locking? | `SHOW PROCESSLIST` / InnoDB status | Kill/optimize long query |
| View vs table confusion | `SHOW FULL TABLES` | Query base table or fix view |
| Replication position | `SHOW MASTER STATUS` | Note file+pos for dump sync |

---

## Gotchas

> [!WARNING]
> **`SHOW GRANTS FROM` is wrong** — it’s `SHOW GRANTS FOR`.

> [!WARNING]
> **PROCESSLIST truncates SQL** — use `performance_schema` for full text when needed.

---

## When NOT to use

- **Application runtime catalog discovery on every request** — cache schema; don’t `SHOW` in hot paths.
- **Cross-engine monitoring** — prefer metrics exporters over scraping SHOW STATUS.

---

## Related

[[cli]] [[mysql query]] [[mysql Privileges]] [[Configuration]]
