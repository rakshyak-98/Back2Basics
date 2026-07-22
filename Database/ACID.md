[[WAL (Write-Ahead Log)]] [[MVCC]] [[mysql transaction]] [[postgres essential]] [[OLTP]] [[connection pooling]]

# ACID

> Transaction guarantees: all-or-nothing writes, valid states, predictable concurrency, survive crashes — **Designing Data-Intensive Applications** (Kleppmann, Ch. 7).

## Mental model

ACID is four independent knobs — databases implement each differently:

| Property | Question it answers | Typical mechanism |
|----------|---------------------|-------------------|
| **Atomicity** | Crash mid-transaction — half applied? | Undo log + rollback; WAL replay |
| **Consistency** | Invalid states possible? | Constraints, FKs, triggers, app invariants |
| **Isolation** | Concurrent txs see each other's partial work? | Locks, [[MVCC]], isolation levels |
| **Durability** | Committed survives power loss? | [[WAL (Write-Ahead Log)]] + fsync |

**Consistency is not magic** — the DB enforces *declared* rules (NOT NULL, CHECK). Business rules ("balance ≥ 0") still need app code or triggers.

**Isolation is where apps break** — ORMs hide transactions; default levels differ; retries aren't automatic.

## Isolation levels & anomalies

SQL standard levels (weakest → strongest):

| Level | Dirty read | Non-repeatable read | Phantom read |
|-------|------------|---------------------|--------------|
| READ UNCOMMITTED | ✓ possible | ✓ | ✓ |
| READ COMMITTED | ✗ | ✓ possible | ✓ |
| REPEATABLE READ | ✗ | ✗ | ✓ possible* |
| SERIALIZABLE | ✗ | ✗ | ✗ |

\*Postgres REPEATABLE READ also blocks phantoms (SSI). MySQL InnoDB REPEATABLE READ uses next-key locks — phantoms mostly blocked.

### Anomaly definitions (what on-call actually sees)

- **Dirty read** — read uncommitted data from another tx; rolled-back rows looked real.
- **Non-repeatable read** — same `SELECT` twice in one tx returns different rows (other tx committed an update).
- **Phantom read** — same range query twice returns different row *count* (inserts/deletes committed by others).
- **Lost update** — two txs read same value, both write; one overwrite silently lost (not always classified as "anomaly" but most common app bug).
- **Write skew** — two txs read disjoint rows, write constraints that together violate an invariant (classic: on-call calendar — two people both think they're sole on-call).

## Engine defaults (know before you deploy)

| Engine | Default isolation | Notes |
|--------|-------------------|-------|
| **PostgreSQL** | READ COMMITTED | Each statement gets fresh snapshot |
| **MySQL InnoDB** | REPEATABLE READ | Consistent reads via undo; gap locks on indexes |
| **SQL Server** | READ COMMITTED | Row versioning optional (RCSI) |
| **SQLite** | SERIALIZABLE | Single-writer; still see `SQLITE_BUSY` |

```sql
-- Postgres: per-session
SHOW transaction_isolation;
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;

-- MySQL
SELECT @@transaction_isolation;
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
```

## Standard config / patterns

### Postgres — when READ COMMITTED isn't enough

```sql
BEGIN;
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
-- ... read + write ...
COMMIT;  -- may fail: ERROR: could not serialize access
```

**App must retry** on `40001` serialization failure — framework rarely does this for you.

### Prevent lost updates (pick one)

```sql
-- 1. Pessimistic lock
SELECT balance FROM accounts WHERE id = 1 FOR UPDATE;

-- 2. Optimistic — compare version
UPDATE accounts SET balance = 900, version = version + 1
WHERE id = 1 AND version = 5;  -- 0 rows = retry

-- 3. Atomic single statement
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
```

### Idempotent retries

Network timeout ≠ rollback. Client retries `COMMIT` or POST — use **idempotency keys** + unique constraints so duplicate commits don't double-charge.

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Random 40001 / deadlock | `pg_stat_database` deadlocks; MySQL `SHOW ENGINE INNODB STATUS` | Shorten txs; consistent lock order; retry with backoff |
| "It worked once, then duplicate" | Missing idempotency; autocommit off forgotten | Unique constraint on idempotency key; explicit COMMIT |
| Long-running open tx bloat | PG: `pg_stat_activity` + `xact_start`; MySQL: `information_schema.innodb_trx` | Kill idle in transaction; fix connection pool leak |
| Phantom counts in reports | RR not enough on PG without SERIALIZABLE | Raise isolation or `SELECT … FOR UPDATE` on range |
| Balance wrong after concurrent updates | Lost update — no locking | `FOR UPDATE` or atomic `UPDATE … SET x = x + 1` |
| Migration "half applied" | DDL autocommit; multi-step without tx wrapper | One migration tx where engine allows; expand-contract pattern |

## Gotchas

> [!WARNING]
> **Autocommit + read-modify-write** — three separate statements = three transactions on READ COMMITTED. Classic inventory oversell.

> [!WARNING]
> **Connection poolers (PgBouncer transaction mode)** — prepared statements and session-level `SET` don't stick; isolation may surprise you.

- **Postgres READ COMMITTED** — each *statement* sees new commits; `SELECT` twice in one tx *can* differ (non-repeatable read by design).
- **MySQL gap locks** — REPEATABLE READ + non-unique index = deadlocks on inserts you'd expect to be unrelated.
- **`READ UNCOMMITTED` on InnoDB** — effectively READ COMMITTED (MVCC); don't rely on dirty reads existing.
- **Durability ≠ backup** — ACID survives crash; not datacenter fire. Test restore.
- **Cross-service "transactions"** — saga/outbox pattern; 2PC is rare for a reason.

## When NOT to use

- **Cross-DB atomicity** — no single ACID tx spans Postgres + Redis + S3. Use outbox/saga.
- **SERIALIZABLE everywhere** — throughput cost + retry storms; use for narrow critical paths.
- **Assuming ORM `@Transactional` fixes isolation** — it opens a tx; level is still DB default unless you SET it.

## Related

[[WAL (Write-Ahead Log)]] [[MVCC]] [[mysql transaction]] [[mysql lock]] [[OCC]] [[BASE]] [[OLTP]] [[connection pooling]]
