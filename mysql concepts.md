## mysql2 — Full Feature Reference

> Latest version: **3.20.0** — a fast MySQL driver implementing core protocol, prepared statements, SSL and compression in native JS. No native bindings — installs cleanly on Linux, Mac, and Windows.

---

### 1. Installation

```bash
npm install mysql2

# TypeScript support
npm install mysql2
npm install --save-dev @types/node  # required for TS
```

---

### 2. `createConnection()` — Single Connection

```js
import mysql from 'mysql2/promise'  // Promise API (recommended)
// import mysql from 'mysql2'       // Callback API

const connection = await mysql.createConnection({
  host: 'localhost',        // DB host
  port: 3306,               // default MySQL port
  user: 'root',
  password: 'secret',
  database: 'mydb',

  // --- Optional config ---
  charset: 'utf8mb4',       // default charset (handles emojis)
  timezone: 'Z',            // store/retrieve dates as UTC
  connectTimeout: 10000,    // ms before connection attempt times out

  namedPlaceholders: false, // enable :name style placeholders
  decimalNumbers: false,    // DECIMAL returned as string by default (precision safe)
  dateStrings: false,       // return dates as strings instead of Date objects
  jsonStrings: false,       // return JSON columns as strings instead of parsed objects
  rowsAsArray: false,       // return rows as arrays instead of objects
  bigNumberStrings: false,  // return BIGINT as strings
  supportBigNumbers: false, // handle BIGINT columns

  multipleStatements: false, // ⚠️ allow multiple SQL statements per query (security risk)
  flags: [],                 // custom connection flags
  debug: false,              // log protocol packets
})

// Always close when done
await connection.end()      // graceful shutdown (drains queue)
connection.destroy()        // immediate hard close (no drain)
```

---

### 3. `await using` — Explicit Resource Management _(Latest)_

`await using` and `using` leverage Explicit Resource Management to automatically call `.end()` or `.release()` when the variable goes out of scope, so you never forget to clean up connections.

```js
import mysql from 'mysql2/promise'

{
  // connection.end() is called automatically on scope exit
  await using connection = await mysql.createConnection({
    host: 'localhost', user: 'root', database: 'mydb'
  })

  const [rows] = await connection.query('SELECT * FROM users')
  // No need to manually call connection.end()
}

// Also works with pools:
{
  await using pool = mysql.createPool({ /* config */ })
  // pool.end() auto-called on scope exit
}
```

---

### 4. `connection.query()` — Simple Queries

```js
// Basic query — no preparation, results returned as objects
const [rows, fields] = await connection.query('SELECT * FROM users')
// rows   → array of row objects
// fields → column metadata (name, type, length, etc.)

// Positional placeholders (? ) — client-side escaped
const [rows] = await connection.query(
  'SELECT * FROM users WHERE age > ? AND name = ?',
  [18, 'Alice']  // values array maps to ? in order
)

// Named placeholders — requires namedPlaceholders: true in config
const [rows] = await connection.query(
  'SELECT * FROM users WHERE id = :id',
  { id: 5 }  // pass an object with matching keys
)

// Insert shorthand — pass an object to map columns automatically
const [result] = await connection.query(
  'INSERT INTO users SET ?',
  { name: 'Bob', age: 30 }  // column: value mapping
)
// result.insertId      → auto-increment ID of inserted row
// result.affectedRows  → number of rows affected
// result.changedRows   → rows actually changed (vs. matched)
```

---

### 5. `connection.execute()` — Prepared Statements

`connection.execute()` internally calls prepare and query. On subsequent calls the cached statement is re-used. This protects against SQL injection at the protocol level.

```js
// execute() = prepare + query, with LRU statement caching
const [rows, fields] = await connection.execute(
  'SELECT * FROM users WHERE name = ? AND age > ?',
  ['Alice', 18]
)

// Manually prepare a statement for repeated use
const stmt = await connection.prepare(
  'SELECT * FROM users WHERE id = ?'
)
const [rows1] = await stmt.execute([1])
const [rows2] = await stmt.execute([2])  // re-uses prepared statement
await stmt.close()  // release the prepared statement

// Named placeholders also work with execute()
// (requires namedPlaceholders: true)
const [rows] = await connection.execute(
  'SELECT * FROM users WHERE id = :id',
  { id: 5 }
)
```

