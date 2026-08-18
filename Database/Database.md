[[ACID]] [[WAL (Write-Ahead Log)]] [[OLTP]] [[OLAP]] [[Database design]] [[connection pooling]] [[MVCC]]

# Database

> Durable shared storage with a query language, transactions, and rules — survive crash, serve many clients, keep declared constraints true.

## Mental model

**Say it in one breath:** A database turns “bytes on disk + concurrent clients” into **atomic commits**, **durable history**, and **queryable structure** so the application does not reinvent crash recovery and locking.

```txt
App(s) ──► connections / pool ──► query planner ──► buffer pool
                                      │
                                      ├── indexes / heap
                                      ├── WAL / redo  ([[WAL (Write-Ahead Log)]])
                                      └── transactions ([[ACID]], [[MVCC]])
```

Without atomicity + durability, a crash mid-update can leave half-written rows. The engine’s job is: **all-or-nothing commit**, then **replay safely** after power loss.

| Workload | Shape | Typical home |

| [[OLTP]] | Short point lookups + small writes | Postgres / MySQL primary |
| --- | --- | --- |
| [[OLAP]] | Scans, aggregates | Warehouse / column store |
| Cache | Ephemeral, optional loss | Redis (often no WAL by default) |

## Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **Atomicity** | Commit all changes or none | “No half-paid order after a crash.” |
| --- | --- | --- |
| **Durability** | Committed data survives power loss | “WAL + fsync before we ack the client.” |
| **Isolation** | Concurrent txs don’t see each other’s mess | “Levels trade anomalies for throughput.” |
| **Schema** | Tables, types, constraints | “Constraints catch bad writes early.” |
| **Index** | Side structure for fast lookup | “Speeds reads; slows writes; must match queries.” |
| **Connection pool** | Reuse DB sessions | “App threads ≠ DB connections.” |

## Standard config / patterns

### Production baseline (any engine)

```txt
1. fsync / sync_binlog / synchronous_commit ON for money paths
2. Connection pool in front of max_connections
3. Backups + tested restore (WAL ≠ DR)
4. Migrations versioned ([[database migration]])
5. Monitoring: connections, replication lag, deadlocks, disk
```

### Safe write shape

```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1 AND balance >= 100;
INSERT INTO ledger (...);
COMMIT;   -- or rollback; never leave multi-step money outside a tx
```

| Knob | Why it matters |

| `max_connections` | Exhaustion looks like random timeouts |
| --- | --- |
| Isolation default | PG READ COMMITTED vs MySQL RR — see [[ACID]] |
| Autovacuum / purge | [[MVCC]] bloat if neglected |
| Read replica lag | Stale reads if you route blindly |

## Time, expiry, and clocks

Expiry and “end of day” logic breaks when clocks disagree.

| Risk | What happens | Fix |

| **Server clock drift** | One node expires a row; another still serves it | NTP/chrony; prefer DB `now()` / `clock_timestamp()` for authoritative checks |
| --- | --- | --- |
| **TZ mismatch** | App `new Date()` in EST vs UTC columns | Store **UTC**; convert at the edge; never mix |
| **Client clock** | User changes laptop time to extend trial | Server-side validation only for auth/billing |

```sql
-- Prefer DB time for expiry checks
SELECT * FROM sessions
WHERE token = $1 AND expires_at > now();
```

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Data missing after crash | fsync settings; disk full during WAL | Restore; never leave `fsync=off` in prod |
| Timeouts under load | Pool wait; `max_connections`; slow queries | [[connection pooling]]; indexes; kill long txs |
| Wrong expiry / “premature logout” | TZ; client vs server time | UTC in DB; server-side checks |
| Duplicate charges | Missing idempotency / unique key | Idempotency key + constraint ([[ACID]]) |
| Replica “lies” | Lag metrics | Route strong reads to primary |
| Schema drift | Manual prod DDL | [[database migration]] only |

## Gotchas

> [!WARNING]
> **Autocommit read-modify-write** — three statements = three transactions on READ COMMITTED. Classic inventory oversell ([[ACID]]).

> [!WARNING]
> **Backup untested** — durability is not disaster recovery. Practice restore.

- **ORM `@Transactional`** opens a transaction; isolation is still the engine default until you set it.
- **Cross-DB “transactions”** — Postgres + Redis + S3 need outbox/saga, not one COMMIT.
- **`SELECT *` in hot paths** — wider rows, less index-only potential.

## When NOT to use

- **Ephemeral session cache** — Redis/memcached; accept loss by design ([[BASE]] tradeoffs).
- **Blob CDN workloads** — object storage + CDN, not row store.
- **Heavy analytics on the primary** — splits [[OLTP]] latency; use replica/warehouse ([[OLAP]]).

## Related

[[ACID]] [[WAL (Write-Ahead Log)]] [[MVCC]] [[OCC]] [[OLTP]] [[OLAP]] [[BASE]] [[Database design]] [[database migration]] [[connection pooling]] [[Data access patterns]] [[Database mistakes]]
