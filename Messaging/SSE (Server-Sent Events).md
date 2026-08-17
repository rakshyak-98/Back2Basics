[[webhook]] [[webSocket]] [[HTTP module]] [[event-driven]]

# SSE (Server-Sent Events)

> One-way push from server to browser over plain HTTP — the server keeps a long-lived response open and writes `text/event-stream` events.

```txt
        SSE (Server-Sent E ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers ask about SSE to see if you know when unidirectional server→clie…

## Sources
- [MDN — Server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events) — deep-dive
- [HTML Living Standard — Server-sent events](https://html.spec.whatwg.org/multipage/server-sent-events.html) — deep-dive
- [Wikipedia — Server-sent events](https://en.wikipedia.org/wiki/Server-sent_events) — overview

## Key Concepts
- **Unidirectional:** server → client only → client still uses normal HTTP for sends.
- **`text/event-stream`:** lines like `data:`, `event:`, `id:` separated by blank lines.
- **Automatic reconnect:** `EventSource` retries on drop; send `id:` so the client can resume.
- **HTTP/1.1 connection limits:** browsers limit concurrent connections per origin → many SSE tabs can starve o…
- **Proxies / buffers:** intermediate buffers may delay events


- **Core:** Server-Sent Events (SSE) let a server push named text events to a browser (or…

## Technical Details
```
Browser                         Server
  │  GET /events (Accept: text/event-stream)
  ├────────────────────────────►│
  │◄════ event-stream (chunked) ═╡  data: {"t":1}\n\n
  │                             │  id: 42\n data: …\n\n
  │  (disconnect)               │
  │  GET … Last-Event-ID: 42    │
  ├────────────────────────────►│  resume
```

- Minimal Node-style response shape:

```http
HTTP/1.1 200 OK
Content-Type: text/event-stream
Cache-Control: no-cache
Connection: keep-alive

id: 1
data: {"status":"ok"}

```

```js
const es = new EventSource("/events");
es.onmessage = (e) => console.log(JSON.parse(e.data));
es.addEventListener("ready", (e) => { /* named event */ });
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Events arrive in bursts | Proxy buffering | `X-Accel-Buffering: no` / disable buffer |
| Stale connection | Idle timeouts | Comment heartbeats (`: ping`) periodically |
| Too many hanging sockets | Per-origin limit | Multiplex; prefer HTTP/2; fall back to poll |
| Cannot send from client | Wrong tool | Use POST APIs or [[webSocket]] |

## Mistakes to Avoid
- **Mistake:** Treating SSE as bidirectional
- **Mistake:** Forgetting heartbeats behind load balancers with short idle time…
- **Mistake:** Buffering the response in nginx/CDN layers so “realtime” becomes…

## Pros/Cons or Trade-offs
- **Pro:** Simple over HTTP, works with standard authentication cookies on same origin, auto-reconnect built in.
- **Con:** Text-oriented; not ideal for bidirectional or binary protocols.
- **Con:** Connection and proxy idle limits need operational care.

## Comparison
- vs [[webSocket]]: WebSocket is full-duplex and binary-friendly
- vs long polling: SSE keeps one stream open instead of repeated request cycles.
- vs [[webhook]]: Webhooks notify *servers*; SSE notifies *browsers/clients*.


### Use cases
- Live dashboards, notification feeds, progress bars for long jobs, and stock/p…

- **Example:** A build page opens `EventSource("/jobs/123/events")` and appends…
