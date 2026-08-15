[[SOLID]] [[API design]] [[Distributed computing]] [[Horizontal vs Vertical Scaling]] [[cache system]]

# System design

> System design is the practice of shaping software so requirements (scale, reliability, cost) are met while keeping boundaries clear enough that implementation can change without rewriting the product.

## Interview Relevance

Clarify requirements, data path, coordination, failure, and operability — not boxes for their own sake.

## Sources

- Martin Kleppmann, *Designing Data-Intensive Applications* (O'Reilly, 2017) — replication, partitioning, consistency — deep-dive
- Google SRE Book — reliability targets, capacity planning, incident response — deep-dive
- AWS Well-Architected Framework — operational excellence, reliability, performance efficiency — overview

## Key Concepts

- **Requirements first:** QPS, durability, consistency, failure domains, operability.
- **Ports and adapters:** domain rules stay free of framework/DB types ([[SOLID]]).
- **Scale path:** single node → replicas/cache → vertical → horizontal → shard/async.
- **Failure design:** timeouts, idempotency, [[backpressure]], observability.


## Technical Details

### What system design is asking

Whether in an interview or a production review, the same questions recur:

| Question | What a good answer names |
|----------|--------------------------|
| Who uses it and how often? | Read/write ratio, peak queries per second, geographic spread |
| What must never be lost? | Durability, backup, replication |
| What can be briefly wrong? | Consistency trade-offs ([[Eventual consistency]]) |
| What fails first? | Single host, zone, region, dependency |
| How do you know it is healthy? | Metrics, traces, synthetic checks |

System design is not drawing boxes for its own sake. Every component should map to a requirement or a failure mode you are mitigating.

## Abstraction versus implementation

Stable systems separate **what** the product does from **how** it is wired today:

```txt
Domain / use cases  →  ports (interfaces, policies)
                              ↑
                    adapters (HTTP, SQL, message bus, object storage)
```

| Layer | Holds | Changes when |
|-------|-------|--------------|
| Domain | Business rules, invariants | Product requirements change |
| Ports | Contracts between domain and outside world | Integration shape changes |
| Adapters | Frameworks, databases, vendor software development kits | You swap vendors or protocols |

This mirrors [[SOLID]] dependency inversion and hexagonal architecture: business logic should not import a specific database driver type.

## A practical design loop

1. **Clarify scope** — functional requirements, scale targets, latency budget, consistency needs.
2. **Sketch the data path** — who writes, who reads, where state lives ([[database sharding]], [[cache system]]).
3. **Identify coordination** — single leader, [[Quorum]], or fully independent replicas ([[Raft]] when you need a replicated log).
4. **Plan for failure** — timeouts, retries with jitter, idempotent handlers, [[backpressure]].
5. **Make it operable** — dashboards, runbooks, capacity headroom before launch.

## Scaling path (typical order)

Most products grow through a predictable sequence; skipping steps often creates rework:

```txt
Single service + single database
  → read replicas + caching
  → vertical scaling (bigger machine)
  → horizontal scaling (more stateless replicas)
  → partition data ([[database sharding]])
  → async pipelines ([[event-driven]])
```

[[Horizontal vs Vertical Scaling]] is a cost and complexity decision, not a moral one. Vertical scaling is simpler until hardware limits or blast radius force distribution.

## Common failure patterns in design reviews

- **Leaky boundaries** — domain code imports HTTP framework types or raw SQL rows; every feature touches twelve files.
- **Distributed monolith** — microservices that must deploy together because they share a database transaction.
- **Missing idempotency** — retries duplicate payments or orders ([[API design]] idempotency keys).
- **Cache as source of truth** — [[cache system]] accelerates reads; it does not replace durability guarantees.
- **No observability** — you cannot fix what you cannot see per layer.

*What breaks first when traffic doubles?* Usually the database connection pool or an unbounded queue — design limits before you need them.

## Related design principles in this vault

| Principle | Focus |
|-----------|-------|
| [[KISS]] | Prefer the simplest design that meets requirements |
| [[DRY]] | One authoritative definition of each rule |
| [[SOLID]] | Object-oriented modularity at class and module boundaries |
| [[GRASP]] | Responsibility assignment in object models |

## Real-World Applications

Interview design problems and production architecture reviews for multi-service products.


## Pros/Cons or Trade-offs

- **Pro:** Explicit requirements prevent cargo-cult microservices.
- **Con:** Over-design wastes time before product-market fit.
- **Trade-off:** distribution complexity vs single-node simplicity.


## Comparison

- vs [[Distributed computing]]: workload split vs end-to-end product design.
- vs [[KISS]]/[[SOLID]]/[[DRY]]: principles constrain how you shape the design.


## Mistakes to Avoid

- Skipping failure modes until production.
- Ignoring idempotency, timeouts, or rollback where required.
- Optimizing or distributing before measuring the real bottleneck.

