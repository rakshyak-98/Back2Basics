[[Database/connection pooling]] [[Design pattern/Object Pool]] [[LLD/Questions/Logger]]

# Connection Pool (LLD)

> Reuse a bounded set of open database connections — acquire, use, release — so request threads do not pay connect cost or exhaust the database.





## Interview Relevance
Classic LLD: thread safety, max size, timeouts, validation (borrow/return), and failure modes when the pool is exhausted.

## Sources
- [HikariCP — About](https://github.com/brettwooldridge/HikariCP) — deep-dive
- [Wikipedia — Connection pool](https://en.wikipedia.org/wiki/Connection_pool) — overview

## Key Concepts
- **Bounded pool:** `maxSize` protects the database.
- **Acquire timeout:** fail fast vs hang forever when exhausted.
- **Idle eviction / max lifetime:** defend against server-side connection kills.
- **Thread safety:** concurrent borrow/return without double-free.
- **Validation:** lightweight ping on borrow if connections go stale.

## Technical Details
```txt
Request → borrow conn → query → return conn → pool
             ↓ empty
        wait up to timeout → error
```

API sketch: `acquire()`, `release(conn)`, `close()`, metrics for active/idle/wait.

| Failure | Design response |
|---------|-----------------|
| Pool exhausted | Timeout + backpressure; size from DB `max_connections` |
| Stale conn | Validate or recreate |
| Leak | Try/finally or use-with-resource; leak detection |

## Real-World Applications
Web APIs with HikariCP/pgbouncer: app pool sized below database capacity accounting for replicas and admin slots.

**Example:** 50 app pods × 20 connections → far above Postgres `max_connections` — shrink pools or add a pooler.

## Pros/Cons or Trade-offs
- **Pro:** Latency and connection stability under load.
- **Con:** Mis-sizing causes outages that look like “DB is down.”

## Comparison
- vs opening a connection per request: simpler, dies under concurrency.
- vs external pooler (PgBouncer): move pooling out of the app for many languages/instances.

## Mistakes to Avoid
- Holding a connection across slow external HTTP calls.
- Unlimited pool growth.
- Swallowing acquire timeouts without metrics/alerts.
