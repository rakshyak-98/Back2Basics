[[backpressure]] [[Throughput]] [[concurrent connection]] [[API design]]

# Token bucket

> A token bucket rate limiter refills tokens at a steady rate up to a burst capacity — each request spends tokens, and an empty bucket means throttle with HTTP 429 or delay.

---

## Algorithm

```txt
tokens = min(burst, tokens + rate × Δt)
if tokens >= cost:
    tokens -= cost
    allow
else:
    deny or queue
```

| Parameter | Meaning |
|-----------|---------|
| `rate` | Sustained requests per second (refill speed) |
| `burst` | Maximum tokens (allowed spike) |
| `cost` | Tokens per request (batch or GraphQL queries may cost > 1) |
| Key | Client Internet Protocol, user identifier, API key |

Short spikes are allowed up to **burst**; sustained traffic is capped at **rate** — smoother than naive fixed windows.

## Compared to other limiters

| Algorithm | Behavior |
|-----------|----------|
| **Token bucket** | Allows bursts; smooth average |
| **Leaky bucket** | Steady outflow; harder peak shaping |
| **Fixed window** | Simple counter per minute; double burst at window edge |
| **Sliding window** | Smoother than fixed; more state |

nginx `limit_req` with `burst` approximates token bucket behavior:

```nginx
limit_req_zone $binary_remote_addr zone=one:10m rate=5r/s;
limit_req zone=one burst=20 nodelay;
```

Distributed deployments should store bucket state in **Redis** (or similar) — per-process buckets let clients rotate across pods and exceed quota.

## Operations

| Symptom | Direction |
|---------|-----------|
| Legitimate users throttled | Burst too low; many users behind carrier-grade NAT — key by authenticated user |
| Limit ineffective | Per-node buckets — centralize |
| Clock jump | Use monotonic time; clamp Δt |
| Clients hammer after 429 | Document exponential backoff with jitter |

Return **429 Too Many Requests** (or 503 with `Retry-After`) — silent drops confuse clients.

Token buckets limit **admission rate**; for **in-flight concurrency** caps use semaphores or connection pools ([[concurrent connection]]).

## Sources

- [RFC 6585](https://www.rfc-editor.org/rfc/rfc6585) — 429 status code.
- Tanenbaum, *Computer Networks* — traffic shaping fundamentals.
- Redis rate limiting patterns — Lua scripts for atomic token decrement.
