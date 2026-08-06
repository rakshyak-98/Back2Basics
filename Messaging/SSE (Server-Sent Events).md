[[Messaging]]

# SSE (Server-Sent Events)

> One-line: what / why for **SSE (Server-Sent Events)** — source TBD.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

- uni directional push from server to browser over HTTP.
- server pushes events -> client auto-receives over single long-lived connection.
> [!INFO] Built in browser support : `EventSource` API
- Browser -> opens persistent HTTP connection
- backend -> writes to it using `text/event-stream`
- One way communication (server -> client only).
- Uses standard HTTP.
- Browser automatically reconnects if connection drops.
- Data format: `text/event-stream`.
- Lightweight compared to WebSockets when only server updates are needed.
| Feature        | SSE             | WebSocket                        |
| -------------- | --------------- | -------------------------------- |
| Direction      | Server → Client | Bidirectional                    |
| Protocol       | HTTP            | WebSocket                        |
| Auto Reconnect | Yes             | Manual                           |
| Simplicity     | Simple          | More complex                     |
| Best For       | Live updates    | Chat, gaming, collaborative apps |

## Standard config / commands

…

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| … | … | … |

## Gotchas

> [!WARNING]
> …

## When NOT to use

…

## Related

[[…]]