> **`query()` vs `execute()`**: `query()` does client-side escaping; `execute()` uses real server-side prepared statements — preferred for security and repeated queries.

---

### 6. `createPool()` — Connection Pooling

Connection pools help reduce the time spent connecting to the MySQL server by reusing a previous connection, leaving them open instead of closing when you are done with them. This improves the latency of queries as you avoid all of the overhead that comes with establishing a new connection.

```js
import mysql from 'mysql2/promise'

const pool = mysql.createPool({
  host: 'localhost',
  user: 'root',
  database: 'mydb',
  password: 'secret',

  // --- Pool-specific config ---
  connectionLimit: 10,        // max total connections in pool (default: 10)
  maxIdle: 10,                // max idle connections kept open (default: = connectionLimit)
  idleTimeout: 60000,         // ms before idle connection is closed (default: 60000)
  waitForConnections: true,   // queue requests when pool is full (default: true)
  queueLimit: 0,              // max queued requests (0 = unlimited)
  enableKeepAlive: true,      // send TCP keepalive packets
  keepAliveInitialDelay: 0,   // ms delay before first keepalive
})

// Use pool directly — connection is auto-acquired and released
const [rows] = await pool.query('SELECT * FROM users')
const [rows] = await pool.execute('SELECT * FROM users WHERE id = ?', [1])

// Manually acquire and release a connection from the pool
const conn = await pool.getConnection()
try {
  await conn.query('...')
} finally {
  conn.release()   // return connection back to pool (NOT end/destroy)
}

// Graceful shutdown — waits for all in-flight queries to complete
await pool.end()
```

---

### 7. Transactions

```js
// Always get a dedicated connection from the pool for transactions
const conn = await pool.getConnection()

try {
  await conn.beginTransaction()

  await conn.execute('INSERT INTO orders (user_id) VALUES (?)', [userId])
  await conn.execute('UPDATE inventory SET stock = stock - 1 WHERE id = ?', [itemId])

  await conn.commit()   // persist all changes
} catch (err) {
  await conn.rollback() // undo all changes on error
  throw err
} finally {
  conn.release()        // always return connection to pool
}

// Transaction isolation levels (set before beginTransaction)
await conn.query("SET TRANSACTION ISOLATION LEVEL READ COMMITTED")
// Options: READ UNCOMMITTED | READ COMMITTED | REPEATABLE READ (default) | SERIALIZABLE
```

---

### 8. Streaming — Query Result Streams

For large result sets — avoids loading all rows into memory at once.

```js
// Callback API only for streaming
import mysql from 'mysql2'

const connection = mysql.createConnection({ /* config */ })

// Stream rows one by one using event emitter
connection.query('SELECT * FROM large_table')
  .stream()
  .pipe(someWritableStream)

// Or listen to events manually
const query = connection.query('SELECT * FROM large_table')

query
  .on('result', (row) => {
    // process each row individually
    connection.pause()  // back-pressure: pause reading
    processRow(row, () => {
      connection.resume() // resume after processing
    })
  })
  .on('fields', (fields) => {
    // column metadata
  })
  .on('end', () => {
    // all rows consumed
  })
  .on('error', (err) => {
    // handle stream error
  })
```

---

### 9. `createPoolCluster()` — Multi-Server Pool Cluster

Pool clusters allow you to manage multiple connection pools for different database servers, enabling features like read/write splitting and load balancing.

