[[System Design]] [[Throughput]] [[backpressure]] [[TCP]]

# concurrent connection

> Concurrent connections — how many live sockets/sessions you hold at once; often the real limit before CPU is.

```txt
        concurrent connect ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** FD/socket limits, keepalives, and why connection count ≠ request concurrency.

## Sources
- [Wikipedia — concurrent connection](https://en.wikipedia.org/wiki/concurrent_connection) — overview

## Key Concepts
- **Live sockets/sessions:** distinct from requests per second.
- **Resource caps:** FDs, memory per conn, LB limits.
- **Keepalive vs churn:** reuse cuts handshakes; idle still costs RAM.
- **App vs protocol limits:** configure both.

## Technical Details
### How it works

```txt
clients ══╗
          ╠══ LB ── workers (ulimit, event loop)
clients ══╝
```

| Limit | Where |
|-------|--------|
| `ulimit -n` | Process FDs |
| `somaxconn` | Accept queue |
| Worker count | App server |
| NAT ports | Client side |


### Configuration and commands

```bash
ss -s
ss -tan state established | wc -l
ulimit -n
sysctl net.core.somaxconn
```

| Knob | Why |
|------|-----|
| Keep-alive | Fewer handshakes; more idle conns |
| HTTP/2 multiplex | Many streams / one conn |
| Idle timeout | Reap dead mobiles |

## Mistakes to Avoid
> [!WARNING]
> **Thread-per-conn** — dies at tens of thousands; use async/evented.

> [!WARNING]
> **Mobile networks** — ghost connections; heartbeat carefully.

> [!WARNING]
> **Counting LB vs app** — health checks inflate numbers.

---

| Symptom | Check | Fix |
|---------|-------|-----|
| `Too many open files` | `ulimit`; FD leak | Raise limit; fix leak |
| Accept drops | `ListenOverflows` | Raise somaxconn; faster accept |
| High conns, low RPS | Idle WS/SSE | Timeouts; scale horizontally |
| Ephemeral port exhaustion | Outbound APIs | Pools; more IPs; HTTP/2 |
| LB 502 under load | Backend conn cap | Raise upstream; warm pools |

---

## Pros/Cons or Trade-offs
- **Pure batch jobs** — connections short; optimize CPU/IO instead.
- **Serverless with tiny concurrency** — different scaling story.
- **One administrator user** — ignore micro-tuning.

---


- **Pro:** Models real resource pressure for long-lived clients.
- **Con:** Easy to confuse with throughput.
- **Trade-off:** many idle conns vs short-lived request/response.

## Comparison
- vs [[Throughput]]: connections are concurrency capacity; throughput is completion rate.
- vs [[server]]: servers must accept and account for connection lifecycle.


### Use cases
- WebSocket fleets, reverse proxies, and API gateways under C10k-style load.
