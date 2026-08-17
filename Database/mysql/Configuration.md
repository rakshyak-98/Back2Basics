[[mysql]] [[variables]] [[SQL Configurations]] [[MySQL storage]] [[connection pooling]]

# Configuration

> MySQL server configuration via `my.cnf` / `my.cnf.d`, `SET PERSIST`, and cloud parameter groups—tune memory, logging, replication, and InnoDB for your hardware.

```txt
        Configuration ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Config questions test whether you size `innodb_buffer_pool_size`, enable slow…

## Sources
- [MySQL Reference Manual — Server Configuration](https://dev.mysql.com/doc/refman/en/server-configuration.html) — overview
- [MySQL Reference Manual — InnoDB Configuration](https://dev.mysql.com/doc/refman/en/innodb-configuration.html) — deep-dive

## Key Concepts
- **File + dynamic settings:** `my.cnf` for boot; `SET PERSIST` / parameter groups for managed changes.
- **Memory first:** buffer pool dominates dedicated DB hosts.
- **Observability knobs:** slow query log and thresholds catch regressions.
- **Safe change discipline:** one knob, measure, document non-defaults.

## Technical Details
| OS | Typical path |
|----|--------------|
| Linux | `/etc/my.cnf`, `/etc/mysql/my.cnf` |
| Docker | `/etc/mysql/conf.d/*.cnf` |

- Minimal production baseline:

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

- Change safely:

- One knob at a time with metrics
- Document non-defaults in runbooks
- Test on staging with realistic load

- Pair `max_connections` with application [[connection pooling]]

## Mistakes to Avoid
- **Mistake:** Leaving `latin1` defaults on modern Unicode apps — use `utf8mb4`
- **Mistake:** Setting buffer pool larger than available RAM
- **Mistake:** Changing many parameters at once so you cannot attribute regress…

## Pros/Cons or Trade-offs
- **Pro:** Right-sized InnoDB and logging dramatically improve stability and debuggability.
- **Con:** Cargo-cult settings from blogs break workloads; oversized `max_connections` increases memory and contention.

## Comparison
- vs [[variables]]: runtime `SHOW VARIABLES` / session settings inspect live st…


### Use cases
- Hardening a new MySQL primary before launch and tuning after a slow-query inc…
