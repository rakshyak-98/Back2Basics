[[NodeJS]] [[expressjs]] [[Stream]]

# HTTP module

> Node’s built-in `http`/`https` servers and clients — Express sits on top; use raw server when you need the `Server` handle (WS, dual HTTP/HTTPS, graceful shutdown).

## Mental model

**Say it in one breath:** `http.createServer(handler)` returns a `Server` you `listen` on. Pass an Express `app` as the handler when you need Socket.IO or custom lifecycle beyond `app.listen`.

```txt
http.Server → 'request' (req, res)
            → upgrade (WebSocket)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **IncomingMessage** | req stream | “Headers + readable body.” |
| --- | --- | --- |
| **ServerResponse** | res writable | “`writeHead` / `end`.” |
| **createServer(app)** | Express as handler | “Same app; you own the Server object.” |

## Standard config / commands

```js
import http from 'node:http'
import express from 'express'

const app = express()
const server = http.createServer(app)
server.listen(3000)

// Graceful shutdown
process.on('SIGTERM', () => {
  server.close(() => process.exit(0))
})
```

| Knob | Why it matters |

| `server.timeout` | Drop slow sockets |
| --- | --- |
| `keepAliveTimeout` | Interact with LBs correctly |
| `http.request` / `fetch` | Outbound calls |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Can’t attach WebSocket | Used only `app.listen` without server | `createServer(app)` then IO(server) |
| Connections hang on deploy | No `server.close` | Drain on SIGTERM |
| Header too large | Default limits | Raise `maxHeaderSize` if needed |
| Body never read | Forgot consume stream | Read/pipe or reject |

## Gotchas

> [!WARNING]
> **Must consume or destroy request bodies** — unused bodies can pin sockets.

> [!WARNING]
> **HTTP vs HTTPS** — TLS needs `https.createServer(options, app)`.

## When NOT to use

- **Simple apps happy with `app.listen`** — fine until you need the Server.
- **Prefer frameworks’ abstractions** unless you need low-level control.

## Related

[[expressjs]] [[Express middleware]] [[Stream]]
