[[System Design]] [[Throughput]] [[backpressure]] [[TCP]]

# concurrent connection

> Concurrent connections — how many live sockets/sessions you hold at once; often the real limit before CPU is.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Each connection costs FDs, memory, and timer softirq. Throughput ≠ concurrency; long-lived streams burn concurrency without huge RPS.

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

---

## Standard config / commands

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

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `Too many open files` | `ulimit`; FD leak | Raise limit; fix leak |
| Accept drops | `ListenOverflows` | Raise somaxconn; faster accept |
| High conns, low RPS | Idle WS/SSE | Timeouts; scale horizontally |
| Ephemeral port exhaustion | Outbound APIs | Pools; more IPs; HTTP/2 |
| LB 502 under load | Backend conn cap | Raise upstream; warm pools |

---

## Gotchas

> [!WARNING]
> **Thread-per-conn** — dies at tens of thousands; use async/evented.

> [!WARNING]
> **Mobile networks** — ghost connections; heartbeat carefully.

> [!WARNING]
> **Counting LB vs app** — health checks inflate numbers.

---

## When NOT to use

- **Pure batch jobs** — connections short; optimize CPU/IO instead.
- **Serverless with tiny concurrency** — different scaling story.
- **One admin user** — ignore micro-tuning.

---

## Related

[[Throughput]] [[backpressure]] [[TCP]] [[Real-time Subscription]] [[Scaling Throughput in High-load system]]
