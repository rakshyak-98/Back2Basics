[[ACID]] [[Database mistakes]] [[OLTP]] [[Vector database]]

# BASE

> One-line: distributed-systems tradeoff label — **B**asically **A**vailable, **S**oft state, **E**ventual consistency — opposite emphasis from [[ACID]]; know what you're giving up.

## Mental model

ACID optimizes **single-node transactional correctness**. BASE describes many **distributed / NoSQL** designs that prefer availability under partition ([[CAP theorem]] intuition): respond even when stale; accept that replicas converge **eventually**.

```
ACID (typical RDBMS)          BASE (many Dynamo-style stores)
───────────────               ───────────────────────────────
Strong consistency            High availability first
Sync replication wait         Async replication common
Rollback on failure           Compensating actions / repair
Single source of truth now    Multiple versions → merge later
```

| Letter | Meaning | Operational read |
|--------|---------|------------------|
| **B**asically Available | System responds (maybe degraded/stale) | Read replica lag OK for some queries |
| **S**oft state | State may change without input (replication, TTL) | Caches expire; background sync |
| **E**ventual consistency | Replicas converge if no new writes | "Read your writes" not guaranteed without sticky routing |

## Standard config / commands

### Patterns that imply BASE

```txt
Cassandra / DynamoDB  → tunable consistency (often eventual default)
Redis primary-replica → async repl → stale reads on replica
CQRS read models      → lag between write and read side
CDN edge cache        → TTL-based staleness
```

### Mitigate eventual consistency in apps

```javascript
// After write, read from primary or version key
await db.put({ id, version: Date.now(), ... });
const row = await db.get(id, { consistentRead: true }); // Dynamo-style

// Idempotency keys for retries
headers: { 'Idempotency-Key': uuid }
```

### Monitor replica lag

```sql
-- Postgres
SELECT EXTRACT(EPOCH FROM (now() - pg_last_xact_replay_timestamp()));

-- MySQL
SHOW REPLICA STATUS\G  -- Seconds_Behind_Source
```

### When you need stronger guarantees

```txt
Use transactional store (Postgres) for money/inventory
Saga / outbox pattern for cross-service consistency
Leader election + sync quorum for critical metadata
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| User sees stale data after update | Read from replica | Route session to primary; sticky sessions |
| Duplicate charges on retry | No idempotency | Idempotency keys; dedupe table |
| Lost update across regions | Last-write-wins | Version vectors; CRDT or conflict UI |
| "Ghost" records after delete | Tombstone replication delay | Read-your-writes; higher consistency level |
| Inventory oversell | Eventual stock count | Reserve in ACID store; async analytics separate |

## Gotchas

> [!WARNING]
> **BASE is not "no consistency"** — it's explicit about **when** consistency holds; document SLAs.

> [!WARNING]
> **Caching without invalidation** — classic eventual consistency bug in "monolith with Redis".

> [!WARNING]
> **Cross-DC async repl** — RPO > 0; plan for failover data loss window.

## When NOT to use

- **Ledger, inventory, booking without compensations** — use ACID RDBMS or strongly consistent store.
- **Label as BASE to excuse missing design** — still need idempotency, conflict policy, and monitoring.

## Related

[[ACID]] [[OLTP]] [[Database mistakes]] [[Data access patterns]] [[stateless offset handling]]
