[[Socket IO]] [[express concepts]] [[SSE (Server-Sent Events)]] [[expressjs]]

# uWebSocket

> µWebSockets.js is a high-performance Node WebSocket and HTTP server — lower overhead than Express plus `ws` for realtime fanout, with a different API and no Express middleware drop-in.





## Interview Relevance
Interviewers contrast “use Express for everything” with specialized servers: backpressure, native addons, and when Socket.IO features are worth the cost.

## Sources
- [uWebSockets.js — GitHub](https://github.com/uNetworking/uWebSockets.js) — deep-dive
- [uWebSockets — User manual](https://unetworking.github.io/uWebSockets/user_manual.html) — overview
- [MDN — WebSockets](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API) — overview

## Core Definition
`uWebSockets.js` exposes `uWS.App` / `uWS.SSLApp` with HTTP and WebSocket routes. It emphasizes throughput and backpressure (`getBufferedAmount`) and built-in topic pub/sub. It is not an Express-compatible middleware stack.

## Key Concepts
- **Backpressure:** watch buffered bytes; slow or disconnect slow consumers.
- **Topics:** lightweight pub/sub without an external adapter for single-process fanout.
- **Binary vs text:** `message` handlers receive `isBinary`.
- **Native addon:** install may need a toolchain or prebuilds — CI images matter.
- **API mismatch:** porting Express middleware requires deliberate redesign.

## Technical Details
```txt
uWS.App().ws('/ws', handlers).listen(port)
```

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
| Binary vs text | Check `isBinary` in the message handler |
| Native build | Toolchain or prebuilt binaries in CI |
| TLS | `uWS.SSLApp` with certificate paths |

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `npm install` fails | Native addon build | Toolchain or prebuilds |
| Express patterns fail | Different API | Port handlers deliberately |
| Memory growth | Slow consumers | Backpressure; disconnect slow clients |

## Real-World Applications
High-fanout tickers, game relays, and chat backends where Express+`ws` CPU or memory cost dominates.

**Example:** A market-data feed buffers gigabytes when clients stall — check `getBufferedAmount()` and unsubscribe or close sockets above a threshold.

## Pros/Cons or Trade-offs
- **Pro:** Excellent throughput and built-in pub/sub for single-node fanout.
- **Con:** Smaller ecosystem; no drop-in Helmet/Passport stack.
- **Con:** Multi-node still needs an external bus if processes do not share memory.

## Comparison
- vs [[Socket IO]]: Socket.IO adds rooms, fallbacks, and adapters; µWS is closer to raw WebSocket performance.
- vs Express + `ws`: familiar middleware vs specialized API — pick based on latency/CPU budget.
- vs [[SSE (Server-Sent Events)]]: SSE is one-way HTTP; µWS shines for bidirectional sockets.
- vs learning HTTP basics: start with [[express concepts]].

## Mistakes to Avoid
- Expecting Express middleware to mount unchanged.
- Ignoring backpressure until memory blows up.
- Assuming install works on every CI image without native build support.
- Choosing µWS for a CRUD app that needs the Express ecosystem.
