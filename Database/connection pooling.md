[[mysql]] [[psql essential]] [[ACID]] [[Database mistakes]] [[half-open connections]]

is a technique where an application **reuses existing connections** to a database or another service instead of creating a new connection for every request.

Without pooling
```txt
Request arrives
    ↓
Open database connection
    ↓
Authenticate
    ↓
Run SQL query
    ↓
Close connection
```
- If this happens thousands of times, repeatedly opening and closing connections becomes expensive.
With a **connection pool**, the application keeps a limited number of connections open:

```txt
                 ┌── Connection 1 ── Database
Request ───────► │── Connection 2 ── Database
                 │── Connection 3 ── Database
                 │── Connection 4 ── Database
                 └── Connection 5 ── Database
                     Connection Pool
```
**When a request needs the database, it borrows an available connection:**

```txt
1. Request needs DB
       ↓
2. Pool gives it Connection #3
       ↓
3. Application runs query
       ↓
4. Connection #3 is returned to pool
       ↓
5. Another request can reuse it
```
The important part is that **returning a connection to the pool usually does not close the underlying database connection.**

**Why use connection pooling ?**
Creating database connections can involve TCP setup, authentication, TLS negotiation, and database-side resource allocation, Reusing them therefore improves **latency and throughput** and prevents an application from creating an unlimited number of connections.

> A pool also provide a useful concurrency limit. At most roughly 10 requests can use those connections simultaneously. The others wait until a connection becomes available rather than opening 100 new database connections.

"Connection pooling = maintain a reusable collection of already-open connections and lend them out temporarily when needed."

# connection pooling

> Reuse open DB connections instead of TCP+auth per request — cuts latency and protects the server from connection storms — **HikariCP / PgBouncer docs** + Kleppmann.

---

## Mental model

```txt
Without pool:  Request → connect → auth → query → disconnect   (expensive)
With pool:     Request → borrow conn → query → return conn       (amortized)
```

Each DB connection consumes **RAM on server** (Postgres ~5–10MB each) and **FDs** on both sides. Spawning 500 app threads ≠ 500 DB connections — pool caps concurrency to what DB tolerates.

```txt
         ┌─────────────┐
App ───► │ Pool (app   │ ───► Postgres (max_connections = 100)
         │  or PgBouncer)│
         └─────────────┘
```

**Pool types:**
- **Client-side** (HikariCP, pgxpool, SQLAlchemy) — inside app process
- **Server-side** (PgBouncer, RDS Proxy, ProxySQL) — shared across many app instances

**Transaction vs session pooling:** session mode safe for prepared statements/temp tables; transaction mode higher density but breaks session-scoped features.

---

## Standard config / commands

### Postgres sizing rule of thumb

```txt
max_connections (Postgres) ≥ (app_instances × pool_max) + admin headroom
If product > ~100 effective connections → add PgBouncer
```

### HikariCP (JVM — production default)

```properties
spring.datasource.hikari.maximum-pool-size=20
spring.datasource.hikari.minimum-idle=5
spring.datasource.hikari.connection-timeout=30000
spring.datasource.hikari.idle-timeout=600000
spring.datasource.hikari.max-lifetime=1800000
spring.datasource.hikari.leak-detection-threshold=60000
```

### node pg pool

```javascript
import { Pool } from 'pg';

const pool = new Pool({
  host: process.env.PGHOST,
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 5000,
});

const client = await pool.connect();
try {
  await client.query('SELECT ...');
} finally {
  client.release();   // always — or leak
}
```

### PgBouncer (server-side)

```ini
[databases]
mydb = host=127.0.0.1 port=5432 dbname=mydb

[pgbouncer]
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 25
listen_port = 6432
```

App connects to `6432`, not direct Postgres `5432`.

### Verify pool health

```sql
-- Postgres: active connections
SELECT count(*), state FROM pg_stat_activity GROUP BY state;

SHOW max_connections;
```

```bash
# App metrics: pool active, idle, waiting threads (Hikari MXBean)
# Alert on pool waiting > 0 sustained
```

### Prepared statements + pooling

```txt
Transaction pooling (PgBouncer): disable prepared statements in driver
  OR use session pooling for ORMs heavy on prepares
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `too many connections` | `pg_stat_activity` count | Lower pool max; add PgBouncer; scale read replicas |
| Requests hang then timeout | Pool exhausted (all in use) | ↑ pool slightly; fix slow queries; leak detection |
| Connection leak after deploy | Missing `release()` / try-finally | Enable leak detection; audit ORM session lifecycle |
| `FATAL: remaining connection slots reserved` | Superuser slots only left | Kill idle connections; emergency terminate idle in `pg_stat_activity` |
| Spiky latency after idle | TCP/firewall dropped idle conn | `max-lifetime` < firewall timeout; `tcp_keepalive` |
| Works single pod, fails scaled | Each pod × pool_max | Aggregate math; central PgBouncer |
| Prepared statement errors via PgBouncer | pool_mode=transaction | Session mode or disable prepares |
| RDS Proxy auth errors | IAM token expiry | Refresh token; check proxy config |

---

## Gotchas

> [!WARNING]
> **Pool size ≠ faster** — too large increases DB contention and memory; tune from query latency and CPU.

> [!WARNING]
> **Long transactions hold pool slots** — open txn during external HTTP call starves pool.

> [!WARNING]
> **Migrations bypass pool** — flyway/liquibase direct connection OK; don't run DDL through transaction pooler.

> [!WARNING]
> **Serverless (Lambda)** — one pool per instance still explodes connections; use RDS Proxy or Data API pattern.

> [!WARNING]
> **Read replica routing** — pool must separate writer/reader endpoints; sticky txn on primary.

---

## When NOT to use

- **Single-threaded CLI cron** — one connection per job is fine.
- **Embedded SQLite** — file lock model; pooling in-process only (still useful for ORM).
- **Bypass pool for COPY/bulk load** — dedicated session with raised timeouts.

---

## M

## Related

[[Database mistakes]] · [[mysql]] · [[psql essential]] · [[ACID]] · [[half-open connections]] · [[file descriptors]] · [[AWS RDS]] · [[AWS Lambda]]