```js
import mysql from 'mysql2/promise'

const cluster = mysql.createPoolCluster({
  canRetry: true,           // retry on connection failure (default: true)
  removeNodeErrorCount: 5,  // remove node after this many errors (default: 5)
  restoreNodeTimeout: 0,    // ms before retrying removed node (0 = never restore)
  defaultSelector: 'RR'    // default load-balance selector (see below)
})

// Add named nodes to the cluster
cluster.add('MASTER', { host: 'primary.db', user: 'root', database: 'mydb' })
cluster.add('REPLICA1', { host: 'replica1.db', user: 'root', database: 'mydb' })
cluster.add('REPLICA2', { host: 'replica2.db', user: 'root', database: 'mydb' })

// Get a connection by pattern + selector
// Selector options:
//   'RR'     → Round-Robin (default) — rotate between matching nodes
//   'RANDOM' → random node selection
//   'ORDER'  → always first available node

const masterConn = await cluster.getConnection('MASTER')
const replicaConn = await cluster.getConnection('REPLICA*', 'RR') // matches all REPLICAs

await masterConn.query('INSERT INTO ...')   // writes → master
await replicaConn.query('SELECT ...')       // reads → replica

masterConn.release()
replicaConn.release()

// Namespace — scoped query helper (no manual getConnection needed)
const replicaPool = cluster.of('REPLICA*', 'RR')
const [rows] = await replicaPool.query('SELECT * FROM users')

await cluster.end()
```

---

### 10. SSL / TLS Connections

```js
import fs from 'fs'

const connection = await mysql.createConnection({
  host: 'secure.db.example.com',
  user: 'root',
  database: 'mydb',
  ssl: {
    ca: fs.readFileSync('./certs/ca.pem'),       // CA certificate
    cert: fs.readFileSync('./certs/client-cert.pem'), // client cert
    key: fs.readFileSync('./certs/client-key.pem'),   // client key
    rejectUnauthorized: true,   // ✅ always true in production
    minVersion: 'TLSv1.2',      // minimum TLS version (default: TLSv1.2)
    maxVersion: 'TLSv1.3',      // maximum TLS version (default: TLSv1.3)
    verifyIdentity: false,      // verify server hostname (disabled by default)
  }
})

// Shorthand for Amazon RDS — uses AWS CA bundle automatically
const conn = await mysql.createConnection({
  host: 'myinstance.rds.amazonaws.com',
  ssl: 'Amazon RDS'
})
```

---

### 11. Named Placeholders

Named placeholders are converted to unnamed `?` on the client (the MySQL protocol does not support named parameters). If you reference a parameter multiple times under the same name it is sent to the server multiple times.

```js
const connection = await mysql.createConnection({
  host: 'localhost', user: 'root', database: 'mydb',
  namedPlaceholders: true   // enable globally on connection
})

// Use :name style instead of positional ?
const [rows] = await connection.execute(
  'SELECT * FROM users WHERE id = :id AND status = :status',
  { id: 5, status: 'active' }   // pass an object with matching keys
)

// Also works per-query without global config:
const [rows] = await connection.execute(
  { sql: 'SELECT * FROM users WHERE id = :id', namedPlaceholders: true },
  { id: 5 }
)
```

---

### 12. Escaping & SQL Injection Protection

```js
import mysql from 'mysql2'

// Escape values manually (for dynamic SQL construction)
const safeValue = mysql.escape(userInput)               // escapes a value
const safeId = mysql.escapeId(userColumnName)           // escapes an identifier (table/column name)
const safeSql = mysql.format('SELECT * FROM ?? WHERE id = ?', ['users', 5])
// ?? → identifier placeholder (escaped with backticks)
// ?  → value placeholder (escaped with quotes)

// mysql.raw() — inject unescaped SQL (use with caution!)
const ts = mysql.raw('CURRENT_TIMESTAMP()')
const sql = mysql.format('UPDATE posts SET modified = ?', [ts])
// → UPDATE posts SET modified = CURRENT_TIMESTAMP()

// Connection-level escape (same API)
connection.escape(value)
connection.escapeId(identifier)
connection.format(sql, values)
```

---

### 13. `changeUser()` — Switch Database/User on Existing Connection

```js
// Switch to a different user/database without creating a new connection
await connection.changeUser({
  user: 'newuser',
  password: 'newpassword',
  database: 'other_db',
  charset: 'utf8mb4'
})

// Also accepts passwordSha1 instead of plaintext password
// (useful in proxy implementations)
await connection.changeUser({ passwordSha1: Buffer.from(sha1Hash) })
```

