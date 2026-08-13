[[Throughput]] [[Token bucket]] [[race condition]] [[Scaling Throughput in High-load system]]

# backpressure

> Backpressure is the policy when a consumer cannot keep pace with a producer — block, queue with bounds, shed load, or reject — so unbounded buffers do not exhaust memory and cascade failure.

---

## Every link needs a policy

```txt
Producer → [bounded queue] → Consumer
               ↑ full?
         wait | drop | HTTP 429 / 503
```

Without an explicit policy, frameworks often buffer silently until the process runs out of memory or latency becomes unbounded.

| Strategy | Behavior | Risk |
|----------|----------|------|
| Blocking | Producer waits until space | Deadlock chains if circular |
| Bounded queue | Absorbs short bursts | Must define overflow action |
| Load shedding | Drop or sample | Data loss — metric and alert |
| Credit / window | Consumer grants send rights | Reactive streams, Transmission Control Protocol flow control |
| Rate limiting | [[Token bucket]] at gateway | Protects origin; clients need backoff |

## Application examples

Node.js streams respect backpressure:

```javascript
const ok = writable.write(chunk)
if (!ok) await once(writable, 'drain')
```

nginx rate limiting:

```nginx
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
limit_req zone=api burst=20 nodelay;
```

Message buses (Kafka, and others) use **consumer lag** as implicit backpressure — disk is still finite; alert and scale consumers or pause producers.

## Failure signatures

| Symptom | Likely cause |
|---------|--------------|
| Out of memory / huge lag | Unbounded in-memory queue |
| Upstream timeouts | Blocked producers waiting on full pipes |
| `429` storms | Clients retry without jitter |
| Silent message loss | Drop policy without dead-letter queue |

**Transmission Control Protocol backpressure is not application backpressure** — user-space code can still accumulate unbounded `Promise` chains (`Promise.all` on a million tasks is self-inflicted overload).

*What breaks first under spike?* The slowest stage in the pipeline — isolate thread pools and circuit-break sick dependencies.

## Sources

- Reactive Streams specification — `Publisher` / `Subscriber` backpressure contract.
- Google SRE Book — handling overload, graceful degradation.
- Martin Kleppmann, *Designing Data-Intensive Applications* — unbounded queues and system stability.
