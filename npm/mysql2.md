[[npm]] [[mysql]] [[mysql connection]] [[mysql pool connection]] [[node package json]]

# mysql2

> Popular Node.js MySQL / MariaDB client — talks to the server over the wire with prepared statements, pooling, and optional Promise APIs.

```txt
        mysql2 ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers ask about `mysql2` to see if you use connection pools, prepared …

## Sources
- [mysql2 GitHub documentation](https://github.com/sidorares/node-mysql2) — deep-dive
- [MySQL protocol overview (Oracle)](https://dev.mysql.com/doc/dev/mysql-server/latest/PAGE_PROTOCOL.html) — overview

## Key Concepts
- **Connection vs pool:** a single connection serializes queries
- **Prepared statements / placeholders:** `execute('SELECT … WHERE id = ?', [id])` → binds values safely
- **Promise API:** `require('mysql2/promise')` → `async/await` without callback pyramids.
- **Charset / timezone:** mismatch with the server causes mojibake and off-by-hours timestamps.
- **Release discipline:** always release pooled connections (or use helpers that do) → pool exhaustion …


- **Core:** `mysql2` is an npm package that implements the MySQL client protocol in Node.…

## Technical Details
```js
import mysql from "mysql2/promise";

const pool = mysql.createPool({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
  waitForConnections: true,
  connectionLimit: 10,
});

const [rows] = await pool.execute(
  "SELECT id, email FROM users WHERE id = ?",
  [userId]
);
```

```bash
npm install mysql2
```

| Symptom | Likely cause |
|---------|--------------|
| Queries hang after traffic spike | Pool exhausted; connections not released |
| `ER_ACCESS_DENIED_ERROR` | Wrong user/password/host grant |
| `PROTOCOL_CONNECTION_LOST` | Idle timeout / server restart — reconnect or pool |
| SQL injection incident | String concatenation instead of `?` placeholders |
| Wrong characters in strings | Charset not `utf8mb4` end-to-end |

## Mistakes to Avoid
- **Mistake:** Creating a new connection per request instead of a pool
- **Mistake:** Interpolating request parameters into SQL strings
- **Mistake:** Ignoring timezone/charset settings until production data looks w…

## Pros/Cons or Trade-offs
- **Pro:** Mature, fast, Promise-friendly; close to the MySQL protocol without an ORM.
- **Con:** You still own schema, migrations, and transactions — no unit-of-work abstraction.
- **Con:** Misconfigured pools under serverless (many cold starts) can overwhelm the database — tune limits or use a proxy.

## Comparison
- vs `mysql` (older): use `mysql2` for active maintenance and performance.
- vs ORMs (Sequelize/Prisma): ORMs add modeling and migrations


### Use cases
- Express/Fastify APIs, workers, and migration scripts that talk to MySQL or Ma…

- **Example:** An API handler borrows from a pool, `execute`s a parameterized q…
