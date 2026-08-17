[[mysql]] [[Configuration]] [[SQL Configurations]] [[MySQL storage]] [[connection pooling]]

# variables

> MySQL system variables — global, session, or read-only — control buffers, SQL mode, replication, and InnoDB durability behavior.

```txt
        variables ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Name high-impact knobs (`innodb_buffer_pool_size`, `max_connections`, `innodb…

## Sources
- [Server System Variables](https://dev.mysql.com/doc/refman/en/server-system-variables.html) — deep-dive
- [SET PERSIST](https://dev.mysql.com/doc/refman/en/set-variable.html) — overview

## Key Concepts
- **Scope:** GLOBAL vs SESSION (`@@global.` / `@@session.`).
- **Persistence (8.0+):** `SET PERSIST` writes `mysqld-auto.cnf`.
- **Read-only vars:** Some require restart / config file.
- **SQL mode:** Strictness changes accepted data shapes.

## Technical Details
```sql
SHOW VARIABLES LIKE 'innodb%';
SELECT @@global.max_connections, @@session.sql_mode;

SET PERSIST innodb_buffer_pool_size = 8589934592;
SET GLOBAL max_connections = 500;  -- runtime only unless PERSIST
```

| Variable | Purpose |
|----------|---------|
| `innodb_buffer_pool_size` | Cache for data/index pages |
| `max_connections` | Connection ceiling |
| `innodb_flush_log_at_trx_commit` | Durability vs speed |
| `sql_mode` | Strictness (`STRICT_TRANS_TABLES`) |

## Mistakes to Avoid
- **Mistake:** Setting `innodb_flush_log_at_trx_commit=0` on money paths for “s…
- **Mistake:** Raising `max_connections` instead of fixing [[connection pooling…
- **Mistake:** Changing `sql_mode` in production without checking application a…

## Pros/Cons or Trade-offs
- **Pro:** Runtime tuning without always rebuilding images.
- **Con:** Undocumented drifts between hosts; persist files surprise you on restart.
- **Trade-off:** Durability settings that buy QPS lose crash safety.

## Comparison
- vs [[SQL Configurations]]: cross-engine config discipline; this note is MySQL…


### Use cases
- Size buffer pool to ~50–70% of dedicated DB RAM (rule of thumb)
