[[Database]] [[mysql connection]] [[mysql pool connection]] [[OLTP]]

# connection pooling

> Reuse a bounded set of open database sessions across many application threads so burst traffic does not exhaust `max_connections` or pay TCP+TLS handshake per request.

## Why pools exist

Each database connection consumes memory on the server (buffers, session state) and file descriptors on the client. Creating a connection involves TCP (often TLS), authentication, and sometimes prepared statement caches.

```txt
1000 HTTP workers ──► pool (20 connections) ──► PostgreSQL max_connections=100
```

Without a pool, **queueing at the database** looks like random application timeouts.

## Pool sizing heuristics

| Signal | Likely cause |
|--------|--------------|
| `pool exhausted` / long wait | Pool too small or slow queries hold connections |
| High DB CPU, low app concurrency | Pool too large — too much lock contention |
| Idle connections near `max_connections` | Leak or missing `close()` / context managers |

Rule of thumb: start with `(CPU cores * 2) + spindle_count` for OLTP on PostgreSQL (adjust per workload); measure wait time and query latency.

## Configuration patterns

- Set **connection lifetime** and **idle timeout** to shed stale connections after deploys or firewall NAT timeouts
- Use **statement timeouts** at session level to prevent one bad query from pinning the pool
- Validate **health** on checkout (simple `SELECT 1`) after network blips

## Sources

- PostgreSQL Documentation — [Connection Handling](https://www.postgresql.org/docs/current/runtime-config-connection.html)
- HikariCP wiki — [About Pool Sizing](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing)
- Kleppmann, *DDIA*, Ch. 7 (handling many clients)
