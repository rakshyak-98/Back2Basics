[[webhook]] [[webSocket]] [[HTTP module]] [[event-driven]]

# SSE (Server-Sent Events)

> One-way push from server to browser over plain HTTP — the server keeps a long-lived response open and writes `text/event-stream` events.

## Interview Relevance

Interviewers ask about SSE to see if you know when unidirectional server→client is enough, how reconnection and `Last-Event-ID` work, and why you would still pick [[webSocket]] for bidirectional or binary traffic.

## Sources

- [MDN — Server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events) — deep-dive
- [HTML Living Standard — Server-sent events](https://html.spec.whatwg.org/multipage/server-sent-events.html) — deep-dive
- [Wikipedia — Server-sent events](https://en.wikipedia.org/wiki/Server-sent_events) — overview

## Core Definition

Server-Sent Events (SSE) let a server push named text events to a browser (or any HTTP client) over a single long-lived HTTP response. The browser’s `EventSource` API auto-reconnects and can resume with `Last-Event-ID`.

## Key Concepts

- **Unidirectional:** server → client only → client still uses normal HTTP for sends.
- **`text/event-stream`:** lines like `data:`, `event:`, `id:` separated by blank lines.
- **Automatic reconnect:** `EventSource` retries on drop; send `id:` so the client can resume.
- **HTTP/1.1 connection limits:** browsers limit concurrent connections per origin → many SSE tabs can starve other requests (HTTP/2 helps).
- **Proxies / buffers:** intermediate buffers may delay events — disable response buffering for the stream.

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

Minimal Node-style response shape:

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

## Real-World Applications

Live dashboards, notification feeds, progress bars for long jobs, and stock/price tickers where the client mostly listens.

**Example:** A build page opens `EventSource("/jobs/123/events")` and appends log lines as the worker streams `data:` frames.

## Pros/Cons or Trade-offs

- **Pro:** Simple over HTTP, works with standard authentication cookies on same origin, auto-reconnect built in.
- **Con:** Text-oriented; not ideal for bidirectional or binary protocols.
- **Con:** Connection and proxy idle limits need operational care.

## Comparison

- vs [[webSocket]]: WebSocket is full-duplex and binary-friendly; SSE is simpler when only the server pushes text.
- vs long polling: SSE keeps one stream open instead of repeated request cycles.
- vs [[webhook]]: Webhooks notify *servers*; SSE notifies *browsers/clients*.

## Mistakes to Avoid

- Treating SSE as bidirectional — clients still need normal requests to send data.
- Forgetting heartbeats behind load balancers with short idle timeouts.
- Buffering the response in nginx/CDN layers so “realtime” becomes batchy.
