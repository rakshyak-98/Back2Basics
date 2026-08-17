[[mysql]] [[variables]] [[SQL Configurations]] [[MySQL storage]] [[connection pooling]]

# Configuration

> MySQL server configuration via `my.cnf` / `my.cnf.d`, `SET PERSIST`, and cloud parameter groups—tune memory, logging, replication, and InnoDB for your hardware.





## Interview Relevance
Config questions test whether you size `innodb_buffer_pool_size`, enable slow query logging, and change one knob at a time with metrics. Signal: production baseline literacy, not memorizing every variable.

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

Minimal production baseline:

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

Change safely:

- One knob at a time with metrics
- Document non-defaults in runbooks
- Test on staging with realistic load

Pair `max_connections` with application [[connection pooling]] — raising the server limit alone rarely fixes exhaustion.

## Real-World Applications
Hardening a new MySQL primary before launch and tuning after a slow-query incident. Example: set buffer pool to ~70% RAM on a dedicated host, enable `slow_query_log`, then fix the top offender instead of blindly raising connections.

## Pros/Cons or Trade-offs
- **Pro:** Right-sized InnoDB and logging dramatically improve stability and debuggability.
- **Con:** Cargo-cult settings from blogs break workloads; oversized `max_connections` increases memory and contention.

## Comparison
vs [[variables]]: runtime `SHOW VARIABLES` / session settings inspect live state; Configuration is how you persist and govern those knobs. vs [[SQL Configurations]]: vault-level SQL config themes; this note is MySQL-server specific.

## Mistakes to Avoid
- Leaving `latin1` defaults on modern Unicode apps — use `utf8mb4`.
- Setting buffer pool larger than available RAM — swapping kills latency.
- Changing many parameters at once so you cannot attribute regressions.
