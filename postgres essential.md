[[SQL/postgres]] [[postgres Error]] [[postgres parameter type error]] [[psql database dump]] [[ACID]] [[connection pooling]] [[WAL (Write-Ahead Log)]]

# postgres essential

> PostgreSQL essentials — roles, databases, connections, and the few `psql` commands you need before tuning queries or replication.

```txt
        postgres essential ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers start Postgres with cluster vs database vs schema, auth (`pg_hba…

## Sources
- [PostgreSQL Documentation — Getting Started](https://www.postgresql.org/docs/current/tutorial-start.html) — overview
- [PostgreSQL Documentation — Client Authentication](https://www.postgresql.org/docs/current/client-authentication.html) — deep-dive

## Key Concepts
- **Cluster / database / schema:** Instance → named DB → namespace (`public` default).
- **Role:** Login identity; can own objects and hold privileges.
- **Connection:** Authenticated by `pg_hba.conf` + role password/cert
- **Pooling:** Prefer [[connection pooling]] (PgBouncer) before inflating server connections.
- **Durability:** Commits hit [[WAL (Write-Ahead Log)]] before data files


- **Core:** A Postgres **cluster** is one server instance on disk (`PGDATA`)

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

- Config touchpoints: `postgresql.conf` (`shared_buffers`, `work_mem`, `max_con…

## Mistakes to Avoid
- **Mistake:** Raising `max_connections` instead of pooling
- **Mistake:** Connecting as superuser from apps
- **Mistake:** Ignoring `pg_hba` when “password authentication failed.”
- **Mistake:** Tuning queries without `EXPLAIN` or without checking for paramet…

## Pros/Cons or Trade-offs
- **Pro:** Strong SQL, MVCC, extensions, predictable ops model.
- **Con:** Connection-heavy apps without a pooler melt under load; wrong `work_mem` / vacuum settings cause silent pain.

## Comparison
- vs MySQL: different privilege model, stricter types, richer indexing (GIN/GiS…


### Use cases
- New service checklist: create role + DB, restrict `pg_hba`, put PgBouncer in …
