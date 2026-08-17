[[Database/connection pooling]] [[Design pattern/Object Pool]] [[LLD/Questions/Logger]]

# Connection Pool (LLD)

> Reuse a bounded set of open database connections — acquire, use, release — so request threads do not pay connect cost or exhaust the database.

```txt
        Connection Pool (L ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Classic LLD: thread safety, max size, timeouts, validation (borrow/return), a…

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

- API sketch: `acquire()`, `release(conn)`, `close()`, metrics for active/idle/…

| Failure | Design response |
|---------|-----------------|
| Pool exhausted | Timeout + backpressure; size from DB `max_connections` |
| Stale conn | Validate or recreate |
| Leak | Try/finally or use-with-resource; leak detection |

## Mistakes to Avoid
- **Mistake:** Holding a connection across slow external HTTP calls
- **Mistake:** Unlimited pool growth
- **Mistake:** Swallowing acquire timeouts without metrics/alerts

## Pros/Cons or Trade-offs
- **Pro:** Latency and connection stability under load.
- **Con:** Mis-sizing causes outages that look like “DB is down.”

## Comparison
- vs opening a connection per request: simpler, dies under concurrency.
- vs external pooler (PgBouncer): move pooling out of the app for many languages/instances.


### Use cases
- Web APIs with HikariCP/pgbouncer: app pool sized below database capacity acco…

- **Example:** 50 app pods × 20 connections → far above Postgres `max_connectio…
