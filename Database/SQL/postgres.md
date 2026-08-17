[[Database]] [[SQL]] [[ACID]] [[GIN]] [[psql essential]] [[postgres Error]] [[MVCC]] [[WAL (Write-Ahead Log)]] [[SQL Configurations]] [[ACL (postgreSQL)]]

# postgres

> PostgreSQL — open-source object-relational database with strong [[ACID]] defaults, extensible types, and [[MVCC]] concurrency so readers do not block writers.





## Interview Relevance
Interviewers probe MVCC (visibility, vacuum), isolation defaults, indexing (`jsonb`, partial, [[GIN]]), and ops (autovacuum, WAL, dumps). Signal: you know READ COMMITTED vs SERIALIZABLE and when to use `pg_dump` vs physical backups.

## Sources
- [PostgreSQL Documentation](https://www.postgresql.org/docs/current/) — deep-dive
- [PostgreSQL Global Development Group — About PostgreSQL](https://www.postgresql.org/about/) — overview
- [PostgreSQL Documentation — Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html) — deep-dive
- [PostgreSQL Documentation — WAL Internals](https://www.postgresql.org/docs/current/wal-intro.html) — overview
- Kleppmann, *Designing Data-Intensive Applications*, Ch. 3–7 — overview

## Core Definition
PostgreSQL is a process-per-connection object-relational engine: a postmaster forks backends that plan and execute SQL against shared buffers and WAL, with background workers for checkpoints and autovacuum.

## Key Concepts
- **Postmaster + backends:** one OS process per connection; shared memory for buffers and locks.
- **MVCC:** versions of rows; readers see a snapshot; writers do not lock out readers for normal SELECTs.
- **Autovacuum:** reclaims dead tuples and freezes XIDs — required for long-lived [[MVCC]] health.
- **Extensible types:** `jsonb`, arrays, ranges, UUID, custom types and operators.
- **Index variety:** B-tree, partial, expression, [[GIN]] / GiST / BRIN.
- **Isolation:** default READ COMMITTED; `SERIALIZABLE` uses Serializable Snapshot Isolation.

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

Distinctive strengths:

- Partial and expression indexes; [[GIN]] for `jsonb` / full-text
- Declarative partitioning, table inheritance (legacy patterns), foreign data wrappers
- Logical decoding / replication slots for change-data-capture

CLI and ops entry points:

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

## Real-World Applications
SaaS primary store: `jsonb` for flexible attributes with GIN indexes, READ COMMITTED for most APIs, SERIALIZABLE or careful locking for inventory, and continuous archiving of WAL for point-in-time recovery.

## Pros/Cons or Trade-offs
- **Pro:** Strong defaults, rich SQL, extensibility without leaving the engine.
- **Con:** Process-per-connection needs pooling at scale; vacuum debt causes bloat and wraparound risk.
- **Trade-off:** Strict isolation / sync commit vs throughput under write-heavy load.

## Comparison
vs [[mysql]]: PostgreSQL leans MVCC snapshots and richer types; InnoDB defaults to REPEATABLE READ with next-key locking. vs [[OLAP]] warehouses: PostgreSQL is primarily [[OLTP]]; columnar warehouses win large scans. vs [[write-ahead logging]]: WAL protocol is shared conceptually; PostgreSQL’s LSN and `pg_wal` are the concrete artifact.

## Mistakes to Avoid
- Turning off autovacuum “for performance.”
- Skipping connection pooling and opening thousands of backends.
- Treating `jsonb` as a substitute for modeling hot query paths without indexes.
- Ignoring `serialization_failure` retries under SERIALIZABLE.
