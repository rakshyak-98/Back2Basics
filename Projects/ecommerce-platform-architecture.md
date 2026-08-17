[[Projects]] [[marketplace app]] [[Messaging/Kafka/Kafka distributed event streaming]] [[Payment gateway]] [[gRPC]]

# Ecommerce platform architecture

> Client hits an API gateway, then domain services — sync reads over gRPC where needed, async facts over a bus after local commits.

```txt
        Ecommerce platform ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers want clear failure domains (catalog vs money), outbox/idempotenc…

## Sources
- [Kleppmann — Designing Data-Intensive Applications](https://dataintensive.net/) — deep-dive
- [Microservices.io — Pattern: Transactional outbox](https://microservices.io/patterns/data/transactional-outbox.html) — overview

## Key Concepts
- **API gateway / optional BFF:** edge REST for clients → internal service calls.
- **Sync vs async:** gRPC for low-latency reads; Kafka (or similar) for facts and side effects.
- **Separate money and catalog:** different failure domains → never hold catalog locks waiting on a PSP.
- **Outbox:** emit events after local commit → consumers are idempotent.

## Technical Details
```txt
Client ──► API Gateway (REST) ──► BFF (optional) ──► domain services
                              │
                    gRPC (sync reads) / Kafka (async facts)
                              │
         Order orchestrator · Payment/Refund · Catalog/Pricing
                              ▼
                    Notification (always async)
```

| Concern | Approach |
|---------|----------|
| Dual writes | Outbox + idempotent consumers |
| PSP latency | Do not hold DB locks across HTTP to Stripe/etc. |
| Cascades | Timeouts, bulkheads, backoff |

## Mistakes to Avoid
- **Mistake:** One giant ACID transaction across search index + PSP + primary DB
- **Mistake:** Fire-and-forget dual writes without an outbox
- **Mistake:** Letting notification failures roll back paid orders

## Pros/Cons or Trade-offs
- **Pro:** Clear domains scale teams and blast radius.
- **Con:** Eventual consistency needs explicit user-visible states.

## Comparison
- vs [[marketplace app]]: this note is the platform wiring
- vs modular monolith: start monolith if the team is small; keep the same domain boundaries.


### Use cases
- Order placed → local persist + outbox row → payment intent → webhook complete…

- **Example:** Payment succeeds but order write fails
