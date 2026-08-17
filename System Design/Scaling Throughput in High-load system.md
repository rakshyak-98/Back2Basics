[[Throughput]] [[backpressure]] [[gRPC]] [[concurrent connection]] [[API design]]

# Scaling Throughput in High-load system

> High-load throughput optimization removes per-request overhead — batching, asynchronous job queues, connection multiplexing, and warm pools — when REST-per-call and connection churn saturate the control plane.

```txt
        Scaling Throughput ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Remove per-request overhead: pooling, batching, caching, async

## Sources
- Google gRPC performance guide — channel reuse, streaming — overview
- Netflix/conversational engineering blogs — asynchronous job APIs for media pipelines — overview
- Brendan Gregg, *Systems Performance* — identifying saturation — overview

## Key Concepts
- **Remove per-request overhead:** pools, reuse, batching, caching first.
- **Find the bottleneck stage:** CPU, disk, lock, or downstream RTT.
- **Async offload:** move non-critical work off the request path.
- **Measure:** p99 and saturation before buying horizontal scale.

## Technical Details
### The API wall

```txt
Poor:  300× PUT /channel/{i}   (serialization + Transport Layer Security handshake tax)
Better: PUT /channels:batch   → queue → pre-warmed worker pool
```

| Lever | Effect |
|-------|--------|
| Batching | Fewer round trips; one transaction boundary |
| Asynchronous `202 Accepted` | Application programming interface not blocked on GPU encode |
| HTTP/2 / [[gRPC]] | Multiplex streams; less connection churn |
| Pre-warmed pools | Avoid cold encoder or database session open |
| [[Token bucket]] admission | Protect downstream from overload |

### Asynchronous job pattern

```txt
POST /jobs → 202 + job_id
GET  /jobs/{id} → status (queued, running, failed, complete)

Workers pull queue with bounded concurrency ([[backpressure]])
```

- Clients poll or subscribe ([[Real-time Subscription]]) for completion

### Connection and protocol tuning

| Symptom | Direction |
|---------|-----------|
| Central processing unit in handshake | Keep-alive; reuse gRPC channels; connection pool |
| Application programming interface timeout, workers idle | Synchronous fan-out — move to queue |
| Good average, bad p99 | Lock contention, garbage collection — profile |
| Softirq storm | Batch packets; fewer short-lived connections ([[concurrent connection]]) |

## Mistakes to Avoid
- **Mistake:** Skipping failure modes until production
- **Mistake:** Ignoring idempotency, timeouts, or rollback where required
- **Mistake:** Optimizing or distributing before measuring the real bottleneck

## Pros/Cons or Trade-offs
Low queries-per-second create-read-update-delete does not need batch endpoints. Strict synchronous user experience (payment confirmation) may require optimized synchronous path, not `202`.

Public browser clients may still need REST or JSON gateway even when internal east-west traffic uses gRPC.

*What breaks first at ten times load?* Unbounded job queue without [[backpressure]] — memory exhaustion delayed, not prevented.


- **Pro:** Multiplicative gains without new machines.
- **Con:** Premature optimization of the wrong stage.
- **Trade-off:** throughput vs latency when batching.

## Comparison
- vs [[Throughput]]: metric definition vs how to raise it under load.
- vs [[Horizontal vs Vertical Scaling]]: optimize before/while scaling out.


### Use cases
- High-QPS APIs, ad/telemetry ingest, and checkout spikes.
