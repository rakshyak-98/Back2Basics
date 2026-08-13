<!-- note-strategy: operational -->
[[Networking]] [[TCP]] [[UDP]] [[webSocket]] [[P2P (Peer-to-Peer)]]

# Data transfer communication channels

> Pick the channel that matches the job — request/response, push, queue, or peer media — not one protocol for everything.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Channels differ by who starts, whether they stay open, and where the data lives (wire, broker, or shared memory).

```txt
Same machine          Across network
─────────────         ────────────────
pipes / shm    →      HTTP / gRPC / WS
Unix sockets   →      queues / WebRTC / FTP
```

### Interview map (words you can say)

| Channel | Plain job | Say in interview |
|---------|-----------|------------------|
| **HTTP/HTTPS** | Request/response over the web | “Default for APIs; add auth and TLS.” |
| **WebSocket** | Long-lived bidirectional bytes | “Push without polling; still one TCP.” |
| **SSE** | Server → browser event stream | “Simpler than WS when client only listens.” |
| **gRPC / RPC** | Call a remote function | “Typed contracts; great service-to-service.” |
| **Message queue** | Async handoff via broker | “Decouple producer and consumer.” |
| **WebRTC** | P2P A/V + data after ICE | “Low latency media; NAT traversal required.” |
| **Pipes / Unix socket** | Local IPC | “Fastest same-host path; no internet.” |
| **SFTP/SCP** | Bulk file copy | “Batch transfer, not chatty APIs.” |

### Decision cheat sheet

| Need | Prefer |
|------|--------|
| CRUD API / browsers | HTTPS |
| Live UI updates | WebSocket or SSE |
| Work fan-out / buffer | Queue (Kafka/SQS/…) |
| Same-host speed | Unix domain socket / shm |
| Browser P2P media | WebRTC |
| Big file drop | Object storage + HTTPS, or SFTP |

---

## Standard config / commands

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

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| “Real-time” feels polled | Using HTTP GET loops | Switch to WS/SSE or push via queue→WS |
| Lost messages under load | No broker / no ack | Introduce a queue; don’t rely on one TCP |
| Browser can’t P2P | ICE/TURN missing | See [[ICE (Interactive Connectivity Establishment)]] |
| Fast locally, dead remote | Bound to localhost / wrong channel | Expose HTTPS or Unix→TCP carefully |
| Huge payloads over WS | Wrong tool | Object store + URL; keep WS for control |

---

## Gotchas

> [!WARNING]
> **HTTP is not a queue** — retries and fan-out need a broker or you lose work on crash.

> [!WARNING]
> **WebSocket ≠ WebRTC** — WS is client↔server TCP; WebRTC is peer media over ICE/UDP.

> [!WARNING]
> **Shared memory doesn’t cross machines** — scale-out forces a network channel.

---

## When NOT to use

- **One golden hammer** — don’t put file sync, RPC, and chat all on raw WebSockets.
- **Email as a data bus** — high latency; use queues for systems, email for humans.
- **Bluetooth for datacenter backends** — short-range IoT only.

---

## Related

[[Networking]] [[TCP]] [[UDP]] [[webSocket]] [[P2P (Peer-to-Peer)]] [[ICE (Interactive Connectivity Establishment)]] [[half-open connections]]
