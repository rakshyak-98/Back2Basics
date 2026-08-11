[[NodeJS]] [[Error handeling]] [[Runtime Errors]] [[mysql/mysql connection]]

# node error

> Common Node + MySQL disconnect: idle connection killed by server `wait_timeout` — use a pool that replaces dead sockets.

---

## Mental model

**Say it in one breath:** A long-held single connection goes idle longer than MySQL’s timeout; next query hits a dead socket. Pools discard dead conns and open fresh ones.

```txt
app ── stale conn ──► MySQL wait_timeout ──► PROTOCOL_CONNECTION_LOST
         prefer: createPool → auto replace
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **wait_timeout** | Server closes idle sessions | “Cloud DBs often set this low.” |
| **Pool** | Borrow/return connections | “Survives idle better than one conn.” |
| **PROTOCOL_CONNECTION_LOST** | Socket died mid-use | “Retry once or let pool refresh.” |

## Standard config / commands

```js
import mysql from 'mysql2/promise'

const pool = mysql.createPool({
  host: 'localhost',
  user: 'u',
  password: 'p',
  database: 'db',
  waitForConnections: true,
  connectionLimit: 10,
  connectTimeout: 10_000,
})

const [rows] = await pool.query('SELECT 1')
```

```sql
SHOW VARIABLES LIKE '%timeout%';
```

| Knob | Why it matters |
|------|----------------|
| `connectionLimit` | Cap DB load |
| Pool `error` handler | Log lost connections |
| Server timeouts | Align with pool idle behavior |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Disconnect after idle | Single `createConnection` | Switch to pool |
| Errors after nodemon | Stale handles | Pool; don’t keep global conn across restarts |
| Still timing out | Server timeout tiny | Raise `wait_timeout` or ping/keepalive |
| Too many conns | Limit × replicas | Lower `connectionLimit` |

---

## Gotchas

> [!WARNING]
> **One global connection in serverless** — cold starts + timeouts; prefer short-lived or external pooler.

> [!WARNING]
> **Swallowing pool errors** — always log `PROTOCOL_CONNECTION_LOST` / timeout codes.

---

## When NOT to use

- This note is a **failure playbook**, not a library — for application errors see [[Error handeling]].

---

## Related

[[Error handeling]] [[Runtime Errors]] [[mysql/mysql connection]]
