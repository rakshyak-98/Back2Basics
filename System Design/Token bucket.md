[[System Design]] [[backpressure]] [[Throughput]] [[race condition]]

# Token bucket

> Token bucket — rate limiter: tokens refill over time; each request spends a token; empty bucket ⇒ throttle.

---

## Mental model

**Say it in one breath:** Bucket holds up to `burst` tokens; refill at `rate`. Smooths traffic while allowing short spikes.

```txt
tokens = min(burst, tokens + rate*dt)
if tokens >= cost: tokens -= cost; allow
else: deny / delay
```

| Vs | Difference |
|----|------------|
| Leaky bucket | Steady outflow; shapes harder |
| Fixed window | Cheap; boundary burst double-spend |
| Sliding window | Smoother; more state |

---

## Standard config / commands

```js
// Redis + Lua sketch keys: tokens, timestamp
// INCR/EXPIRE naive counters are fixed-window — prefer true bucket script
```

```nginx
limit_req_zone $binary_remote_addr zone=one:10m rate=5r/s;
# burst=… approximates token bucket behavior
```

| Knob | Meaning |
|------|---------|
| `rate` | Sustained RPS |
| `burst` | Peak tokens |
| Key | IP / user / API key |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Legit users `429` | Burst too low; shared NAT IP | Raise burst; key by user id |
| Throttle ineffective | Multi-instance local buckets | Central Redis bucket |
| Spiky allow at window edge | Fixed window bug | Sliding or token bucket |
| Clock jump | Bad `dt` | Monotonic time; clamp dt |
| Cost≠1 requests | GraphQL/batch | Weighted tokens |

---

## Gotchas

> [!WARNING]
> **Per-node buckets** — users bypass by hashing across pods; centralize.

> [!WARNING]
> **Silent drop vs `429`** — APIs should signal clients to back off.

> [!WARNING]
> **Refill math in floats** — use integer millis tokens.

---

## When NOT to use

- **Hard concurrency caps** — use semaphores/pools (in-flight limits).
- **Fair multi-tenant complex quotas** — may need hierarchical/fair queuing.
- **One-shot admin scripts** — don’t rate-limit yourself into pain.

---

## Related

[[backpressure]] [[Throughput]] [[concurrent connection]] [[Scaling Throughput in High-load system]]
