[[Database]] [[mysql connection]] [[mysql pool connection]] [[OLTP]] [[mysql]] [[Design pattern/Object Pool]]

# connection pooling

> A connection pool maintains a bounded set of open database sessions that application threads borrow and return — avoiding per-request TCP+TLS handshakes and protecting the database from connection exhaustion.

---

## Why It Matters

Opening a database connection is expensive: TCP (often TLS), authentication, session initialization, and server-side memory allocation. Under burst traffic, creating one connection per HTTP request can exhaust `max_connections` on PostgreSQL or MySQL long before application CPU saturates. A pool amortizes connect cost and caps concurrent sessions. Mis-sizing the pool is equally dangerous — too small causes queueing timeouts; too large amplifies lock contention on the database without improving throughput.

---

## Sources

- [HikariCP — About Pool Sizing](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing) — Brett Wooldridge's sizing formula and explanation of why more connections ≠ more throughput on OLTP workloads.
- [PostgreSQL Documentation — Connection Settings](https://www.postgresql.org/docs/current/runtime-config-connection.html) — Official `max_connections` and memory implications per backend process.
- [Wikipedia — Connection pool](https://en.wikipedia.org/wiki/Connection_pool) — General pattern: acquire, use, release, with timeout and validation semantics.
- Kleppmann, *Designing Data-Intensive Applications*, Ch. 7 — Why connection setup dominates latency and how backpressure propagates through tiers.

---

## Key Concepts

```txt
App thread 1 ──┐
App thread 2 ──┼──► Pool (max 20) ──► Database (max_connections = 100)
App thread N ──┘         │
                    acquire / release
                    timeout if exhausted
```

| Concept | Detail |
|---------|--------|
| **Bounded pool** | `maxSize` caps concurrent DB sessions — protects server `max_connections`. |
| **Acquire timeout** | Fail fast when pool is exhausted instead of hanging forever. |
| **Idle eviction** | Drop connections idle longer than threshold — frees server memory. |
| **Max lifetime** | Recycle connections after N minutes — survives server-side idle kills and DNS changes. |
| **Validation** | `SELECT 1` on borrow after network blips — detects half-open TCP sessions. |
| **Hold time** | Slow queries pin pool slots — pool size cannot fix missing indexes. |
| **Thread safety** | Concurrent borrow/return without double-free or use-after-return. |

### Pool sizing rule of thumb (OLTP, PostgreSQL)

Start with: `connections = (CPU cores × 2) + effective_spindle_count` (HikariCP wiki). Measure, then tune. For 50 app pods, **each pod's pool must be sized so total connections stay below database `max_connections` minus admin overhead**.

---

## Technical Details

### Request flow

```txt
Request → pool.acquire(timeout) → execute query → pool.release(conn)
              ↓ timeout
         PoolExhaustedException → 503 / circuit breaker
```

### API sketch (application-level pool)

```java
// Pseudocode — same semantics in HikariCP, pg, mysql2, sqlalchemy
Connection conn = pool.acquire(5, TimeUnit.SECONDS);
try {
    conn.execute("SELECT …");
} finally {
    pool.release(conn);   // always in finally / try-with-resources
}
```

### Configuration patterns

| Setting | Purpose |
|---------|---------|
| `maximumPoolSize` | Hard cap on open connections |
| `connectionTimeout` | Max wait when pool is full |
| `idleTimeout` | Evict idle connections |
| `maxLifetime` | Force recycle (e.g. 30 min) |
| `connectionTestQuery` | Validation query on checkout |

### External poolers

| Tool | When |
|------|------|
| **PgBouncer** | Many app instances/languages sharing one Postgres — transaction or statement pooling |
| **RDS Proxy** | AWS-managed connection multiplexing for Lambda and burst workloads |
| **ProxySQL** | MySQL query routing, read/write split, connection pooling |

Move pooling out of the app when you have hundreds of short-lived processes (serverless) or heterogeneous clients.

### Failure signals

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `pool exhausted` / long acquire wait | Pool too small or slow queries hold slots | Tune size; fix slow queries |
| High DB CPU, low app concurrency | Pool too large — lock contention | Reduce pool size |
| `Connection reset` / stale conn errors | Network blip; server killed idle session | Enable validation; lower max lifetime |
| Connections grow to `max_connections` | Leak — missing `close()` / context manager | Audit try/finally; leak detection |
| Works in dev, fails in prod | 1 pod vs 50 pods × pool size | Size per instance; use external pooler |

---

## Mistakes to Avoid

- Setting pool size equal to HTTP worker count without accounting for pod count.
- Growing the pool to "fix" timeouts caused by slow queries — fix the query or add read replicas.
- Holding a connection across slow external HTTP calls — return to pool before calling third parties.
- Forgetting statement timeouts — one bad query pins every slot until killed.
- Unlimited pool growth — masks leaks until the database itself crashes.

---

## Pros/Cons or Trade-offs

| Pro | Con |
|-----|-----|
| Stable latency under burst | Mis-sized pools cause outages that look like "DB is down" |
| Predictable load on the database | Session state (`SET`, temp tables) can leak across checkouts if not reset |
| Cheaper than one connection per request | Adds operational tuning surface |

---

## Comparison

| Approach | Trade-off |
|----------|-----------|
| New connection per request | Simple code; dies under concurrency |
| Application pool (HikariCP, pg pool) | Per-process cap; multiply by replica count |
| External pooler (PgBouncer) | Centralized sizing; adds network hop |
| vs [[mysql connection]] | A connection is one TCP session; a pool manages many |

---

## Use cases

- Spring Boot + HikariCP behind a load balancer: size pool so `pods × maxPoolSize < Postgres max_connections - 10`.
- Node.js `pg` pool with `max: 20` per process — monitor `pool.waitingCount` in metrics.
- Serverless Lambda → RDS Proxy to avoid connection storms on cold starts.
