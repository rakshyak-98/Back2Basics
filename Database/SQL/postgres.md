[[Database]] [[SQL]] [[ACID]] [[GIN]] [[psql essential]] [[postgres Error]] [[MVCC]] [[WAL (Write-Ahead Log)]] [[SQL Configurations]] [[ACL (postgreSQL)]]

# postgres

> PostgreSQL — open-source object-relational database with strong [[ACID]] defaults, extensible types, and [[MVCC]] concurrency so readers do not block writers.

```txt
        postgres ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers probe MVCC (visibility, vacuum), isolation defaults, indexing (`…

## Sources
- [PostgreSQL Documentation](https://www.postgresql.org/docs/current/) — deep-dive
- [PostgreSQL Global Development Group — About PostgreSQL](https://www.postgresql.org/about/) — overview
- [PostgreSQL Documentation — Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html) — deep-dive
- [PostgreSQL Documentation — WAL Internals](https://www.postgresql.org/docs/current/wal-intro.html) — overview
- Kleppmann, *Designing Data-Intensive Applications*, Ch. 3–7 — overview

## Key Concepts
- **Postmaster + backends:** one OS process per connection; shared memory for buffers and locks.
- **MVCC:** versions of rows
- **Autovacuum:** reclaims dead tuples and freezes XIDs
- **Extensible types:** `jsonb`, arrays, ranges, UUID, custom types and operators.
- **Index variety:** B-tree, partial, expression, [[GIN]] / GiST / BRIN.
- **Isolation:** default READ COMMITTED; `SERIALIZABLE` uses Serializable Snapshot Isolation.


- **Core:** PostgreSQL is a process-per-connection object-relational engine: a postmaster…

## Technical Details
```txt
Client ──► postmaster ──► backend process per connection
                              │
                              ├── parser / rewriter / planner / executor
                              ├── shared_buffers + WAL
                              └── background (autovacuum, checkpointer, walwriter)
```

| Setting | Default | Note |
|---------|---------|------|
| Isolation | READ COMMITTED | New snapshot per statement |
| `synchronous_commit` | on | Durability before commit ack |
| Autovacuum | on | Dead-tuple cleanup and XID freeze |
| `shared_buffers` | often ~128MB stock | Raise for real workloads; see [[SQL Configurations]] |

- Distinctive strengths:

- Partial and expression indexes; [[GIN]] for `jsonb` / full-text
- Declarative partitioning, table inheritance (legacy patterns), foreign data w…
- Logical decoding / replication slots for change-data-capture

- CLI and ops entry points:

- [[psql essential]] — interactive shell
- [[psql database dump]] — logical backups with `pg_dump`
- [[ACL (postgreSQL)]] — roles and privileges
- [[postgres Error]] — SQLSTATE and recovery

```sql
SHOW transaction_isolation;
SELECT pg_current_wal_lsn();
-- Prefer SERIALIZABLE when write skew matters; retry on serialization_failure
BEGIN;
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
-- ...
COMMIT;
```

## Mistakes to Avoid
- **Mistake:** Turning off autovacuum “for performance.”
- **Mistake:** Skipping connection pooling and opening thousands of backends
- **Mistake:** Treating `jsonb` as a substitute for modeling hot query paths wi…
- **Mistake:** Ignoring `serialization_failure` retries under SERIALIZABLE

## Pros/Cons or Trade-offs
- **Pro:** Strong defaults, rich SQL, extensibility without leaving the engine.
- **Con:** Process-per-connection needs pooling at scale; vacuum debt causes bloat and wraparound risk.
- **Trade-off:** Strict isolation / sync commit vs throughput under write-heavy load.

## Comparison
- vs [[mysql]]: PostgreSQL leans MVCC snapshots and richer types


### Use cases
- SaaS primary store: `jsonb` for flexible attributes with GIN indexes, READ CO…
