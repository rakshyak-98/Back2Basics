## Benefits of using `MySQLStore` with `express-session`:
1. **Persistence across server restarts**  
    Sessions are stored in MySQL, so users remain logged in even if the server restarts or crashes.
2. **Scalability**  
    Multiple Node.js instances can share sessions via a single MySQL store, enabling horizontal scaling behind a load balancer.
3. **Centralized session management**  
    Session data can be inspected, revoked, or managed directly through MySQL queries or admin tools.
4. **Memory efficiency**  
    Sessions are not stored in Node.js memory, reducing memory usage and avoiding memory leaks in long-running processes.
5. **Automatic cleanup support**  
    `express-mysql-session` can auto-clear expired sessions using `clearExpired` and `checkExpirationInterval` options.

### When not to use MySQLStore:
- For high throughput or low-latency apps, MySQL is slower than Redis.
- JWTs are a better fit for stateless APIs.
- In-memory stores like Redis are more performant for frequent session reads/writes.

### Edge cases:
- The session table must exist or be auto-created with `createDatabaseTable: true`.
- The MySQL user must have read/write access to the session table.
- Monitor table size if sessions are long-lived or traffic is high.
- Use `app.set('trust proxy', 1)` and configure cookies if behind a proxy like nginx or Heroku.