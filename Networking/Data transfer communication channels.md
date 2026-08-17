[[Networking]] [[TCP]] [[UDP]] [[webSocket]] [[P2P (Peer-to-Peer)]] [[ICE (Interactive Connectivity Establishment)]] [[half-open connections]]

# Data transfer communication channels

> Pick the channel that matches the job — request/response, push, queue, or peer media — not one protocol for everything.





## Interview Relevance
Interviewers ask which channel you would pick (HTTP, WebSocket, queue, WebRTC, Unix socket) to see if you match protocol to job — latency, fan-out, browser constraints, and failure modes — instead of one golden hammer.

## Sources
- [RFC 6455 — The WebSocket Protocol](https://www.rfc-editor.org/rfc/rfc6455) — overview
- [RFC 9110 — HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110) — overview
- [MDN — Web APIs / WebSocket](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API) — overview
- [Wikipedia — Inter-process communication](https://en.wikipedia.org/wiki/Inter-process_communication) — overview

## Key Concepts
- **HTTP/HTTPS:** request/response over the web → default for APIs; add auth and TLS.
- **WebSocket:** long-lived bidirectional frames → push without polling; still one TCP.
- **SSE:** server → browser event stream → simpler when the client only listens.
- **gRPC / RPC:** call a remote function → typed contracts for service-to-service.
- **Message queue:** async handoff via broker → decouple producer and consumer.
- **WebRTC:** P2P A/V + data after ICE → low-latency media; NAT traversal required.
- **Pipes / Unix socket:** local IPC → fastest same-host path; no internet.
- **SFTP/SCP / object store:** bulk file copy → batch transfer, not chatty APIs.

## Technical Details
```txt
Same machine          Across network
─────────────         ────────────────
pipes / shm    →      HTTP / gRPC / WS
Unix sockets   →      queues / WebRTC / FTP
```

| Need | Prefer |
|------|--------|
| CRUD API / browsers | HTTPS |
| Live UI updates | WebSocket or SSE |
| Work fan-out / buffer | Queue (Kafka/SQS/…) |
| Same-host speed | Unix domain socket / shm |
| Browser P2P media | WebRTC |
| Big file drop | Object storage + HTTPS, or SFTP |

```bash
# Is something listening?
ss -tlnp | head

# HTTP quick check
curl -sS -o /dev/null -w '%{http_code}\n' https://example.com/

# WebSocket smoke (if wscat installed)
# wscat -c wss://example.com/ws

# Local IPC: Unix socket
ss -xlnp | grep my.sock
```

| Knob | Why it matters |
|------|----------------|
| TLS termination | Encrypt on the wire; pin ciphers at LB |
| Timeouts / keepalives | Idle channels die without heartbeats |
| Backpressure | Queues and WS need size limits |
| Authn on upgrade | WS/SSE must check cookies/JWT at handshake |

| Symptom | Check | Fix |
|---------|-------|-----|
| “Real-time” feels polled | Using HTTP GET loops | Switch to WS/SSE or push via queue→WS |
| Lost messages under load | No broker / no ack | Introduce a queue; don’t rely on one TCP |
| Browser can’t P2P | ICE/TURN missing | See [[ICE (Interactive Connectivity Establishment)]] |
| Fast locally, dead remote | Bound to localhost / wrong channel | Expose HTTPS or Unix→TCP carefully |
| Huge payloads over WS | Wrong tool | Object store + URL; keep WS for control |

## Real-World Applications
APIs, live dashboards, async workers, and media calls each need a different channel.

**Example:** A dashboard polls every second over HTTPS and feels laggy — move live updates to WebSocket or SSE, and keep CRUD on HTTP.

## Pros/Cons or Trade-offs
- **Pro:** Matching channel to job cuts latency, cost, and operational complexity.
- **Con:** Each channel adds its own auth, timeout, and backpressure rules.
- **Con:** Mixing too many transports without need multiplies debugging surface.

## Comparison
- vs HTTP as a queue: HTTP retries alone do not replace a broker for durable fan-out.
- vs [[webSocket]] vs WebRTC: WS is client↔server TCP; WebRTC is peer media over ICE/UDP.
- vs shared memory: shm does not cross machines — scale-out forces a network channel.

## Mistakes to Avoid
- One golden hammer — don’t put file sync, RPC, and chat all on raw WebSockets.
- Treating HTTP as a durable work queue — crash mid-retry loses work without a broker.
- Confusing WebSocket with WebRTC.
- Using email or Bluetooth as a datacenter data bus.
