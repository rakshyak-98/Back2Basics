[[SQL/postgres]] [[postgres Error]] [[postgres parameter type error]] [[psql database dump]] [[ACID]] [[connection pooling]] [[WAL (Write-Ahead Log)]]

# postgres essential

> PostgreSQL essentials — roles, databases, connections, and the few `psql` commands you need before tuning queries or replication.





## Interview Relevance
Interviewers start Postgres with cluster vs database vs schema, auth (`pg_hba`), and why pools beat raising `max_connections`. Clear answers here unlock indexing and WAL follow-ups.

## Sources
- [PostgreSQL Documentation — Getting Started](https://www.postgresql.org/docs/current/tutorial-start.html) — overview
- [PostgreSQL Documentation — Client Authentication](https://www.postgresql.org/docs/current/client-authentication.html) — deep-dive

## Core Definition
A Postgres **cluster** is one server instance on disk (`PGDATA`). Inside it: databases, roles, schemas, and objects. You always connect to one database as one role.

## Key Concepts
- **Cluster / database / schema:** Instance → named DB → namespace (`public` default).
- **Role:** Login identity; can own objects and hold privileges.
- **Connection:** Authenticated by `pg_hba.conf` + role password/cert; limited by `max_connections`.
- **Pooling:** Prefer [[connection pooling]] (PgBouncer) before inflating server connections.
- **Durability:** Commits hit [[WAL (Write-Ahead Log)]] before data files — foundation of [[ACID]].

## Technical Details
```bash
psql -h localhost -U postgres -d mydb
\conninfo
\dt
\d+ my_table
\x on
```

```sql
SHOW server_version;
SHOW transaction_isolation;
SELECT pid, usename, state, query FROM pg_stat_activity;
```

Config touchpoints: `postgresql.conf` (`shared_buffers`, `work_mem`, `max_connections`); `pg_hba.conf` (trust, scram-sha-256, host rules).

## Real-World Applications
New service checklist: create role + DB, restrict `pg_hba`, put PgBouncer in front, enable `pg_stat_statements`, and practice `EXPLAIN (ANALYZE, BUFFERS)` before guessing indexes. See [[SQL/postgres]] for deeper SQL.

## Pros/Cons or Trade-offs
- **Pro:** Strong SQL, MVCC, extensions, predictable ops model.
- **Con:** Connection-heavy apps without a pooler melt under load; wrong `work_mem` / vacuum settings cause silent pain.

## Comparison
vs MySQL: different privilege model, stricter types, richer indexing (GIN/GiST). vs [[MongoDB]]: relational schemas and transactions-first vs flexible documents. Sibling errors: [[postgres Error]], [[postgres parameter type error]].

## Mistakes to Avoid
- Raising `max_connections` instead of pooling.
- Connecting as superuser from apps.
- Ignoring `pg_hba` when “password authentication failed.”
- Tuning queries without `EXPLAIN` or without checking for parameter type mismatches.
