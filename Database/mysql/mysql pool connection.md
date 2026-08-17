[[mysql connection]] [[connection pooling]] [[mysql]] [[variables]]

# mysql pool connection

> Application-side pool of reusable MySQL sessions — HikariCP, mysql2 pool, SQLAlchemy `QueuePool` — to cap server connections and amortize handshake cost.

```txt
        mysql pool connect ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Capacity planning: `pool_max × app_instances` versus `max_connections`

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

## Mistakes to Avoid
- **Mistake:** Multiplying default pool sizes across 100 pods
- **Mistake:** Holding a borrowed connection during downstream HTTP
- **Mistake:** Disabling lifetime rotation and accumulating half-dead connectio…

## Pros/Cons or Trade-offs
- **Pro:** Stable latency, controlled concurrency into MySQL.
- **Con:** Mis-sized pools cause either connection storms or artificial app queues.
- **Trade-off:** App pools vs external proxies (ProxySQL, RDS Proxy) for many languages/services.

## Comparison
- vs raw [[mysql connection]] per request: pooling wins at scale


### Use cases
- Each Kubernetes pod runs HikariCP at 10–20
