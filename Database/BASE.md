[[Database]] [[ACID]] [[OLTP]] [[Vector database]]

# BASE

> A design stance for large distributed stores—Basically Available, Soft state, Eventually consistent—trading immediate [[ACID]] guarantees for availability and partition tolerance.

```txt
        BASE ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** BASE tests whether you know CAP-era tradeoffs without treating “eventual cons…

## Sources
- Dan Pritchett, "BASE: An Acid Alternative" (ACM Queue, 2008) — deep-dive
- Kleppmann, *Designing Data-Intensive Applications*, Ch. 9 — deep-dive
- [Wikipedia — Eventual consistency](https://en.wikipedia.org/wiki/Eventual_consistency) — overview

## Key Concepts
- **Basically Available:** respond even if some nodes or replicas are down → partial answers beat total …
- **Soft state:** state may change without new input → replication lag, TTL expiry, background …
- **Eventually consistent:** replicas converge if writes stop → reads may be stale meanwhile.
- **Not a protocol:** a family of engineering tradeoffs → contrast with ACID’s precise transaction …


- **Core:** BASE is not a formal standard like [[ACID]]

## Technical Details
| Letter | Meaning in practice |
|--------|---------------------|
| **Basically Available** | System responds even if some nodes or replicas are down |
| **Soft state** | State may change without new input (replication lag, TTL expiry) |
| **Eventually consistent** | Replicas converge if writes stop; reads may be stale meanwhile |

- When BASE fits:

- Session caches, feature flags, rate-limit counters where brief staleness is a…
- CDN-backed read models fed by async replication
- [[Vector database]] indexes rebuilt asynchronously from an [[OLTP]] source of…

- When BASE hurts:

- Financial ledger balances, inventory deduction, idempotent payment processing

- *When would you accept eventual consistency for a shopping cart?* When showin…

## Mistakes to Avoid
- **Mistake:** Calling every NoSQL system “BASE” without naming the actual cons…
- **Mistake:** Using eventual consistency for money movement without idempotenc…
- **Mistake:** Assuming “eventually” has a bound

## Pros/Cons or Trade-offs
- **Pro:** Higher availability and partition tolerance; simpler horizontal scale for read-heavy soft data.
- **Con:** Clients must tolerate staleness, conflict resolution, and harder debugging of “why did I see X then Y?”

## Comparison
- vs [[ACID]]: ACID gives immediate, transaction-scoped correctness on one store


### Use cases
- Feature-flag stores, session caches, and search indexes fed by CDC from an OL…
