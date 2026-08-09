[[mysql]] [[mysql index]] [[cli]] [[mysql json]]

# mysql query

> Everyday MySQL SQL in the CLI — format results, find objects, and read metadata without guessing table names.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** `;` ends a statement with a grid; `\G` ends it with one field per line — same SQL, different display.

```txt
SELECT ... ;     → wide table
SELECT ... \G    → vertical (wide schemas)
information_schema → catalogs of tables/columns
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **`\G`** | Vertical result terminator | “I use `\G` when columns don’t fit the terminal.” |
| **information_schema** | SQL catalog views | “Find tables/columns without remembering names.” |
| **SHOW** | Quick introspection | “SHOW TABLES / COLUMNS / INDEX for triage.” |
| **COALESCE** | First non-NULL | “Fallback: hotel override else template default.” |
| **JSON_TYPE** | JSON value kind | “ARRAY vs OBJECT before treating the column.” |

---

## Standard config / commands

```mysql
SELECT * FROM t\G
SHOW FULL TABLES WHERE Table_type = 'VIEW';
SHOW FULL TABLES WHERE Table_type = 'BASE TABLE';
SHOW FULL COLUMNS FROM t;
SHOW TABLES LIKE '%user%';
SELECT CURRENT_USER();

-- find a table
SELECT table_schema, table_name
FROM information_schema.tables
WHERE table_name = 'users';

-- column map
SELECT table_name, column_name, data_type
FROM information_schema.columns
WHERE table_schema = 'your_db';

SELECT * FROM t WHERE JSON_TYPE(jcol) = 'ARRAY';
SELECT COALESCE(override_col, default_col) AS effective FROM ...;
```

Dates (ops-friendly):

```sql
SELECT DATE_FORMAT(MAX(trxnDate), '%d %b %Y, %W') AS last_day
FROM transactions;
```

| Knob | Why it matters |
|------|----------------|
| `\G` vs `;` | Readability only — not different SQL semantics |
| `information_schema` filters | Always constrain `table_schema` on busy servers |
| `SHOW FULL COLUMNS` | Nullability, defaults, privileges hints |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Unreadable wide rows | Display | Use `\G` or `pager less -S` |
| “Unknown table” | Wrong schema | `SELECT DATABASE()`; search `information_schema` |
| View vs base table confusion | `SHOW FULL TABLES` | Drop/alter the right object type |
| JSON logic wrong | `JSON_TYPE` / path | Confirm ARRAY vs OBJECT |
| COALESCE “not working” | All NULL inputs | Provide a literal default as last arg |

---

## Gotchas

> [!WARNING]
> **`\G` is a client terminator** — not sent as SQL to other drivers; don’t paste into app code.

> [!WARNING]
> **Unfiltered `information_schema` scans** — can be heavy on hosts with many schemas; always filter.

> [!WARNING]
> **`SHOW TABLES FROM db` ≠ permissions to SELECT** — visibility and DML grants differ.

---

## When NOT to use

- **Building production APIs with ad-hoc `SHOW` strings** — use migrations + typed queries.
- **Formatting dates in SQL for every UI locale** — prefer app-layer i18n when possible.
- **Scanning all of `information_schema` on a busy primary** — use replicas / tighter filters.

---

## Related

[[mysql]] [[cli]] [[mysql index]] [[mysql json]] [[show query]] [[mysql table]]
