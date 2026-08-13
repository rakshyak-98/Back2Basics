[[mysql]] [[mysql connection]] [[connection pooling]]

# MySQL storage

> Store Express (or similar) sessions in MySQL so logins survive process restarts and shared app instances.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** In-memory session stores die with the Node process; a MySQL session table is shared durable state behind a load balancer — slower than Redis, fine for moderate traffic.

```txt
Browser cookie ──► Node (express-session) ──► MySQL sessions table
                         ▲
              multiple app instances share one store
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Session store** | Where server-side session blobs live | “Cookie holds the id; MySQL holds the data.” |
| **MySQLStore** | `express-mysql-session` adapter | “Survives restart; horizontal scale-friendly.” |
| **clearExpired** | Periodic DELETE of old rows | “Without it the sessions table grows forever.” |
| **trust proxy** | Honor `X-Forwarded-*` | “Needed for Secure cookies behind nginx.” |

---

## Standard config / commands

```js
const session = require('express-session')
const MySQLStore = require('express-mysql-session')(session)

const store = new MySQLStore({
  host: '127.0.0.1',
  user: 'app',
  password: '…',
  database: 'app',
  createDatabaseTable: true,
  clearExpired: true,
  checkExpirationInterval: 900000,
})

app.set('trust proxy', 1)
app.use(session({
  secret: process.env.SESSION_SECRET,
  resave: false,
  saveUninitialized: false,
  store,
  cookie: { secure: true, httpOnly: true, sameSite: 'lax' },
}))
```

| Knob | Why it matters |
|------|----------------|
| `createDatabaseTable` | Auto-creates sessions table if missing |
| `clearExpired` | Prevents unbounded table growth |
| DB grants | Store needs INSERT/UPDATE/DELETE/SELECT |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Logged out after deploy | Memory store still in use | Point `store` at MySQLStore |
| Session lost across instances | Each box has own memory store | Shared MySQL/Redis store |
| Table missing / access denied | Grants + `createDatabaseTable` | GRANT; create table once |
| Cookie not set behind TLS terminator | `secure` + no trust proxy | `trust proxy` + Secure cookie |
| Sessions table huge | Expiration cleanup off | Enable `clearExpired` / TTL job |

---

## Gotchas

> [!WARNING]
> **MySQL ≠ Redis for hot sessions** — high QPS session churn prefers Redis; MySQL is persistence/simplicity.

> [!WARNING]
> **Don’t put secrets only in the cookie** — server store still needs a strong `secret` and HTTPS.

---

## When NOT to use

- **Stateless APIs** — prefer [[JWT]] / opaque tokens with no server session.
- **Very high session read/write rate** — use Redis (or similar) as the session store.

---

## Related

[[mysql connection]] [[connection pooling]] [[mysql]] [[JWT]]
