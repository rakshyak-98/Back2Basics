[[stateless]] [[webSocket]] [[backpressure]] [[event-driven]] [[Food delivery]]

# Real-time Subscription

> Real-time subscription keeps a channel open (or long-polls) so the server pushes updates when data changes — replacing wasteful polling for live dashboards, chat, and order status.

---

## Transport options

```txt
Client ──subscribe(topic)──► Gateway ──► Pub/Sub / database triggers
Client ◄──── event stream ──────────────┘
```

| Transport | Direction | Notes |
|-----------|-----------|-------|
| Server-Sent Events | Server → client | Simple over HTTP; one-way |
| WebSocket | Bidirectional | Lower overhead for chat and games |
| Long poll | Fallback | Higher load; works through strict proxies |
| Push notification | Mobile background | Apple Push Notification service / Firebase Cloud Messaging |

## Client patterns

```javascript
const es = new EventSource('/events')
es.onmessage = (e) => apply(JSON.parse(e.data))

const ws = new WebSocket('wss://api.example.com/room/1')
ws.onmessage = (e) => apply(JSON.parse(e.data))
```

| Knob | Why |
|------|-----|
| Heartbeat every 30–60s | Detect dead network address translation |
| `Last-Event-ID` / cursor | Resume after reconnect ([[stateless]]) |
| Auth on connect | Short-lived ticket or cookie |
| Small payloads | Send identifiers; client refetches details |

## Scaling fan-out

Single-process broadcast does not scale — use Redis pub/sub, NATS, or Kafka consumer → gateway pattern. Gateway instances remain [[stateless]] if subscription routing uses shared bus.

Apply [[backpressure]] when slow clients cannot read — drop or disconnect to protect others.

## Failure signatures

| Symptom | Direction |
|---------|-----------|
| Connect then silence | Proxy buffering Server-Sent Events — `X-Accel-Buffering: no` |
| Mobile drops | Heartbeat too slow |
| Duplicate events on resume | Idempotent apply by event identifier |
| Missed messages without sticky sessions | Local subscriber map — externalize |

Order tracking in [[Food delivery]] and live sports scores are typical subscription workloads — pair with idempotent state application.

## Sources

- [HTML Living Standard — Server-sent events](https://html.spec.whatwg.org/multipage/server-sent-events.html).
- [RFC 6455](https://www.rfc-editor.org/rfc/rfc6455) — WebSocket Protocol.
- Martin Kleppmann, *Designing Data-Intensive Applications* — publish/subscribe.