---

### 14. TypeScript Support

TypeScript support requires `@types/node` to ensure proper interaction between TypeScript and the Node.js modules used by mysql2.

```ts
import mysql, {
  RowDataPacket,
  ResultSetHeader,
  OkPacket,
  FieldPacket,
  PoolOptions,
  ConnectionOptions
} from 'mysql2/promise'

// Type your SELECT results
interface User extends RowDataPacket {
  id: number
  name: string
  email: string
}

const [rows] = await connection.query<User[]>(
  'SELECT * FROM users WHERE id = ?', [1]
)
// rows is now typed as User[]

// Type INSERT/UPDATE/DELETE results
const [result] = await connection.execute<ResultSetHeader>(
  'INSERT INTO users (name) VALUES (?)', ['Alice']
)
result.insertId      // typed
result.affectedRows  // typed

// Rows as arrays (instead of objects)
interface UserArray extends RowDataPacket {
  [index: number]: string | number  // column values by index
}
const conn = await mysql.createConnection({ rowsAsArray: true /* ... */ })
const [rows] = await conn.query<UserArray[]>('SELECT id, name FROM users')
```

---

### 15. Promise Wrapper — `mysql2/promise` vs `mysql2`

```js
// Option A: Full Promise API (recommended for new projects)
import mysql from 'mysql2/promise'
const conn = await mysql.createConnection({ /* ... */ })

// Option B: Callback API with on-demand Promise wrapping
import mysql from 'mysql2'
const conn = mysql.createConnection({ /* ... */ })
const promiseConn = conn.promise()   // wraps a single connection
await promiseConn.query('SELECT 1')

// Option C: Custom Promise implementation (e.g. Bluebird)
import bluebird from 'bluebird'
const conn = await mysql.createConnection({
  host: 'localhost', user: 'root',
  Promise: bluebird    // swap in custom Promise library
})
```

---

### 16. Connection Events

```js
// Available on callback-style connections (mysql2 not mysql2/promise)
connection.on('connect', () => { /* connection established */ })
connection.on('end', () => { /* connection closed */ })
connection.on('error', (err) => {
  // err.code examples:
  // 'PROTOCOL_CONNECTION_LOST' → server closed connection
  // 'ER_ACCESS_DENIED_ERROR'   → bad credentials
  // 'ECONNREFUSED'             → DB server not reachable
  if (err.fatal) reconnect()
})
connection.on('enqueue', () => { /* query queued */ })

// Pool events
pool.on('acquire', (conn) => { /* connection acquired from pool */ })
pool.on('release', (conn) => { /* connection released back to pool */ })
pool.on('connection', (conn) => { /* new connection created */ })
pool.on('enqueue', () => { /* waiting for available connection */ })
```

---

### Summary Table

|Feature|Purpose|
|---|---|
|`createConnection()`|Single connection to MySQL server|
|`await using` / `using`|Auto-cleanup via Explicit Resource Management|
|`connection.query()`|Simple queries with client-side escaping|
|`connection.execute()`|Server-side prepared statements + LRU cache|
|`connection.prepare()`|Manual prepared statement lifecycle control|
|`createPool()`|Connection pooling for performance|
|`pool.getConnection()`|Manual acquire/release from pool|
|Transactions|`beginTransaction / commit / rollback`|
|Streaming|Process large result sets row-by-row|
|`createPoolCluster()`|Multi-server clusters, read/write splitting|
|SSL / TLS|Encrypted connections, cert-based auth|
|Named Placeholders|`:name` style parameters for readability|
|Escaping helpers|`escape / escapeId / format / raw`|
|`changeUser()`|Switch user/database on live connection|
|TypeScript support|Full types: `RowDataPacket`, `ResultSetHeader`, etc.|
|Promise Wrapper|`mysql2/promise` or per-connection `.promise()`|
|Connection Events|Monitor connect, error, acquire, release lifecycle|
