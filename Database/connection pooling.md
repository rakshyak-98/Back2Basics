[[Database]] [[mysql connection]] [[mysql pool connection]] [[OLTP]] [[mysql]]

# connection pooling

> Reuse a bounded set of open database sessions across many application threads so burst traffic does not exhaust `max_connections` or pay TCP+TLS handshake per request.





## Interview Relevance
Pooling is a classic ops interview topic: sizing, exhaustion symptoms, statement timeouts, and why “more connections” often makes latency worse. Signal: you size pools from wait time and DB capacity, not from HTTP worker count one-to-one.

## Sources
- [PostgreSQL Documentation — Connection Settings](https://www.postgresql.org/docs/current/runtime-config-connection.html) — overview
- [HikariCP wiki — About Pool Sizing](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing) — deep-dive
- Kleppmann, *Designing Data-Intensive Applications*, Ch. 7 — overview

## Key Concepts
- **Bounded reuse:** many app workers share few DB sessions → protects `max_connections` and handshake cost.
- **Server cost per connection:** memory, buffers, file descriptors → unbounded clients crash the database first.
- **Hold time matters:** slow queries pin pool slots → pool size cannot fix missing indexes.
- **Lifecycle hygiene:** max lifetime, idle timeout, health checks → shed stale sessions after deploys and NAT blips.

## Technical Details
Each database connection consumes memory on the server (buffers, session state) and file descriptors on the client. Creating a connection involves TCP (often TLS), authentication, and sometimes prepared statement caches.

```txt
1000 HTTP workers ──► pool (20 connections) ──► PostgreSQL max_connections=100
```

Without a pool, **queueing at the database** looks like random application timeouts.

| Signal | Likely cause |
|--------|--------------|
| `pool exhausted` / long wait | Pool too small or slow queries hold connections |
| High DB CPU, low app concurrency | Pool too large — too much lock contention |
| Idle connections near `max_connections` | Leak or missing `close()` / context managers |

Rule of thumb: start with `(CPU cores * 2) + spindle_count` for OLTP on PostgreSQL (adjust per workload); measure wait time and query latency.

Configuration patterns:

- Set **connection lifetime** and **idle timeout** to shed stale connections after deploys or firewall NAT timeouts
- Use **statement timeouts** at session level to prevent one bad query from pinning the pool
- Validate **health** on checkout (simple `SELECT 1`) after network blips

## Real-World Applications
Web [[OLTP]] services behind HikariCP, PgBouncer, or [[mysql pool connection]]. Example: 1,000 request workers share a pool of 20; timeouts drop once statement timeout kills a stuck report query holding slots.

## Pros/Cons or Trade-offs
- **Pro:** Stable latency under burst; predictable load on the database; cheaper than one connection per request.
- **Con:** Mis-sized pools hide query problems or amplify lock contention; session state (temp tables, SET) can leak across checkouts if not reset.

## Comparison
vs [[mysql connection]]: a connection is one TCP session; a pool multiplexes many app tasks onto a fixed set of those sessions. vs opening per-request connections: pools trade a small wait queue for far lower handshake and memory cost.

## Mistakes to Avoid
- Setting pool size equal to HTTP worker count — often saturates `max_connections`.
- Growing the pool to “fix” timeouts caused by slow queries.
- Forgetting statement timeouts — one bad query pins every slot.
- Leaking connections (no `close()` / context manager) until the pool and server are exhausted.
