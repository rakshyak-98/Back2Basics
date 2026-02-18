```text
Error: The client was disconnected by the server because of inactivity. See wait_timeout and interactive_timeo
```

> [!INFO]
> use `mysql/pool` instead of a single long-lived connection `mysql.createConnection`.

- Your Node.js app holds onto a MySQL connection (or pool) for a long time.
- No queries are sent for longer than wait_timeout seconds (default usually 8 hours / 28800 s, but sometimes much lower — especially on hosted/cloud DBs).

> [!INFO]
> - When your app later tries to use that stale connection → boom, this error.

### Quick Fixes (choose one or combine)

1. **Use a connection pool + handle disconnects** (most recommended for production-like local dev)

```js
const mysql = require('mysql2'); // or 'mysql' — but mysql2 is better

const pool = mysql.createPool({
  host: 'localhost',
  user: 'your_user',
  password: 'your_pass',
  database: 'your_db',
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0,
  // Very helpful:
  connectTimeout: 10000,
  // Optional but useful in dev:
  // timezone: 'Z',
});

// Optional: better error handling + auto-reconnect logic
pool.on('error', (err) => {
  console.error('Pool error:', err);
  if (err.code === 'PROTOCOL_CONNECTION_LOST' || err.code === 'ER_CLIENT_INTERACTION_TIMEOUT') {
    console.log('MySQL connection lost — pool should recover automatically');
  }
});

// How to use it (promise style - recommended)
async function queryExample() {
  try {
    const [rows] = await pool.promise().query('SELECT 1');
    return rows;
  } catch (err) {
    if (err.code === 'ER_CLIENT_INTERACTION_TIMEOUT' || err.code === 'PROTOCOL_CONNECTION_LOST') {
      // You can retry once here if needed
      console.log('Retrying after timeout...');
      // or just let it fail and next request will get fresh conn from pool
    }
    throw err;
  }
}

```

### The pool automatically:

- Discards dead connections
- Creates new ones when needed
- Survives `nodemon` restarts much better

### Mysql 

```ini
[mysqld]
wait_timeout        = 86400
interactive_timeout = 86400
```

```sql
SHOW VARIABLES LIKE '%timeout%';
```

