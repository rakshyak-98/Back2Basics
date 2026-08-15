[[backpressure]] [[Scaling Throughput in High-load system]] [[concurrent connection]] [[Latency]]

# Throughput

> Throughput is the rate of successful work completed per unit time — requests per second, transactions per second, megabits per second — while error rate and latency remain within service level objectives.

## Interview Relevance

Distinguish throughput vs latency; Little’s law intuition; find the bottleneck stage.

## Sources

- Neil Gunther, *Analyzing Computer System Performance with Perl::PDQ* — Little's Law application — overview
- Google SRE Book — capacity planning and load testing — deep-dive
- Brendan Gregg, *Systems Performance* — utilization and saturation analysis — overview

## Key Concepts

- **Rate of successful work:** ops/sec, bits/sec, jobs/sec — define the unit.
- **Not latency:** high throughput can coexist with bad p99.
- **Bottleneck stage:** pipeline rate equals the slowest stage.
- **Little’s law intuition:** concurrency ≈ throughput × latency.


## Technical Details

### Find the bottleneck layer

```txt
Network / load balancer → application workers → database / disk / GPU
     packets per second        requests per second         input/output operations per second
```

Peak requests per second with fifty percent errors is not useful throughput — measure **successful** completions.

**Little's Law:** `concurrency ≈ throughput × latency` — raising latency at fixed concurrency lowers effective throughput.

| Layer | Common choke |
|-------|--------------|
| Network | Packets per second, file descriptor limits, softirq |
| Application | Central processing unit, garbage collection, lock contention |
| Data store | Connection pool exhaustion, disk input/output, hot rows |
| External API | Partner rate limits |

## Measurement

```bash
# Example load generators
hey -z 30s -c 50 https://api.example.com/health
# vegeta, k6 — define success criteria (status, latency p99)
```

Pair load tests with `ss -s`, `pidstat`, database slow query logs, and traces — optimize the **slowest** stage first (Amdahl).

## Knobs that move throughput

| Knob | Effect |
|------|--------|
| Connection pool size | Too small → wait; too large → database stampede |
| Batching | Fewer round trips; may hurt tail latency |
| [[cache system]] | Cuts origin work |
| Async offload | Return `202 Accepted`; workers absorb ([[event-driven]]) |
| [[backpressure]] | Prevents overload collapse |

## Real-World Applications

Capacity planning, load tests, and SLO conversations about RPS vs latency.


## Pros/Cons or Trade-offs

- **Pro:** Clear capacity language for sizing.
- **Con:** Vanity throughput without success criteria (errors count).
- **Trade-off:** batching for throughput vs interactive latency.


## Comparison

- vs latency SLOs: complementary metrics.
- vs [[Scaling Throughput in High-load system]]: how to raise the number.


## Mistakes to Avoid

| Symptom | Likely cause |
|---------|--------------|
| Requests per second flat, low CPU | Pool or lock wait |
| Requests per second flat, high CPU | Hot code path or garbage collection |
| Good average, awful p99 | Tail saturation — shed load, quality of service tiers |
| Errors climb with load | Downstream timeout — circuit break |

*What breaks first when load doubles?* Usually the first shared resource without headroom — often the database connection pool.
