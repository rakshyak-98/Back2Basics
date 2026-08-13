[[SQL]] [[mysql variables]] [[Configuration]] [[SQL/postgres]]

# SQL Configurations

> Server and session parameters that control memory, connections, logging, and durability—misconfiguration often appears as timeouts or silent data loss after crash.

## Layers of configuration

| Layer | Examples |
|-------|----------|
| Server file | `postgresql.conf`, MySQL `my.cnf` |
| Runtime | `ALTER SYSTEM`, `SET GLOBAL` |
| Session | `SET work_mem`, `SET TRANSACTION` |

## High-impact knobs

| Parameter family | Risk if wrong |
|------------------|---------------|
| Memory (`shared_buffers`, `innodb_buffer_pool_size`) | OOM or cache thrashing |
| Connections (`max_connections`) | Exhaustion without [[connection pooling]] |
| Durability (`synchronous_commit`, `innodb_flush_log_at_trx_commit`) | [[ACID]] durability loss |
| Replication | Split-brain, stale reads |

## Change discipline

- Document why each non-default value exists
- Roll out one change at a time with metrics
- Keep staging proportional to production for meaningful load tests

## Sources

- PostgreSQL Documentation — [Server Configuration](https://www.postgresql.org/docs/current/runtime-config.html)
- MySQL Reference Manual — [Server System Variables](https://dev.mysql.com/doc/refman/en/server-system-variables.html)
