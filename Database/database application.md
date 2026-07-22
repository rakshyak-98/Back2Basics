[[Database design]] [[OLTP]] [[connection pooling]] [[Data access patterns]] [[migration]]

# Database application (app ↔ DB layer)

> **Programs that issue queries and enforce data rules** — ORM, query builder, repository layer, transactions, and connection lifecycle. The "application" in "database application" is your service code, not the RDBMS binary.

## Mental model

A database application = **schema** + **access layer** (SQL/ORM) + **transaction boundaries** + **pool**. Users hit API; API opens connection (from pool), runs queries in a transaction, commits/rolls back, returns DTOs. Leaks and N+1 queries live here, not in "the database being slow."

```
HTTP handler ──► service/repo ──► pool.getConnection()
                        │                │
                        └── business rules └── SQL / ORM ──► [[OLTP]] store
```

Separate **read models** ([[OLAP]], replicas) from **write path** when analytics would crush OLTP ([[Data access patterns]]).

## Standard config / commands

### Layering (typical)

| Layer | Responsibility |
|-------|----------------|
| Handler/controller | Auth, HTTP, validation |
| Service | Use cases, transaction scope |
| Repository/DAO | Queries only; no HTTP types |
| Migration | Schema version ([[migration]]) |

### Transaction boundary (Node + Postgres)

```javascript
await db.transaction(async (trx) => {
  await trx('accounts').where({ id: fromId }).decrement('balance', amount);
  await trx('accounts').where({ id: toId }).increment('balance', amount);
  await trx('ledger').insert({ fromId, toId, amount });
});
// rollback on throw — [[ACID]]
```

### Connection pool (production defaults)

```javascript
// pg — don't create pool per request
const pool = new Pool({
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 5000,
});
```

Align `max` with DB `max_connections / app_instances` ([[connection pooling]]).

### ORM hygiene

- **Eager load** associations needed in list endpoints — avoid N+1.
- **Pagination**: keyset (`WHERE id > ? ORDER BY id LIMIT`) over `OFFSET` on huge tables.
- **Migrations own schema** — not `sync()` in prod (Sequelize/TypeORM).

### Read vs write routing

```javascript
// pseudo — replica for reports only
const rows = await readPool.query('SELECT ... aggregate ...');
const order = await writePool.query('INSERT INTO orders ... RETURNING *');
```

Replica lag → stale reads; never read-your-writes on replica for UX-critical paths unless tracked.

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Pool timeout waiting connection | Pool size; slow queries holding conn | Increase pool slightly; fix slow SQL; set statement timeout |
| Random 500 after deploy | Migration not run; code expects new column | Run [[migration]] before app rollout |
| Data partial update | Missing transaction wrapper | Wrap multi-step updates in one txn |
| Memory climb | ORM loading unbounded relations | Pagination; select specific columns |
| Deadlocks | Concurrent updates same rows | Consistent lock order; retry with backoff |
| Works in test, fails prod | SQLite vs Postgres semantics | Test against prod engine in CI |

## Gotchas

> [!WARNING]
> **Long-running transaction in request** — holds connections and blocks vacuum/undo — move batch work offline.

> [!WARNING]
> **ORM `save()` in loop** — N round-trips; use batch insert/update.

> [!WARNING]
> **Silent SQL logging in prod** — PII in logs; sample or redact.

> [!WARNING]
> **Global singleton pool in serverless** — each invocation may need Data API or external pooler (RDS Proxy).

## When NOT to use

- **Fat models with HTTP and SQL mixed** — splits testability and encourages circular imports.
- **Database as message queue** — use proper broker; SKIP LOCKED patterns are last resort.
- **Cross-DB joins in app** — integrate at service layer or warehouse.

## Related

[[Database design]] · [[OLTP]] · [[connection pooling]] · [[Data access patterns]] · [[migration]] · [[Database mistakes]]
