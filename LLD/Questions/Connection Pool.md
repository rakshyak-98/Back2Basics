[[Questions]] [[Design pattern/Singleton]] [[Database/connection pooling]]

# Connection Pool

> Low-level design exercise — Singleton connection pool that hands out database connections and tracks available versus in-use slots.

## Mental model

**Say it in one breath:** A fixed pool of connections is created once; callers borrow, use, and release — like a library shelf where books must be returned before others can take them.

### Problem statement

Design a **connection pool** for a database module. Use **Singleton** so one pool manager exists and access is thread-safe.

### Requirements

**Part 1 — Singleton**

- `ConnectionPoolImpl` implements `ConnectionPool`.
- `get_instance(max_connections)` returns the singleton.
- `reset_instance()` clears it (for tests).

**Part 2 — Pool management**

| Method | Behavior |
| --- | --- |
| `initialize_pool()` | Create fixed connections; track available vs in-use |
| `get_connection()` | Return an available connection; mark unavailable |
| `release_connection(conn)` | Mark connection available again |
| `get_available_connections_count()` | Count free slots |
| `get_total_connections_count()` | Total pool size |

## Standard config / commands

```python
pool = ConnectionPoolImpl.get_instance(max_connections=10)
pool.initialize_pool()
conn = pool.get_connection()
# use conn
pool.release_connection(conn)
```

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Hang on `get_connection` | Pool exhausted | Increase max size or fix connection leaks |
| Connection used twice | Missing `release` | `try/finally` around borrow |
| Stale connections | Idle timeout | Health-check or recycle idle connections |

## Gotchas

> [!WARNING]
> **Leaked connections** — every `get` must pair with `release` or the pool starves.

## When NOT to use

- **Serverless with one query** — pool overhead may exceed benefit; use managed proxy (RDS Proxy, PgBouncer).

## Related

[[Database/connection pooling]] [[Design pattern/Singleton]] [[LLD/Questions/Logger]]
