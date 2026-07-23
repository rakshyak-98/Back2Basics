[[mysql]] [[SQL/SQL]] [[database migration]] [[mysql table]]

# ALTER TABLE

> One-line: evolve schema in place — adds cost (locks, rebuilds); plan online DDL, batch alters, and rollback via migrations.

## Mental model

`ALTER TABLE` changes table metadata and sometimes **rewrites the whole table** (MySQL InnoDB). Operations range from instant metadata-only (add column with default in MySQL 8+) to hours-long rebuilds on large tables.

```
ALTER types (MySQL InnoDB, simplified)
├── Instant / in-place metadata   (some ADD COLUMN in 8.0+)
├── In-place (online DDL)         (add index — still I/O heavy)
└── Copy / rebuild                (change PK, reorder columns — table lock risk)
```

Always run through **versioned migrations** ([[database migration]]), test **down** path, and measure on prod-sized snapshot first.

## Standard config / commands

### Table comment / options

```sql
ALTER TABLE hotels COMMENT = 'Hotel catalog';
ALTER TABLE hotels ENGINE=InnoDB ROW_FORMAT=DYNAMIC;
```

### Add / modify columns

```sql
ALTER TABLE hotels
  ADD COLUMN created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP AFTER name,
  MODIFY COLUMN phone VARCHAR(20) NOT NULL COMMENT 'E.164 preferred';
```

### Column reorder (full definition required)

```sql
ALTER TABLE users
  MODIFY COLUMN email VARCHAR(255) NOT NULL AFTER id;
```

### Indexes

```sql
ALTER TABLE orders ADD INDEX idx_customer_date (customer_id, order_date);
ALTER TABLE orders DROP INDEX idx_old;
```

### Online-friendly patterns (large tables)

```sql
-- pt-online-schema-change / gh-ost for zero-downtime on old MySQL or risky alters
-- MySQL 8: check ALGORITHM=INSTANT, LOCK=NONE support
ALTER TABLE t ADD COLUMN x INT, ALGORITHM=INSTANT, LOCK=DEFAULT;
```

### Postgres contrast

```sql
ALTER TABLE users ADD COLUMN email TEXT;
ALTER TABLE users ALTER COLUMN email SET NOT NULL; -- may require validation scan
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Migration hangs hours | `SHOW PROCESSLIST`; `performance_schema` | Wait or kill; use online schema tool |
| Replication lag spike | DDL on primary | Run off-peak; use parallel replica tools; throttle |
| `Lock wait timeout` | Blocking metadata lock | Find blocker; schedule maintenance window |
| App errors mid-ALTER | Partial visibility | Deploy backward-compatible code first (expand-contract) |
| Down migration fails | Data loss on DROP | Backup; avoid DROP until code deployed |
| Instant ADD fails MySQL 8 | Row size / column count limits | Fall back to copy algorithm |

## Gotchas

> [!WARNING]
> **Workbench GUI alters** — may drop/recreate table internally; always verify generated SQL.

> [!WARNING]
> **MODIFY without full spec** — can silently change nullability/defaults.

> [!WARNING]
> **Frequent column reorder in prod** — full rebuild; cosmetic order not worth it.

> [!WARNING]
> **ALTER + long transactions** — blocks and is blocked by open transactions.

## When NOT to use

- **Renaming column + app deploy atomically** — use expand-contract: add new col → dual-write → backfill → switch → drop old.
- **Massive data rewrite** — `UPDATE` in batches or ETL job, not one ALTER trick.

## Related

[[database migration]] [[mysql table]] [[mysql columns]] [[mysql lock]] [[Database mistakes]]
