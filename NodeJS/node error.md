[[NodeJS]] [[Error handeling]] [[Runtime Errors]] [[mysql/mysql connection]]

# node error

> Common Node + MySQL disconnect: idle connection killed by server `wait_timeout` — use a pool that replaces dead sockets.

```txt
        node error ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers use **node error** to check whether you can explain the mechanis…

## Sources
- [Node.js — Errors](https://nodejs.org/api/errors.html) — deep-dive
- [Wikipedia — node error](https://en.wikipedia.org/wiki/node_error) — overview

## Key Concepts
- **wait_timeout:** Server closes idle sessions — Cloud DBs often set this low.
- **Pool:** Borrow/return connections — Survives idle better than one conn.
- **PROTOCOL_CONNECTION_LOST:** Socket died mid-use — Retry once or let pool refresh.

## Technical Details
```txt
app ── stale conn ──► MySQL wait_timeout ──► PROTOCOL_CONNECTION_LOST
         prefer: createPool → auto replace
```

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

## Mistakes to Avoid
- **Mistake:** **One global connection in serverless**
- **Mistake:** **Swallowing pool errors**
- **Mistake:** **Disconnect after idle:** check Single `createConnection`
- **Mistake:** **Errors after nodemon:** check Stale handles
- **Mistake:** **Still timing out:** check Server timeout tiny
- **Mistake:** **Too many conns:** check Limit × replicas

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Common Node + MySQL disconnect: idle connection killed by server `wait_timeout` …).
- **Con / when not:** This note is a **failure playbook**, not a library

## Comparison
- vs [[Error handeling]]: know when each applies


### Use cases
- In production APIs and tooling, **node error** shows up whenever teams ship N…
