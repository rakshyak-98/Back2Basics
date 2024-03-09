is responsible for managing connection persistence and reuse of HTTP clients.
- maintains a queue of pending requests for a given host and port.
- reusing a single socket connection for each until the queue is empty.
- whether it is destroyed or pooled depends on the `keepAlive` option.
> [!INFO] Pooled connections have TCP keep-Alive enabled for them, but server can close idle connections.
- servers may also refuse to allow multiple requests over the same connection, in which case the connection will have to be remade for every request and cannot be pooled.
- the agent will still make the request to that server, but each one will occur over a new connection.
> [!INFO] When a connection is closed by the client or server, it is removed from the pool.
- used sockets consume OS resources.
- sockets are removed from an agent when the socket emits either a `close` event or an `agentRemove` event.