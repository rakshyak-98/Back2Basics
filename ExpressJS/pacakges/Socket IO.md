<!-- note-strategy: operational -->
[[ExpressJS]] [[express concepts]] [[WebRTC]] [[SSE (Server-Sent Events)]]

# Socket IO

> Socket.IO — realtime library with fallbacks (WebSocket first); events, rooms, and reconnect—broader than raw WS.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Client and server share event names. Engine.IO negotiates transport. Not identical to browser `WebSocket` API—need matching Socket.IO client.

```txt
client emit ──► server on
server to(room).emit ──► clients
```

---

## Standard config / commands

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
| CORS | Browser clients |
| Adapter (Redis) | Multi-node rooms |
| Auth middleware | `socket.handshake` |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Connect loop | Version mismatch | Align major versions |
| Works single node only | Sticky/adapter | Redis adapter + sticky |
| CORS errors | Origin | Configure cors |
| Auth missing | Handshake | Middleware reject |

---

## Gotchas

> [!WARNING]
> **Socket.IO ≠ WS** — different protocol framing.

> [!WARNING]
> **Horizontal scale** — need pub/sub adapter.

---

## When NOT to use

- **Simple one-way server push** — SSE.
- **Binary media P2P** — WebRTC.
- **Standards-only WS clients** — `ws` library.

---

## Related

[[uWebSocket]] [[SSE (Server-Sent Events)]] [[express concepts]]
