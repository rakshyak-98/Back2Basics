[[SOLID]] [[API design]] [[Distributed computing]] [[Horizontal vs Vertical Scaling]] [[cache system]]

# System design

> System design is the practice of shaping software so requirements (scale, reliability, cost) are met while keeping boundaries clear enough that implementation can change without rewriting the product.

```txt
        System design ──┬── Interview
               ├── Sources
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Clarify requirements, data path, coordination, failure, and operability

## Sources
- Martin Kleppmann, *Designing Data-Intensive Applications* (O'Reilly, 2017) — replication, partitioning, consistency — deep-dive
- Google SRE Book — reliability targets, capacity planning, incident response — deep-dive
- AWS Well-Architected Framework — operational excellence, reliability, performance efficiency — overview

## Technical Details
### What system design is asking

- Whether in an interview or a production review, the same questions recur:

| Question | What a good answer names |
|----------|--------------------------|
| Who uses it and how often? | Read/write ratio, peak queries per second, geographic spread |
| What must never be lost? | Durability, backup, replication |
| What can be briefly wrong? | Consistency trade-offs ([[Eventual consistency]]) |
| What fails first? | Single host, zone, region, dependency |
| How do you know it is healthy? | Metrics, traces, synthetic checks |

- System design is not drawing boxes for its own sake.
- Every component should map to a requirement or a failure mode you are mitigat…

### A practical design loop

1. **Clarify scope** — functional requirements, scale targets, latency budget, consistency needs.
2. **Sketch the data path** — who writes, who reads, where state lives ([[database sharding]], [[cache system]]).
3. **Identify coordination** — single leader, [[Quorum]], or fully independent replicas ([[Raft]] when you need a replicated log).
4. **Plan for failure** — timeouts, retries with jitter, idempotent handlers, [[backpressure]].
5. **Make it operable** — dashboards, runbooks, capacity headroom before launch.

### Scaling path (typical order)

- Most products grow through a predictable sequence

```txt
Single service + single database
  → read replicas + caching
  → vertical scaling (bigger machine)
  → horizontal scaling (more stateless replicas)
  → partition data ([[database sharding]])
  → async pipelines ([[event-driven]])
```

- [[Horizontal vs Vertical Scaling]] is a cost and complexity decision, not a m…
- Vertical scaling is simpler until hardware limits or blast radius force distr…

## Mistakes to Avoid
- **Mistake:** Skipping failure modes until production
- **Mistake:** Ignoring idempotency, timeouts, or rollback where required
- **Mistake:** Optimizing or distributing before measuring the real bottleneck

## Pros/Cons or Trade-offs
- **Pro:** Explicit requirements prevent cargo-cult microservices.
- **Con:** Over-design wastes time before product-market fit.
- **Trade-off:** distribution complexity vs single-node simplicity.

## Comparison
- vs [[Distributed computing]]: workload split vs end-to-end product design.
- vs [[KISS]]/[[SOLID]]/[[DRY]]: principles constrain how you shape the design.


### Use cases
- Interview design problems and production architecture reviews for multi-servi…
