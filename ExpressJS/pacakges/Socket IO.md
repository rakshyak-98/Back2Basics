[[ExpressJS]] [[express concepts]] [[WebRTC]] [[SSE (Server-Sent Events)]] [[uWebSocket]]

# Socket IO

> Socket.IO is a realtime event library with transport fallbacks (WebSocket first, then polling) — rooms, reconnect, and named events; not interchangeable with the browser's native WebSocket API.

---

## Client and server events

```txt
client.emit('chat', msg) ──► server.on('chat')
server.to('lobby').emit('chat', msg) ──► all clients in room
```

Engine.IO negotiates transport. The client must use the Socket.IO client library — a raw WebSocket client cannot speak the protocol.

---

## With Express

```js
import { createServer } from 'http'
import { Server } from 'socket.io'
const httpServer = createServer(app)
const io = new Server(httpServer, { cors: { origin: '*' } })
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
| Auth middleware | Validate `socket.handshake` (token in auth payload) |

---

## What breaks first

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Connect loop | Client/server version mismatch | Align major versions |
| Works on one node only | No shared adapter | Redis adapter + sticky sessions |
| CORS errors | Origin not allowed | Configure `cors` option |
| Unauthorized connections | No handshake auth | Middleware on `io.use` |

Socket.IO protocol ≠ raw WebSocket framing. Horizontal scale requires a pub/sub adapter.

---

## When to choose something else

- **One-way server push** — [[SSE (Server-Sent Events)]] is simpler.
- **Peer-to-peer media** — [[WebRTC]].
- **Standards-only WebSocket clients** — `ws` or [[uWebSocket]].

---

## Related

[[uWebSocket]] · [[SSE (Server-Sent Events)]] · [[express concepts]]
