[[System Design]] [[stateless]] [[WebSocket]] [[SSE]] [[backpressure]]

# Real-time Subscription

> Real-time subscription — client stays connected (or long-polls) and receives pushes when data changes, instead of hammering polls.

## Mental model

**Say it in one breath:** Subscribe once; server pushes events. Transport choices: WebSocket, SSE, MQTT, GraphQL subscriptions.

```txt
Client ──subscribe(topic)──► Gateway ──► Pub/Sub / DB triggers
Client ◄──── event stream ──────────────┘
```

| Transport | Notes |
| --- | --- |
| **SSE** | HTTP one-way server→client; simple |
| **WebSocket** | Bidirectional |
| **Short poll** | Fallback; higher load |

## Standard config / commands

```js
const es = new EventSource('/events')
es.onmessage = (e) => apply(JSON.parse(e.data))

// WS
const ws = new WebSocket('wss://api/room/1')
ws.onmessage = (e) => apply(JSON.parse(e.data))
```

| Knob | Why |
| --- | --- |
| Heartbeat | Detect dead NATs |
| Last-Event-ID / cursor | Resume after reconnect ([[stateless]]) |
| Auth | Tickets/cookies on connect |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Connect then silence | Proxy buffering SSE | `X-Accel-Buffering: no`; disable buffer |
| Mobile drops | Idle NAT | Heartbeat ≤30–60s |
| Fan-out lag | Single process broadcast | Redis pub/sub / NATS |
| Dup events on resume | Cursor | Idempotent apply |
| Sticky session required | Local subscriber map | Shared bus |

## Gotchas

> [!WARNING]
> **LB without sticky + local state** — messages miss; externalize.

> [!WARNING]
> **SSE through old proxies** — transform/buffer breaks stream.

> [!WARNING]
> **Pushing huge payloads** — send ids; let client refetch.

## When NOT to use

- **Rare updates** — poll every few minutes is simpler.
- **One-shot request/response** — plain HTTP.
- **Million-viewer media** — CDN livestream, not per-user WS chat patterns.

## Related

[[stateless]] [[WebRTC]] [[backpressure]] [[event-driven]] [[Data fetching Frontend]]
