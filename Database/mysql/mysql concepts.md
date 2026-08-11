[[mysql]] [[mysql connection]] [[mysql transaction]] [[connection pooling]]

# mysql concepts

> mysql2 (Node) mental model — connection vs pool, `query` vs `execute`, transactions on a borrowed connection, and cleanup with `await using`.

---

## Mental model

**Say it in one breath:** One `createConnection` is a single socket; a `createPool` hands out reusable sockets; `execute` uses server prepared statements; multi-step txns must `getConnection` → begin → commit/rollback → `release`.

```txt
createPool
   ├─ pool.query / pool.execute     ── auto acquire + release
   └─ getConnection()               ── hold for TRANSACTION
         begin → work → commit/rollback → release()
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Pool** | Reuse TCP sessions | “Avoid connect-per-request latency.” |
| **query()** | Client-side escape | “Fine for ad hoc; SET ? object shorthand.” |
| **execute()** | Server prepared stmt | “Prefer for repeated / security-sensitive SQL.” |
| **namedPlaceholders** | `:name` binds | “Off by default; object binds need it or arrays.” |
| **await using** | Auto end/release | “Scope exit cleans the connection/pool.” |
| **release ≠ end** | Return to pool | “end() destroys; release() recycles.” |

---

## Standard config / commands

```js
import mysql from 'mysql2/promise'

const pool = mysql.createPool({
  host: 'localhost',
  user: 'app',
  password: '…',
  database: 'mydb',
  connectionLimit: 10,
  waitForConnections: true,
  namedPlaceholders: false,
  multipleStatements: false, // keep false in prod
})

const [rows] = await pool.execute(
  'SELECT * FROM users WHERE id = ?',
  [1],
)

const conn = await pool.getConnection()
try {
  await conn.beginTransaction()
  await conn.execute('INSERT INTO orders (user_id) VALUES (?)', [userId])
  await conn.commit()
} catch (e) {
  await conn.rollback()
  throw e
} finally {
  conn.release()
}

{
  await using connection = await mysql.createConnection({ /* … */ })
  const [rows] = await connection.query('SELECT 1')
} // end() on scope exit
```

| Knob | Why it matters |
|------|----------------|
| `connectionLimit` | Too high thunders MySQL `max_connections` |
| `queueLimit` | 0 = unlimited wait; set a cap to fail fast |
| `decimalNumbers` / bigints | Precision vs JS number limits |
| `multipleStatements` | SQL injection blast radius if on |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Bind parameters must be array | execute + object | Pass array, use `query`, or enable `namedPlaceholders` |
| Hung requests | Pool exhausted | Raise limit carefully; find leaks (no release) |
| Partial commits | Txn across pool.query calls | One `getConnection` for the whole txn |
| Too many connections | App replicas × pool size | Cap pools; use ProxySQL/RDS Proxy |
| Charset mojibake | connection charset | `utf8mb4` everywhere |

---

## Gotchas

> [!WARNING]
> **Never return a connection to the pool mid-transaction.**

> [!WARNING]
> **`execute` + `INSERT … SET ?` object** — often breaks; use `query` or explicit columns + arrays.

---

## When NOT to use

- **Browser talking to MySQL** — always via your API.
- **Huge unbounded result sets in memory** — stream rows (callback API) or paginate.

---

## Related

[[mysql connection]] [[mysql transaction]] [[mysql pool connection]] [[connection pooling]] [[MySQL Error]]
