[[mysql connection]] [[connection pooling]] [[mysql]] [[variables]]

# mysql pool connection

> Application-side pool of reusable MySQL sessions — HikariCP, mysql2 pool, SQLAlchemy `QueuePool` — to cap server connections and amortize handshake cost.

## Interview Relevance
Capacity planning: `pool_max × app_instances` versus `max_connections`. Stale connections and pool wait timeouts are common production war stories.

## Sources
- [Connector/J connection notes](https://dev.mysql.com/doc/connector-j/en/connector-j-usagenotes-connect-drivermanager.html) — overview
- [HikariCP configuration](https://github.com/brettwooldridge/HikariCP#configuration-knobs) — deep-dive
- [[connection pooling]] — overview

## Key Concepts
- **Borrow / return:** Request takes a live session; must return it promptly.
- **Sizing:** Leave headroom for migrations, admin, and other services.
- **Validation:** Test-on-checkout or max lifetime to shed dead sockets.
- **Leak detection:** Pools that never return connections look like “MySQL is slow.”

## Technical Details
```properties
maximumPoolSize=20
connectionTimeout=30000
idleTimeout=600000
maxLifetime=1800000
```

| Symptom | Check |
|---------|-------|
| `Too many connections` | Pool max × instances vs `max_connections` |
| Stale connection errors | Test query on checkout; reduce `maxLifetime` |
| Pool wait timeouts | Slow queries holding connections |

## Real-World Applications
Each Kubernetes pod runs HikariCP at 10–20; horizontal scale requires lowering per-pod size or raising server limits with memory math.

## Pros/Cons or Trade-offs
- **Pro:** Stable latency, controlled concurrency into MySQL.
- **Con:** Mis-sized pools cause either connection storms or artificial app queues.
- **Trade-off:** App pools vs external proxies (ProxySQL, RDS Proxy) for many languages/services.

## Comparison
vs raw [[mysql connection]] per request: pooling wins at scale. vs [[connection pooling]] general note: this is MySQL client-pool practice.

## Mistakes to Avoid
- Multiplying default pool sizes across 100 pods.
- Holding a borrowed connection during downstream HTTP.
- Disabling lifetime rotation and accumulating half-dead connections after failover.
