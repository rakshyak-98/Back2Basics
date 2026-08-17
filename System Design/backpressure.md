[[Throughput]] [[Token bucket]] [[race condition]] [[Scaling Throughput in High-load system]]

# backpressure

> Backpressure is the policy when a consumer cannot keep pace with a producer — block, bound the queue, shed load, or reject — so buffers do not exhaust memory and cascade failure.

```txt
        backpressure ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Name an explicit overflow policy for every stage

## Sources
- Reactive Streams specification — backpressure contract — deep-dive
- Google SRE Book — overload and graceful degradation — deep-dive
- Martin Kleppmann, *Designing Data-Intensive Applications* — unbounded queues — deep-dive

## Key Concepts
- **Every link needs a policy:** wait, drop, 429/503, or credit/window.
- **Bounded queues:** absorb bursts; define overflow.
- **Load shedding:** intentional loss — metric and alert.
- **Rate limiting:** [[Token bucket]] at the edge.

## Technical Details
```txt
Producer → [bounded queue] → Consumer
               ↑ full?
         wait | drop | HTTP 429 / 503
```

| Strategy | Behavior | Risk |
|----------|----------|------|
| Blocking | Producer waits | Deadlock if circular |
| Bounded queue | Absorbs short bursts | Need overflow action |
| Load shedding | Drop or sample | Data loss |
| Credit / window | Consumer grants send rights | Reactive streams, TCP |
| Rate limiting | [[Token bucket]] | Clients need backoff |

```javascript
const ok = writable.write(chunk)
if (!ok) await once(writable, 'drain')
```

```nginx
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
limit_req zone=api burst=20 nodelay;
```

- Kafka consumer lag is implicit backpressure — disk is still finite.
- **TCP backpressure ≠ app backpressure:** 

| Symptom | Likely cause |
|---------|--------------|
| OOM / huge lag | Unbounded in-memory queue |
| Upstream timeouts | Blocked producers on full pipes |
| 429 storms | Retries without jitter |
| Silent loss | Drop without dead-letter |

## Mistakes to Avoid
- **Mistake:** Unbounded queues “for reliability.”
- **Mistake:** Dropping without metrics/DLQ
- **Mistake:** Assuming the kernel socket buffer saves the application

## Pros/Cons or Trade-offs
- **Block:** preserves data; can deadlock/timeout upstream.
- **Shed:** protects the system; loses work.
- **Trade-off:** latency SLOs vs completeness SLOs.

## Comparison
- vs [[Token bucket]]: admission shaping vs full-pipeline consumer pressure.
- vs infinite buffer: “never block” until memory death.


### Use cases
- Stream processors, API gateways, Node streams, and any pipeline in [[Scaling …
