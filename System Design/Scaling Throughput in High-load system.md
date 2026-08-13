[[System Design]] [[Throughput]] [[backpressure]] [[gRPC]] [[concurrent connection]]

# Scaling Throughput in High-load system

> High-load throughput — when REST-per-call and connection churn choke media/control planes, batch, async, and multiplex instead.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#When the API hits a wall]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Dense control planes (hundreds of channels/encoders) die on per-item HTTP and TLS handshakes. Bulk APIs, `202` + workers, and HTTP/2/gRPC reuse fix the shape of the work.

```txt
Bad:  300× PUT /channel/i   (SerDes + handshake tax)
Good: PUT /channels:batch   → queue → pre-warmed worker pool
```

| Lever | Effect |
|-------|--------|
| Batching | Fewer requests, one transaction |
| Async (`202`) | API not blocked on NVENC/GPU |
| gRPC / HTTP/2 | Multiplex; less churn |
| Pre-warmed pools | Avoid cold session open |

---

## Standard config / commands

```txt
POST /jobs  → 202 + job_id
GET  /jobs/{id}  → status
# Workers pull queue with bounded concurrency
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| CPU in handshake/TLS | Conn churn | Keepalive; gRPC; pool clients |
| API timeout, workers idle | Sync fan-out | 202 + queue |
| Encoder pool empty | Cold NVENC | Pre-warm; limit concurrency |
| Good average, bad p99 | Lock / GC | Profile; object reuse |
| Softirq storm | PPS | Batch packets; fewer short conns |

---

## When the API hits a wall

| Component | Metric | High-load signal |
|-----------|--------|------------------|
| NIC | PPS | Softirq CPU high |
| API | Context switches | Thread contention |
| GPU/encoder | Session open latency | Cold-start spike |
| Memory | GC | Per-request alloc churn |

---

## Gotchas

> [!WARNING]
> **Bulk endpoints without partial failure model** — define per-item errors.

> [!WARNING]
> **Unbounded queues** — async without [[backpressure]] just delays OOM.

> [!WARNING]
> **gRPC everywhere dogma** — public browsers may still need REST/JSON gateway.

---

## When NOT to use

- **Low QPS CRUD** — plain REST is fine.
- **Tiny payloads rare calls** — batching adds complexity for nothing.
- **Strict sync user UX that must finish in-request** — keep sync but optimize path.

---

## Related

[[Throughput]] [[backpressure]] [[concurrent connection]] [[Token bucket]] [[marshalling]]
