[[NodeJS]] [[expressjs]] [[Stream]] [[Express middleware]]

# HTTP module

> Node’s built-in `http`/`https` servers and clients — Express sits on top; use raw server when you need the `Server` handle (WS, dual HTTP/HTTPS, graceful shutdown).

```txt
        HTTP module ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers use **HTTP module** to check whether you can explain the mechani…

## Sources
- [Node.js — HTTP](https://nodejs.org/api/http.html) — deep-dive
- [Wikipedia — HTTP module](https://en.wikipedia.org/wiki/HTTP_module) — overview

## Key Concepts
- **IncomingMessage:** req stream — Headers + readable body.
- **ServerResponse:** res writable — `writeHead` / `end`.
- **createServer(app):** Express as handler — Same app; you own the Server object.

## Technical Details
```txt
http.Server → 'request' (req, res)
            → upgrade (WebSocket)
```

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
|------|----------------|
| `server.timeout` | Drop slow sockets |
| `keepAliveTimeout` | Interact with LBs correctly |
| `http.request` / `fetch` | Outbound calls |

## Mistakes to Avoid
- **Mistake:** **Must consume or destroy request bodies**
- **Mistake:** **HTTP vs HTTPS** — TLS needs `https.createServer(options, app)`
- **Mistake:** **Can’t attach WebSocket:** check Used only `app.listen` without…
- **Mistake:** **Connections hang on deploy:** check No `server.close`
- **Mistake:** **Header too large:** check Default limits
- **Mistake:** **Body never read:** check Forgot consume stream

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Node’s built-in `http`/`https` servers and clients — Express sits on top; use ra…).
- **Con / when not:** **Simple apps happy with `app.listen`**
- **Con / when not:** **Prefer frameworks’ abstractions** unless you need low-l…

## Comparison
- vs [[expressjs]]: Express adds routing/middleware; `http` is the primitive Se…


### Use cases
- In production APIs and tooling, **HTTP module** shows up whenever teams ship …
