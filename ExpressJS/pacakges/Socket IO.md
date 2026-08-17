[[express concepts]] [[uWebSocket]] [[SSE (Server-Sent Events)]] [[WebRTC]] [[webhook]]

# Socket IO

> Socket.IO is a realtime event library with transport fallbacks (WebSocket first, then long-polling) — rooms, reconnect, and named events; not the browser’s native WebSocket API.

```txt
        Socket IO ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers ask when to use Socket.IO versus raw WebSockets, SSE, or WebRTC,…

## Sources
- [Socket.IO — Documentation](https://socket.io/docs/v4/) — deep-dive
- [Socket.IO — Using with Express](https://socket.io/docs/v4/server-api/) — overview
- [MDN — The WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API) — overview

## Key Concepts
- **Transport fallback:** WebSocket when possible, polling otherwise — works through awkward proxies.
- **Rooms:** logical groups for broadcast (`socket.join('lobby')`).
- **Handshake authentication:** validate tokens in `io.use` from `socket.handshake`
- **Adapter:** Redis (or similar) so emits reach clients on other nodes.
- **Protocol ≠ WS:** native `WebSocket` clients will fail against a Socket.IO server.


- **Core:** Engine.IO negotiates a transport and speaks the Socket.IO protocol on top. Cl…

## Technical Details
```txt
client.emit('chat', msg) ──► server.on('chat')
server.to('lobby').emit('chat', msg) ──► all clients in room
```

```js
import { createServer } from 'http'
import { Server } from 'socket.io'
const httpServer = createServer(app)
const io = new Server(httpServer, { cors: { origin: 'https://app.example' } })
io.use(async (socket, next) => {
  // validate socket.handshake.auth.token
  next()
})
io.on('connection', (socket) => {
  socket.join('lobby')
  socket.on('chat', (msg) => io.to('lobby').emit('chat', msg))
})
httpServer.listen(3000)
```

| Knob | Why it matters |
|------|----------------|
| CORS | Browser clients need allowed origins |
| Redis adapter | Multi-node room broadcast |
| Authentication middleware | Validate handshake before `connection` |
| Sticky sessions | Polling upgrade and sticky LB for multi-node |

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Connect loop | Client/server major version mismatch | Align versions |
| Works on one node only | No shared adapter | Redis adapter + sticky sessions |
| CORS errors | Origin not allowed | Configure `cors` |
| Unauthorized connections | No handshake checks | `io.use` middleware |

## Mistakes to Avoid
- **Mistake:** Pointing a raw WebSocket client at a Socket.IO server
- **Mistake:** Scaling to multiple nodes without a pub/sub adapter
- **Mistake:** Trusting client-emitted identity without handshake authentication
- **Mistake:** Setting `cors.origin: '*'` with credentials in production

## Pros/Cons or Trade-offs
- **Pro:** Rooms, ACK, reconnect, and fallbacks out of the box.
- **Con:** Custom protocol — harder to debug with generic WS tools.
- **Con:** Multi-node requires adapter + sticky sessions; operational cost rises.

## Comparison
- vs [[SSE (Server-Sent Events)]]: SSE is one-way server→client over HTTP
- vs [[WebRTC]]: peer media and data channels — different problem than server fanout.
- vs [[uWebSocket]] / `ws`: standards WebSocket; you build rooms and fallbacks yourself.
- vs Express HTTP: pair Socket.IO with `http.Server` wrapping the Express `app`.


### Use cases
- Chat, collaborative cursors, live dashboards, and notification fanout where r…

- **Example:** Two Kubernetes pods each hold half the sockets
