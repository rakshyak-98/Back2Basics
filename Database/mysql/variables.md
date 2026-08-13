[[mysql]] [[Configuration]] [[SQL Configurations]]

# variables

> MySQL system variables—global, session, or read-only—control buffer sizes, SQL modes, replication, and InnoDB behavior.

## Inspect

```sql
SHOW VARIABLES LIKE 'innodb%';
SELECT @@global.max_connections, @@session.sql_mode;
```

## Set persistence (8.0+)

```sql
SET PERSIST innodb_buffer_pool_size = 8589934592;  -- survives restart via mysqld-auto.cnf
SET GLOBAL max_connections = 500;  -- runtime only unless PERSIST
```

## High-impact variables

| Variable | Purpose |
|----------|---------|
| `innodb_buffer_pool_size` | Cache for data/index pages |
| `max_connections` | Connection ceiling |
| `innodb_flush_log_at_trx_commit` | Durability vs speed |
| `sql_mode` | Strictness (`STRICT_TRANS_TABLES`) |

## Sources

- MySQL Reference Manual — [Server System Variables](https://dev.mysql.com/doc/refman/en/server-system-variables.html)
- MySQL Reference Manual — [SET PERSIST](https://dev.mysql.com/doc/refman/en/set-variable.html)
