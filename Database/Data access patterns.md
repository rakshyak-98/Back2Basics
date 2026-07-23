[[Database design]] [[OLTP]] [[OLAP]] [[connection pooling]] [[covering index]] [[BASE]]

# Data access patterns

> How the app reads/writes drives schema, indexes, caching, and consistency — staff design-review lens — **Designing Data-Intensive Applications** (Kleppmann).

## Mental model

Schema follows **access paths**, not ER diagrams drawn once. Ask every feature:

1. **Who writes?** frequency, burstiness, idempotency
2. **Who reads?** latency SLO, staleness tolerance
3. **Key?** point lookup vs scan vs graph walk
4. **Shape?** row, document, time-series, blob

```
         ┌─────────────┐
Write ──►│  Primary    │──► CDC/outbox ──► search index / warehouse
         │  (OLTP)     │
         └──────┬──────┘
                │ read paths
    ┌───────────┼───────────┐
    ▼           ▼           ▼
  Cache      Replica    Materialized view
 (eventual)  (lag OK)   (pre-aggregated)
```

**Pattern picks consistency boundary** — not the ORM.

## Core patterns (catalog)

| Pattern | Read | Write | Schema hint |
|---------|------|-------|-------------|
| **Key-value / ID lookup** | `GET by PK` | Upsert row | Surrogate PK; avoid hot UUIDv4 |
| **1:N owned children** | List by FK | Insert child + parent tx | Index `(parent_id, sort_key)` |
| **Pagination (feed)** | Keyset / cursor | Append-only | `(user_id, created_at, id)` composite; no OFFSET deep pages |
| **Counter / rate** | Approx OK? | High increment | Sharded counters, Redis HINCRBY, or async rollup |
| **Inventory / balance** | Strong read | Atomic decrement | `UPDATE … WHERE qty >= N`; [[ACID]] + row lock |
| **Idempotent command** | — | Retry-safe | Unique `(idempotency_key)`; store outcome |
| **Outbox** | — | DB tx + event row | Same tx as business write; poller publishes |
| **CQRS-lite** | Replica/warehouse | Primary only | Don't run `GROUP BY` on checkout DB |
| **Search** | Full text | Async index | Postgres GIN / OpenSearch; not `LIKE '%foo%'` |
| **Blob metadata** | Row in DB | Object in S3 | Store URI + checksum; not BYTEA at scale |

## Read patterns → engineering choices

### Read-your-writes

User saves profile → refresh must show new data.

- Route to **primary** or sticky session for N seconds after write.
- Don't read replica immediately after POST unless app handles lag.

### Stale reads OK

Dashboard, recommendations, "views: ~1.2k".

- **Replica + cache** with TTL; label UI "may be delayed."
- [[BASE]] consciously.

### Thundering herd

Popular key expires together.

- Jitter TTL; singleflight / request coalescing; probabilistic early refresh.

### N+1 vs batch

```sql
-- Bad: 1 + N queries from ORM lazy load
-- Good:
SELECT o.*, li.* FROM orders o JOIN line_items li ON li.order_id = o.id
WHERE o.user_id = $1;
```

## Write patterns → engineering choices

### Single-row OLTP

Default path: short tx, indexed WHERE, pool connection.

### Multi-row invariant

Transfer money, swap seats — one tx, consistent lock order, or SERIALIZABLE + retry ([[ACID]]).

### High fan-out write

Activity feed insert for 10k followers — don't synchronous INSERT 10k rows. **Fan-out on read**, queue workers, or hybrid (celebrity exception).

### Soft delete vs hard delete

- Soft: `deleted_at` — every query filters; index `(active, …)`.
- Hard + audit table — cleaner reads, compliance trail separate.

## Caching decision table

| Data | Cache? | Invalidation |
|------|--------|--------------|
| Session / JWT blocklist | Redis | TTL or explicit DEL |
| Product catalog | CDN/Redis | Pub/sub on admin update |
| User permissions | Local + Redis | Version column bump |
| Inventory | **Careful** | Write-through or skip cache on stock |

> [!WARNING]
> **Cache-aside without TTL on miss stampede** — DB dies, cache empty, every request hits DB.

## Standard checklist (design review)

```
□ Every API endpoint: list queries (count, p99 target)
□ Hot path EXPLAIN / EXPLAIN ANALYZE documented
□ Idempotency for external side effects
□ Replica lag acceptable? Which routes pinned to primary?
□ Migration: expand-contract (add col → dual write → backfill → switch → drop)
□ Connection pool size justified (not = thread count)
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| DB CPU 100%, app idle | ORM SQL log; `pg_stat_statements` | Kill N+1; add index; cache read |
| Inconsistent UI after save | Read replica routing | Primary for session writes |
| Duplicate charges | Missing idempotency key | Unique constraint + return stored result |
| Feed pagination slow page 500 | `OFFSET` | Keyset: `WHERE (created_at,id) < ($c,$id)` |
| Cache stale forever | No invalidation on write | Delete key on update; shorter TTL |
| Warehouse wrong vs app | CDC lag / dual write drift | Reconcile job; fix outbox |

## Gotchas

- **Design schema from mock UI once** — second screen needs join you didn't index.
- **JSON column for everything** — loses constraint + index precision; fine for optional metadata, not core filters.
- **Cross-aggregate in request path** — `COUNT(*)` on 100M rows per page load belongs offline.
- **Global secondary index on sharded DB** — scatter-gather; prefer local indexes + routing key.

## When NOT to use

- **One pattern everywhere** — feed ≠ ledger ≠ analytics; polyglot persistence is normal.
- **Cache before measuring** — fix query/index first; cache hides debt until incident.

## Related

[[Database design]] [[OLTP]] [[OLAP]] [[connection pooling]] [[covering index]] [[migration]] [[mysql index]] [[MVCC]]
