[[Database]] [[ACID]] [[OLTP]] [[Vector database]]

# BASE

> A design stance for large distributed stores—Basically Available, Soft state, Eventually consistent—trading immediate [[ACID]] guarantees for availability and partition tolerance.





## Interview Relevance
BASE tests whether you know CAP-era tradeoffs without treating “eventual consistency” as a free lunch. Interviewers want when staleness is acceptable, how soft state appears (TTL, lag), and when to keep an [[ACID]] source of truth instead.

## Sources
- Dan Pritchett, "BASE: An Acid Alternative" (ACM Queue, 2008) — deep-dive
- Kleppmann, *Designing Data-Intensive Applications*, Ch. 9 — deep-dive
- [Wikipedia — Eventual consistency](https://en.wikipedia.org/wiki/Eventual_consistency) — overview

## Core Definition
BASE is not a formal standard like [[ACID]]; it names architectures that prioritize availability under partition by allowing temporary inconsistency and state that can change without a new client write.

## Key Concepts
- **Basically Available:** respond even if some nodes or replicas are down → partial answers beat total outage.
- **Soft state:** state may change without new input → replication lag, TTL expiry, background repair.
- **Eventually consistent:** replicas converge if writes stop → reads may be stale meanwhile.
- **Not a protocol:** a family of engineering tradeoffs → contrast with ACID’s precise transaction semantics.

## Technical Details
| Letter | Meaning in practice |
|--------|---------------------|
| **Basically Available** | System responds even if some nodes or replicas are down |
| **Soft state** | State may change without new input (replication lag, TTL expiry) |
| **Eventually consistent** | Replicas converge if writes stop; reads may be stale meanwhile |

When BASE fits:

- Session caches, feature flags, rate-limit counters where brief staleness is acceptable
- CDN-backed read models fed by async replication
- [[Vector database]] indexes rebuilt asynchronously from an [[OLTP]] source of truth

When BASE hurts:

- Financial ledger balances, inventory deduction, idempotent payment processing — use [[ACID]] on a single authoritative store or explicit sagas/outbox patterns across services.

*When would you accept eventual consistency for a shopping cart?* When showing a stale item count for a few hundred milliseconds is cheaper than blocking checkout on a global lock.

## Real-World Applications
Feature-flag stores, session caches, and search indexes fed by CDC from an OLTP primary. Example: cart item count served from a cache that lags a few hundred milliseconds while payment still commits on an ACID ledger.

## Pros/Cons or Trade-offs
- **Pro:** Higher availability and partition tolerance; simpler horizontal scale for read-heavy soft data.
- **Con:** Clients must tolerate staleness, conflict resolution, and harder debugging of “why did I see X then Y?”

## Comparison
vs [[ACID]]: ACID gives immediate, transaction-scoped correctness on one store; BASE accepts delayed convergence for availability across distributed replicas. Neither replaces the other—pair an ACID system of record with BASE read models when needed.

## Mistakes to Avoid
- Calling every NoSQL system “BASE” without naming the actual consistency model.
- Using eventual consistency for money movement without idempotency and a single source of truth.
- Assuming “eventually” has a bound — without anti-entropy and monitoring, lag can be unbounded.
