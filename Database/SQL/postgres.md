[[Database]] [[SQL]] [[ACID]] [[GIN]] [[psql essential]] [[postgres Error]]

# postgres

> PostgreSQL—open-source object-relational database with strong [[ACID]] defaults, extensible types, and [[MVCC]] concurrency without read locks blocking writers.

## Architecture snapshot

```txt
Client ──► postmaster ──► backend process per connection
                              │
                              ├── planner/executor
                              ├── shared_buffers + WAL
                              └── background (autovacuum, checkpointer)
```

## Distinctive strengths

- Rich types (`jsonb`, arrays, ranges, UUID)
- Partial and expression indexes; [[GIN]] / GiST
- Table inheritance, partitioning, foreign data wrappers
- Serializable Snapshot Isolation at `SERIALIZABLE` level

## Defaults worth knowing

| Setting | Default | Note |
|---------|---------|------|
| Isolation | READ COMMITTED | New snapshot per statement |
| `synchronous_commit` | on | Durability before commit ack |
| Autovacuum | on | Required for [[MVCC]] tuple cleanup |

## CLI and ops entry points

- [[psql essential]] — interactive shell
- [[psql database dump]] — logical backups with `pg_dump`
- [[ACL (postgreSQL)]] — privilege model

## Sources

- PostgreSQL Documentation — [https://www.postgresql.org/docs/current/](https://www.postgresql.org/docs/current/)
- PostgreSQL Global Development Group — [About PostgreSQL](https://www.postgresql.org/about/)
