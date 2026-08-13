[[ExpressJS]] [[Socket IO]] [[express concepts]] [[SSE (Server-Sent Events)]]

# uWebSocket

> µWebSockets.js is a high-performance Node WebSocket and HTTP server — lower overhead than Express plus `ws` for realtime fanout, with a different API and no Express middleware drop-in.

---

## API shape

```txt
uWS.App().ws('/ws', handlers).listen(port)
```

Backpressure via `getBufferedAmount`, built-in topic pub/sub, and `uWS.SSLApp` for TLS. Not compatible with Express middleware out of the box.

---

## Example

```js
import uWS from 'uWebSockets.js'
uWS.App()
  .ws('/ws', {
    open: (ws) => ws.send('hi'),
    message: (ws, message, isBinary) => ws.send(message, isBinary),
  })
  .listen(9001, (token) => {
    if (!token) throw new Error('bind failed')
  })
```

| Concern | Practice |
|---------|----------|
| Backpressure | Monitor `getBufferedAmount`; drop or slow producers |
| Binary vs text | Check `isBinary` in message handler |
| Native build | Install may require toolchain or prebuilds |

---

## What breaks first

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `npm install` fails | Native addon build | Toolchain or prebuilt binaries |
| Express patterns fail | Different API | Port handlers deliberately |
| Memory growth | Slow consumers | Backpressure; disconnect slow clients |

---

## When µWebSockets is a poor fit

- CRUD apps needing a large middleware ecosystem — Express or Fastify.
- Socket.IO features (rooms, fallbacks) — use [[Socket IO]].
- Learning HTTP basics — start with [[express concepts]].

---

## Related

[[Socket IO]] · [[express concepts]] · [[SSE (Server-Sent Events)]]
