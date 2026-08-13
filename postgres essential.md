[[postgres essential]] [[SQL/postgres]] [[postgres Error]] [[postgres parameter type error]] [[psql database dump]] [[ACID]] [[connection pooling]]

# postgres essential

> PostgreSQL essentials — roles, databases, connections, and the few `psql` commands you need before tuning queries or replication.

---

## Core objects

| Object | Purpose |
|--------|---------|
| **Cluster** | One `postgres` server instance on disk (`PGDATA`) |
| **Database** | Isolated namespace of schemas; connection selects one DB |
| **Role / user** | Authentication identity; can own objects and hold `LOGIN` |
| **Schema** | Namespace inside a database (`public` default) |
| **Table / index** | Heap + B-tree/GiST/GIN per [[SQL/postgres]] |

## First commands (`psql`)

```bash
psql -h localhost -U postgres -d mydb
\conninfo          # current connection
\dt                # tables in search_path
\d+ my_table        # columns, indexes
\x on              # expanded output for wide rows
```

```sql
SHOW server_version;
SHOW transaction_isolation;
SELECT pid, usename, state, query FROM pg_stat_activity;
```

## Configuration touchpoints

- `postgresql.conf` — memory (`shared_buffers`, `work_mem`), connections (`max_connections`)
- `pg_hba.conf` — who can connect from which host (trust, scram-sha-256)
- Connection pooling — prefer [[connection pooling]] (PgBouncer) before raising `max_connections`

## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| `password authentication failed` | `pg_hba.conf`; role password | `ALTER ROLE … PASSWORD`; match auth method |
| `too many connections` | `pg_stat_activity`; pooler | Pool via PgBouncer; lower idle clients |
| `inconsistent types deduced for parameter $n` | Query + column types | See [[postgres parameter type error]] |
| Disk growth | Largest tables; WAL | `VACUUM`; archive or tune `max_wal_size` |
| Slow queries | `pg_stat_statements` | Indexes; `EXPLAIN (ANALYZE, BUFFERS)` |

## Related

[[SQL/postgres]] · [[postgres Error]] · [[ACID]] · [[WAL (Write-Ahead Log)]] · [[psql database dump]]

## Sources

- [PostgreSQL Documentation — Getting Started](https://www.postgresql.org/docs/current/tutorial-start.html)
- [Wikipedia — PostgreSQL](https://en.wikipedia.org/wiki/PostgreSQL)
