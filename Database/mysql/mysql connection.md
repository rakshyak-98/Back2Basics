`createConnection`
- One TCP connection to MySQL, reused for all queries.

Good for
- cli scripts, migrations, one-off jobs.
- very low traffic
- Simple apps where you want minimal setup.

Limitation 
- One query at a time per connection -> concurrent HTTP requests queue on the same connection.
- Transactions block everything else on that connection until commit/rollback.
- If the connection drops, all routes fail until reconnect.

`createPool`
- A pool of connection (e.g. 10). Each request borrows one, runs queries, then releases it.

Good for
- Web API's with concurrent requests.
- Routes that use `async/await` and transactions.
- Production services where multiple users hit the API at once.
- Avoiding "connection busy" bottlenecks.

Tradeoffs
- More DB connection open (controlled by `connectionLimit`)
- Needed to always release connections in `finally` when using `getConnection()`