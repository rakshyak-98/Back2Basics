[[System Design]] [[Latency]] [[backpressure]] [[Scaling Throughput in High-load system]]

# Throughput

> Throughput — how much successful work per time (RPS, TPS, Mbps) while latency and errors stay acceptable.

---

## Mental model

**Say it in one breath:** Capacity under load. Raise throughput by removing the bottleneck layer — not by guessing.

```txt
NIC / LB  →  app workers  →  DB / disk / GPU
  PPS          RPS              IOPS / sessions
```

| Layer | Metric | Typical choke |
|-------|--------|---------------|
| Network | PPS, bandwidth | Softirq, fd limits |
| App | RPS, CPU | SerDes, locks, GC |
| I/O | DB QPS, queue depth | Connections, disk |

Little’s Law: `concurrency ≈ throughput × latency`.

---

## Standard config / commands

```bash
# Rough load signal
hey -z 30s -c 50 https://api/… 
# or vegeta, k6
ss -s
pidstat -u 1
```

| Knob | Effect |
|------|--------|
| Pool sizes | Too small → wait; too big → stampede |
| Batching | Fewer round-trips |
| Caching | Cut origin work |
| Async offload | API returns 202; workers absorb |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| RPS flat, CPU low | Lock / pool wait | Find blocker; raise pool carefully |
| RPS flat, CPU high | Hot code / GC | Profile; reduce allocs |
| Good RPS, awful p99 | Tail saturation | QoS; shed load; cache |
| Errors climb with load | Dependency timeout | Backpressure; bulkhead |
| Softirq high | PPS storm | Batching; kernel tune; fewer conns |

---

## Gotchas

> [!WARNING]
> **Peak RPS with 50% errors is not throughput** — count *successful* work.

> [!WARNING]
> **Optimizing non-bottleneck** — measure first.

> [!WARNING]
> **Latency vs throughput trade** — batching helps RPS, can hurt p99.

---

## When NOT to use

- **Ultra-low QPS admin tools** — optimize clarity, not RPS.
- **One-shot batch jobs** — wall-clock & cost matter more than RPS.
- **Comparing Mbps across compressions** — normalize payload.

---

## Related

[[Scaling Throughput in High-load system]] [[backpressure]] [[concurrent connection]] [[Token bucket]]
