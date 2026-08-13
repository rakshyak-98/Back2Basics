[[mysql]] [[variables]] [[SQL Configurations]] [[MySQL storage]]

# Configuration

> MySQL server configuration via `my.cnf` / `my.cnf.d`, `SET PERSIST`, and cloud parameter groups—tune memory, logging, replication, and InnoDB for your hardware.

## File locations

| OS | Typical path |
|----|--------------|
| Linux | `/etc/my.cnf`, `/etc/mysql/my.cnf` |
| Docker | `/etc/mysql/conf.d/*.cnf` |

## Minimal production baseline

```ini
[mysqld]
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci
innodb_buffer_pool_size = 70% of RAM (dedicated server)
innodb_redo_log_capacity = sized for write throughput
max_connections = 500  # with app-side pooling
slow_query_log = 1
long_query_time = 1
```

## Change safely

- One knob at a time with metrics
- Document non-defaults in runbooks
- Test on staging with realistic load

## Sources

- MySQL Reference Manual — [Server Configuration](https://dev.mysql.com/doc/refman/en/server-configuration.html)
- MySQL Reference Manual — [InnoDB Configuration](https://dev.mysql.com/doc/refman/en/innodb-configuration.html)
