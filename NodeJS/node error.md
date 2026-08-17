[[NodeJS]] [[Error handeling]] [[Runtime Errors]] [[mysql/mysql connection]]

# node error

> Common Node + MySQL disconnect: idle connection killed by server `wait_timeout` — use a pool that replaces dead sockets.





## Interview Relevance
Interviewers use **node error** to check whether you can explain the mechanism in plain words and apply it under failure. Expect follow-ups on **wait_timeout**, **Pool**, **PROTOCOL_CONNECTION_LOST**.

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

## Real-World Applications
In production APIs and tooling, **node error** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **One global connection in serverless** — cold starts + timeouts; prefer short-lived or external pooler; **Swallowing pool errors** — always log `PROTOCOL_CONNECTION_LOST` / timeout codes.

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Common Node + MySQL disconnect: idle connection killed by server `wait_timeout` …).
- **Con / when not:** This note is a **failure playbook**, not a library — for application errors see [[Error handeling]].

## Comparison
vs [[Error handeling]]: know when each applies — do not treat them as interchangeable. vs [[Runtime Errors]]: know when each applies — do not treat them as interchangeable. vs [[mysql/mysql connection]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid
- **One global connection in serverless** — cold starts + timeouts; prefer short-lived or external pooler.
- **Swallowing pool errors** — always log `PROTOCOL_CONNECTION_LOST` / timeout codes.
- **Disconnect after idle:** check Single `createConnection`; fix: Switch to pool
- **Errors after nodemon:** check Stale handles; fix: Pool; don’t keep global conn across restarts
- **Still timing out:** check Server timeout tiny; fix: Raise `wait_timeout` or ping/keepalive
- **Too many conns:** check Limit × replicas; fix: Lower `connectionLimit`
