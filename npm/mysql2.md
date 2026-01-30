> [!NOTE]
> - in the `mysql2` package when you run DDL statements the response is a `RequestHeader`, not rows.

## Create Pool connection

```js

const pool = mysql.createPool({
  port: process.env.DB_PORT,
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_DATABASE,
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0,
  connectTimeout: 10000,
  idleTimeout: 60000,
  enableKeepAlive: true
});

```

## Connection shutdown

```js

(async () => {
  try {
    const connection = await pool.getConnection();
    console.log(
      `MySQL pool initialized | Connected to: ${process.env.DB_DATABASE}`
    );
    connection.release();
  } catch (err) {
    console.error("Failed to initialize MySQL pool:", err);
    process.exit(1);
  }
})();

process.on("SIGTERM", async () => {
  console.log("Shutting down... closing DB Pool");
  await pool.end();
  process.exit(0);
});

```
