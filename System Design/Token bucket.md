[[backpressure]] [[Throughput]] [[concurrent connection]] [[API design]]

# Token bucket

> A token bucket rate limiter refills tokens at a steady rate up to a burst capacity — spend tokens per request; empty bucket means throttle (429) or delay.

```txt
        Token bucket ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Explain rate vs burst, compare to fixed/sliding windows, and why distributed …

## Sources
- [RFC 6585](https://www.rfc-editor.org/rfc/rfc6585) — 429 status code — overview
- Tanenbaum, *Computer Networks* — traffic shaping — overview
- Redis rate-limiting patterns (atomic Lua) — deep-dive

## Key Concepts
- **rate:** sustained refill (req/s).
- **burst:** max tokens (allowed spike).
- **cost:** tokens per request (GraphQL may cost > 1).
- **key:** IP, user id, API key.

## Technical Details
```txt
tokens = min(burst, tokens + rate × Δt)
if tokens >= cost:
    tokens -= cost
    allow
else:
    deny or queue
```

| Algorithm | Behavior |
|-----------|----------|
| **Token bucket** | Allows bursts; smooth average |
| **Leaky bucket** | Steady outflow |
| **Fixed window** | Simple; double-burst at edges |
| **Sliding window** | Smoother; more state |

```nginx
limit_req_zone $binary_remote_addr zone=one:10m rate=5r/s;
limit_req zone=one burst=20 nodelay;
```

- Distributed: store buckets in Redis
- Use monotonic time; clamp Δt on clock jumps.

- Token buckets limit **admission rate**
- Pair with [[backpressure]] and [[API design]] docs.

## Mistakes to Avoid
- **Mistake:** Per-pod buckets in Kubernetes (limit bypass)
- **Mistake:** Silent drops instead of 429 + `Retry-After`
- **Mistake:** Keying only by IP behind carrier-grade NAT

## Pros/Cons or Trade-offs
- **Pro:** Allows short bursts without abandoning a sustained cap.
- **Con:** Needs careful keying (CGNAT) and shared state in fleets.
- **Trade-off:** burst comfort vs abuse headroom.

## Comparison
- vs leaky bucket: burst-friendly vs steady outflow.
- vs concurrency limits: rate over time vs simultaneous in-flight.


### Use cases
- Public API gateways, nginx `limit_req`, and SaaS per-tenant quotas.
