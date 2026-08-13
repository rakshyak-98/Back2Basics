[[mysql]] [[connection pooling]] [[mysql ssl connection]] [[mysql pool connection]]

# mysql connection

> A TCP session between client and `mysqld`—authentication, character set, session variables, and one thread of server execution until disconnect.

## Lifecycle

```txt
TCP connect ──► TLS (optional) ──► auth plugin handshake ──► session ready
```

Each connection maps to a server thread (traditionally) and counts against `max_connections`.

## Session state

- `@@autocommit`, isolation level
- Prepared statements tied to connection
- Temporary tables visible only to this session

## Production pattern

Applications should not open a new connection per HTTP request at scale—use [[mysql pool connection]] in front of the server.

## Sources

- MySQL Reference Manual — [Connection Management](https://dev.mysql.com/doc/refman/en/connection-management.html)
- MySQL Reference Manual — [max_connections](https://dev.mysql.com/doc/refman/en/server-system-variables.html#sysvar_max_connections)
