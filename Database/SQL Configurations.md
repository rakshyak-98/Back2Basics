[[SQL]] [[mysql variables]] [[Configuration]] [[SQL/postgres]] [[connection pooling]] [[ACID]] [[WAL (Write-Ahead Log)]]

# SQL Configurations

> Server and session parameters that control memory, connections, logging, and durability — misconfiguration often shows up as timeouts or silent data loss after a crash.

## Interview Relevance

Interviewers ask how you size buffer pools, cap connections, and choose durability knobs. Signal: you change one setting at a time, know what breaks under load, and never trade crash safety on money paths for a benchmark score.

## Sources

- [PostgreSQL Documentation — Server Configuration](https://www.postgresql.org/docs/current/runtime-config.html) — deep-dive
- [MySQL Reference Manual — Server System Variables](https://dev.mysql.com/doc/refman/en/server-system-variables.html) — deep-dive
- [PostgreSQL Documentation — Resource Consumption](https://www.postgresql.org/docs/current/runtime-config-resource.html) — overview
- Kleppmann, *Designing Data-Intensive Applications*, Ch. 3 — overview

## Core Definition

SQL engines expose layered settings (file, runtime, session) that trade memory, concurrency, and durability. Wrong values starve caches, exhaust connection slots, or acknowledge commits that are not yet on stable storage.

## Key Concepts

- **Server file:** `postgresql.conf`, MySQL `my.cnf` / `mysqld.cnf` — defaults that survive restart.
- **Runtime change:** `ALTER SYSTEM`, `SET GLOBAL` — live adjustments; some need restart or `SIGHUP`.
- **Session override:** `SET work_mem`, `SET TRANSACTION` — per-connection without changing the fleet.
- **Memory family:** `shared_buffers` / `innodb_buffer_pool_size` — too small thrash; too large invites OOM with OS cache.
- **Connection family:** `max_connections` without [[connection pooling]] exhausts RAM and scheduler time.
- **Durability family:** `synchronous_commit`, `innodb_flush_log_at_trx_commit` — [[ACID]] durability vs fsync latency.

## Technical Details

| Layer | Examples | Scope |
|-------|----------|-------|
| Server file | `postgresql.conf`, `my.cnf` | Process defaults |
| Runtime | `ALTER SYSTEM`, `SET GLOBAL` | Instance-wide |
| Session | `SET work_mem`, `SET TRANSACTION` | One connection |

High-impact knobs and failure modes:

| Parameter family | Risk if wrong |
|------------------|---------------|
| Memory (`shared_buffers`, `innodb_buffer_pool_size`) | OOM or cache thrashing |
| Connections (`max_connections`) | Slot exhaustion without [[connection pooling]] |
| Durability (`synchronous_commit`, `innodb_flush_log_at_trx_commit`) | Lost commits after crash |
| Replication | Split-brain, stale reads if lag ignored |
| Logging / statement timeout | Disk fill or runaway queries holding locks |

Change discipline:

1. Document why each non-default value exists.
2. Roll out one change at a time with metrics (latency, buffer hit rate, fsync wait, connection wait).
3. Keep staging sized so load tests exercise the same knobs as production.

```sql
-- PostgreSQL: inspect and set (example)
SHOW shared_buffers;
ALTER SYSTEM SET work_mem = '64MB';  -- then reload

-- MySQL: buffer pool and durability
SHOW VARIABLES LIKE 'innodb_buffer_pool_size';
SET GLOBAL innodb_flush_log_at_trx_commit = 1;
```

*What fails first after raising `max_connections` without a pool?* Memory and context-switch cost — each backend/thread holds private state even when idle.

## Real-World Applications

Sizing a new primary: set buffer pool to a large fraction of RAM (engine docs as baseline), put PgBouncer or a pooler in front, keep full sync commit on payment databases, and lower durability only for bulk-load windows with explicit risk acceptance.

## Pros/Cons or Trade-offs

- **Pro:** Tunable memory and durability let one engine serve both interactive [[OLTP]] and controlled batch windows.
- **Con:** Opaque defaults hide crash-loss and connection storms until an incident.
- **Trade-off:** Full fsync on every commit vs batched durability (faster; possible loss on OS crash).

## Comparison

vs [[SQL/postgres]] / [[mysql]]: those notes cover engine features; this note is the operational parameter surface. vs [[connection pooling]]: pooling reduces need for huge `max_connections`. vs [[WAL (Write-Ahead Log)]]: WAL is the mechanism; durability knobs choose how hard you wait for it.

## Mistakes to Avoid

- Copying cloud “performance” recipes that turn off sync commit on ledgers.
- Raising `max_connections` instead of adding a pooler.
- Changing five parameters in one deploy so you cannot attribute the outage.
- Tuning staging on a tiny box and expecting production buffer behavior to match.
