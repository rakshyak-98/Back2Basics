<!-- note-strategy: operational -->
[[mysql]] [[connection pooling]] [[cli]] [[half-open connections]]

# mysql connection

> A MySQL connection is one TCP (or socket) session to the server — one query stream at a time unless you pool.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** `createConnection` = one shared pipe; `createPool` = a small set of pipes that HTTP handlers borrow and return.

```txt
createConnection          createPool
  App ──► one conn          App ──► borrow ──► conn ──► release
           │                         │
           └─ queue if busy          └─ N concurrent queries
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Connection** | Authenticated session to mysqld | “State and transactions bind to the connection.” |
| **Pool** | Reusable set of connections | “Web APIs need a pool so requests don’t serialize.” |
| **Borrow / release** | Take from pool, put back | “Always release in `finally` or you leak slots.” |
| **connectionLimit** | Max open connections from this app | “Cap below MySQL `max_connections` across all apps.” |
| **Idle timeout** | Server or LB closes quiet sockets | “Half-open connections look alive until first query fails.” |

### When which

| Pattern | Use when | Avoid when |
|---------|----------|------------|
| **createConnection** | CLI, migrations, one-off jobs | Concurrent HTTP handlers |
| **createPool** | APIs, async routes, prod traffic | Tiny scripts (overhead / surprise open count) |

---

## Standard config / commands

```js
// mysql2 — single connection (scripts)
const conn = await mysql.createConnection({
  host: '127.0.0.1', user: 'app', password: '...', database: 'db',
})

// pool (APIs)
const pool = mysql.createPool({
  host: '127.0.0.1', user: 'app', password: '...', database: 'db',
  connectionLimit: 10,
  waitForConnections: true,
  queueLimit: 0,
})

const conn = await pool.getConnection()
try {
  await conn.beginTransaction()
  // ...
  await conn.commit()
} catch (e) {
  await conn.rollback()
  throw e
} finally {
  conn.release()
}
```

| Knob | Why it matters |
|------|----------------|
| `connectionLimit` | Too high → server `Too many connections`; too low → queue latency |
| `host: 127.0.0.1` | Forces TCP; avoids socket surprises in containers |
| Pool + transaction | Hold one borrowed connection for the whole txn |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Requests pile up / timeout | One shared `createConnection` under load | Switch to pool |
| `Too many connections` | `SHOW VARIABLES LIKE 'max_connections';` app limits | Lower `connectionLimit`; raise server cap carefully |
| Pool exhausted | Missing `release()` | `finally { conn.release() }` |
| Random “connection lost” | Idle kill by LB / `wait_timeout` | Pool ping / reconnect; see [[half-open connections]] |
| Txn sees other requests’ data | Sharing one connection across async work | One borrowed conn per txn; never share across requests |

---

## Gotchas

> [!WARNING]
> **One connection = one query at a time** — concurrent awaits on the same connection serialize or corrupt session state.

> [!WARNING]
> **Transactions pin the connection** — hold from `BEGIN` to `COMMIT`/`ROLLBACK`; don’t return to the pool mid-txn.

> [!WARNING]
> **Sum of all app pools ≤ `max_connections`** — replicas, admin tools, and cron count too.

---

## When NOT to use

- **Single-connection in a web server** — use a pool ([[connection pooling]]).
- **Pool for a 10-line migration** — one connection is simpler and safer to reason about.
- **Opening a new connection per query** — handshake cost + connection storms.

---

## Related

[[mysql]] [[connection pooling]] [[cli]] [[mysql pool connection]] [[half-open connections]] [[ACID]]
