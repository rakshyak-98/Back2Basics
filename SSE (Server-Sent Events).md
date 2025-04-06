- uni directional push from server to browser over HTTP.
- server pushes events -> client auto-receives over single long-lived connection.

> [!INFO] Built in browser support : `EventSource` API

- Browser -> opens persistent HTTP connection
- backend -> writes to it using `text/event-stream`