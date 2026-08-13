[[mysql connection]] [[connection pooling]] [[mysql]]

# mysql pool connection

> Application-side pool of reusable MySQL sessions—HikariCP, mysql2 pool, SQLAlchemy `QueuePool`—to cap server connections and amortize handshake cost.

## Configuration sketch (HikariCP)

```properties
maximumPoolSize=20
connectionTimeout=30000
idleTimeout=600000
maxLifetime=1800000
```

## Failure modes

| Symptom | Check |
|---------|-------|
| `Too many connections` on MySQL | Pool max × instances vs `max_connections` |
| Stale connection errors | Enable test query on checkout; reduce `maxLifetime` |
| Pool wait timeouts | Slow queries holding connections |

## Sources

- MySQL Reference Manual — [Connection Interfaces](https://dev.mysql.com/doc/connector-j/en/connector-j-usagenotes-connect-drivermanager.html)
- HikariCP — [Configuration](https://github.com/brettwooldridge/HikariCP#configuration-knobs)
