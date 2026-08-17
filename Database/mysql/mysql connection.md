[[mysql]] [[connection pooling]] [[mysql ssl connection]] [[mysql pool connection]] [[variables]]

# mysql connection

> A TCP session between client and `mysqld` — authentication, character set, session variables, and one unit of server work until disconnect.

```txt
        mysql connection ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers ask how connections relate to `max_connections`, why pooling exi…

## Sources
- [Connection Management](https://dev.mysql.com/doc/refman/en/connection-management.html) — overview
- [max_connections](https://dev.mysql.com/doc/refman/en/server-system-variables.html#sysvar_max_connections) — deep-dive

## Key Concepts
- **One connection ≈ one server thread:** (classic model) counting against `max_connections`.
- **Handshake:** TCP → optional TLS ([[mysql ssl connection]]) → auth plugin → session ready.
- **Session state:** `@@autocommit`, isolation level, user variables, temporary tables, prepared s…
- **Pooling:** Reuse sessions in the app or a proxy ([[mysql pool connection]], [[connection…

## Technical Details
```txt
TCP connect ──► TLS (optional) ──► auth plugin handshake ──► session ready
```

- Character set and timezone are session properties

## Mistakes to Avoid
- **Mistake:** Opening a new connection per HTTP request under load
- **Mistake:** Ignoring TLS for credentials on untrusted networks
- **Mistake:** Exhausting `max_connections` with pool × replica count math erro…

## Pros/Cons or Trade-offs
- **Pro:** Sessions carry useful state (temp tables, transactions) for multi-statement work.
- **Con:** Each idle connection still costs memory; storms of connect/disconnect hurt latency.
- **Trade-off:** Longer-lived pooled connections vs rotation to shed bad session state.

## Comparison
- vs HTTP request lifecycle: one request must not open a dedicated MySQL connec…


### Use cases
- APIs borrow from a pool sized so `instances × pool_max ≤ max_connections` wit…
