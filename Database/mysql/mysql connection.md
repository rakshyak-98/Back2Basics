[[mysql]] [[connection pooling]] [[mysql ssl connection]] [[mysql pool connection]] [[variables]]

# mysql connection

> A TCP session between client and `mysqld` — authentication, character set, session variables, and one unit of server work until disconnect.





## Interview Relevance
Interviewers ask how connections relate to `max_connections`, why pooling exists, and what state lives on a session (autocommit, temp tables, prepared statements).

## Sources
- [Connection Management](https://dev.mysql.com/doc/refman/en/connection-management.html) — overview
- [max_connections](https://dev.mysql.com/doc/refman/en/server-system-variables.html#sysvar_max_connections) — deep-dive

## Key Concepts
- **One connection ≈ one server thread** (classic model) counting against `max_connections`.
- **Handshake:** TCP → optional TLS ([[mysql ssl connection]]) → auth plugin → session ready.
- **Session state:** `@@autocommit`, isolation level, user variables, temporary tables, prepared statements.
- **Pooling:** Reuse sessions in the app or a proxy ([[mysql pool connection]], [[connection pooling]]).

## Technical Details
```txt
TCP connect ──► TLS (optional) ──► auth plugin handshake ──► session ready
```

Character set and timezone are session properties; mismatches cause mojibake or surprising `TIMESTAMP` conversions.

## Real-World Applications
APIs borrow from a pool sized so `instances × pool_max ≤ max_connections` with headroom for admin and replicas tooling.

## Pros/Cons or Trade-offs
- **Pro:** Sessions carry useful state (temp tables, transactions) for multi-statement work.
- **Con:** Each idle connection still costs memory; storms of connect/disconnect hurt latency.
- **Trade-off:** Longer-lived pooled connections vs rotation to shed bad session state.

## Comparison
vs HTTP request lifecycle: one request must not open a dedicated MySQL connection at scale — pool instead.

## Mistakes to Avoid
- Opening a new connection per HTTP request under load.
- Ignoring TLS for credentials on untrusted networks.
- Exhausting `max_connections` with pool × replica count math errors.
