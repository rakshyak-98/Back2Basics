[[mysql/mysql connection]] [[connection pooling]] [[mysql/mysql ssl connection]] [[half-open connections]]

# MySQL connection pool (app-side)

> One-line: reuse TCP+auth sessions via `mysql2`/`createPool` — cap concurrency, always release; raw `createConnection` per request causes races and `PROTOCOL_CONNECTION_LOST`.

## Mental model

Each MySQL connection is a **server session** (memory, temp tables, transaction state). **Pool** maintains N open connections; app **borrows** for query duration and **releases** back.

```
Without pool:  req A ──conn──► START TX ... (held)
               req B ──same conn──► START TX  ← transaction interference

With pool:     req A ──borrow conn1──► commit ──release
               req B ──borrow conn2──► isolated session
```

See [[connection pooling]] for cross-DB theory (PgBouncer, sizing). This note is **Node/mysql2** and MySQL-specific session rules.

## Standard config / commands

### mysql2 pool (production pattern)

```javascript
import mysql from 'mysql2/promise';

const pool = mysql.createPool({
  host: process.env.MYSQL_HOST,
  user: process.env.MYSQL_USER,
  password: process.env.MYSQL_PASSWORD,
  database: process.env.MYSQL_DATABASE,
  waitForConnections: true,
  connectionLimit: 10,        // per app instance — aggregate across pods
  queueLimit: 0,
  enableKeepAlive: true,
  keepAliveInitialDelay: 10_000,
  ssl: { /* see [[mysql ssl connection]] */ },
});

export async function query(sql, params) {
  const [rows] = await pool.execute(sql, params);
  return rows;
}
```

### Transaction with dedicated connection

```javascript
const conn = await pool.getConnection();
try {
  await conn.beginTransaction();
  await conn.execute('UPDATE accounts SET balance = balance - ? WHERE id = ?', [100, 1]);
  await conn.execute('UPDATE accounts SET balance = balance + ? WHERE id = ?', [100, 2]);
  await conn.commit();
} catch (e) {
  await conn.rollback();
  throw e;
} finally {
  conn.release();  // mandatory
}
```

### Pool sizing

```txt
max_connections (MySQL) ≥ Σ (app_instances × connectionLimit) + admin
Typical app instance: 5–20 connections
```

### Health check

```sql
SELECT 1;
SHOW STATUS LIKE 'Threads_connected';
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `PROTOCOL_CONNECTION_LOST` | Idle timeout; firewall | `enableKeepAlive`; lower idle; validate pool on checkout |
| Wrong rollback / mixed transactions | Shared single connection | Use pool + `getConnection()` per transaction |
| Pool queue timeout | `connectionLimit` too low | Fix slow queries; modest ↑ limit; scale read replicas |
| `Too many connections` | Pods × limit | Reduce per-pod limit; ProxySQL; raise MySQL max carefully |
| Connection leak | Missing `release()` | `finally { conn.release() }`; monitor pool metrics |
| Prepared statement errors | Server restart | Pool handles reconnect; retry logic at app layer |

## Gotchas

> [!WARNING]
> **`createConnection` per request** — TCP+auth overhead and transaction cross-talk under concurrency.

> [!WARNING]
> **Long txn holds pool slot** — external HTTP inside transaction starves pool.

> [!WARNING]
> **Serverless many instances** — connection storm; use RDS Proxy or lower limit + fewer concurrency.

## When NOT to use

- **One-shot CLI script** — single connection is fine.
- **Cross-process sharing** — pool is in-process; use ProxySQL between services.

## Related

[[connection pooling]] [[mysql/mysql connection]] [[mysql/mysql ssl connection]] [[Database mistakes]]
