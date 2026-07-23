[[Database]] [[Data access patterns]] [[OLTP]] [[OLAP]] [[Vector database]]

# Heterogeneous Database Systems

> One-line: one application orchestrates **multiple DB engines** (SQL + document + cache + search) — polyglot persistence; integration and consistency are the hard parts.

## Mental model

Instead of one RDBMS for everything, teams pick **best-fit stores per access pattern**:

```
                    ┌─────────────┐
               ┌───►│ Postgres    │  transactions, reporting core
App / API ─────┼───►│ MongoDB     │  flexible documents
               ├───►│ Redis       │  cache, locks, pub/sub
               ├───►│ Elasticsearch│ full-text search
               └───►│ S3 + Athena │  cold analytics
```

**Heterogeneous** = different data models, query languages, consistency models ([[ACID]] vs [[BASE]]), ops tooling. Cohesion comes from **application layer** (API, events, ETL) — not a single SQL dialect.

## Standard config / commands

### Access-pattern routing (design doc table)

| Data | Store | Why |
|------|-------|-----|
| Orders, payments | Postgres | ACID, constraints |
| Product catalog JSON | MongoDB | schema flexibility |
| Session / rate limit | Redis | TTL, speed |
| Search | OpenSearch | inverted index |
| Audit archive | S3 + Parquet | cost |

### Sync patterns

```txt
Transactional outbox (Postgres) → Debezium/Kafka → consumers update search index
Dual-write (avoid) → race conditions; pick single writer + async projection
CDC (Change Data Capture) → keep read models eventually consistent
Saga / choreographed steps → cross-service business transactions
```

### Example outbox table

```sql
CREATE TABLE outbox (
  id BIGSERIAL PRIMARY KEY,
  aggregate_type TEXT NOT NULL,
  aggregate_id TEXT NOT NULL,
  payload JSONB NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now(),
  published_at TIMESTAMPTZ
);
```

### Operational checklist per engine

```txt
□ Backup/restore tested per store
□ Connection pools sized per engine ([[connection pooling]])
□ Observability: lag, hit rate, slow queries per backend
□ Runbooks for partial outage (degrade search, not checkout)
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Search out of sync with DB | Indexer lag / failed consumer | Replay outbox/CDC; rebuild index |
| Double charge | Dual-write without txn | Single source of truth + idempotent consumers |
| Cache serves stale forever | No TTL/invalidation | Event-driven eviction; short TTL + version keys |
| Wrong DB queried | Router misconfig | Feature flags; explicit repository boundaries |
| Partial backup restore | Only restored Postgres | Document cross-store restore order |
| Latency spikes | N+1 across stores | Batch fetch; materialized views |

## Gotchas

> [!WARNING]
> **Distributed transactions (2PC) across Mongo + Postgres** — fragile; prefer sagas/outbox.

> [!WARNING]
> **Joining across DBs in app code** — N+1 and consistency bugs; precompute read models.

> [!WARNING]
> **Operational blast radius** — more engines = more certs, patches, on-call surfaces.

## When NOT to use

- **Early startup / small team** — one well-modeled Postgres often beats five databases.
- **"We might need graph later"** — YAGNI until access pattern proves it.

## Related

[[Data access patterns]] [[Database mistakes]] [[OLTP]] [[OLAP]] [[Microservice]] [[connection pooling]]
