[[ExpressJS]] [[Socket IO]] [[express concepts]]

# uWebSocket

> µWebSockets.js — high-performance Node WebSocket/HTTP library; lower-level and faster than Express+ws for realtime fanout.

## Mental model

**Say it in one breath:** Native-ish performance server for WS/HTTP. Different API from Express—don’t expect middleware ecosystem drop-in.

```txt
uWS.App().ws('/ws', handlers).listen(port)
```

## Standard config / commands

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

| Knob | Why it matters |

| Backpressure | `getBufferedAmount` |
| --- | --- |
| SSL app | `uWS.SSLApp` |
| Pub/sub topics | Built-in topic broadcast |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Install fail | Native build | Toolchain/prebuilds |
| Express habits fail | Different API | Port handlers deliberately |
| Memory growth | Slow consumers | Backpressure; drop |

## Gotchas

> [!WARNING]
> **Not Express middleware compatible** out of the box.

> [!WARNING]
> **Binary vs string** — check `isBinary`.

## When NOT to use

- **CRUD apps with big middleware needs** — Express/Fastify.
- **Socket.IO features (rooms fallbacks)** — Socket.IO.
- **Beginners learning HTTP** — Express first.

## Related

[[Socket IO]] [[express concepts]] [[SSE (Server-Sent Events)]]
