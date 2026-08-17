[[NodeJS]] [[expressjs]] [[Stream]] [[Express middleware]]

# HTTP module

> Node’s built-in `http`/`https` servers and clients — Express sits on top; use raw server when you need the `Server` handle (WS, dual HTTP/HTTPS, graceful shutdown).





## Interview Relevance
Interviewers use **HTTP module** to check whether you can explain the mechanism in plain words and apply it under failure. Expect follow-ups on **IncomingMessage**, **ServerResponse**, **createServer(app)**.

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

## Real-World Applications
In production APIs and tooling, **HTTP module** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **Must consume or destroy request bodies** — unused bodies can pin sockets; **HTTP vs HTTPS** — TLS needs `https.createServer(options, app)`.

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Node’s built-in `http`/`https` servers and clients — Express sits on top; use ra…).
- **Con / when not:** **Simple apps happy with `app.listen`** — fine until you need the Server.
- **Con / when not:** **Prefer frameworks’ abstractions** unless you need low-level control.

## Comparison
vs [[expressjs]]: Express adds routing/middleware; `http` is the primitive Server/IncomingMessage/ServerResponse. vs [[Stream]]: know when each applies — do not treat them as interchangeable. vs [[Express middleware]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid
- **Must consume or destroy request bodies** — unused bodies can pin sockets.
- **HTTP vs HTTPS** — TLS needs `https.createServer(options, app)`.
- **Can’t attach WebSocket:** check Used only `app.listen` without server; fix: `createServer(app)` then IO(server)
- **Connections hang on deploy:** check No `server.close`; fix: Drain on SIGTERM
- **Header too large:** check Default limits; fix: Raise `maxHeaderSize` if needed
- **Body never read:** check Forgot consume stream; fix: Read/pipe or reject
