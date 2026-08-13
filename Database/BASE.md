[[Database]] [[ACID]] [[OLTP]] [[Vector database]]

# BASE

> A design stance for large distributed stores—Basically Available, Soft state, Eventually consistent—trading immediate [[ACID]] guarantees for availability and partition tolerance.

## Origin and intent

BASE was coined to describe architectures (often NoSQL or geo-distributed caches) that **prioritize availability** over strict consistency when networks partition. It is not a formal standard like [[ACID]]; it names a family of engineering tradeoffs.

| Letter | Meaning in practice |
|--------|---------------------|
| **Basically Available** | System responds even if some nodes or replicas are down |
| **Soft state** | State may change without new input (replication lag, TTL expiry) |
| **Eventually consistent** | Replicas converge if writes stop; reads may be stale meanwhile |

## When BASE fits

- Session caches, feature flags, rate-limit counters where brief staleness is acceptable
- CDN-backed read models fed by async replication
- [[Vector database]] indexes rebuilt asynchronously from an [[OLTP]] source of truth

## When BASE hurts

- Financial ledger balances, inventory deduction, idempotent payment processing — use [[ACID]] on a single authoritative store or explicit sagas/outbox patterns across services.

*When would you accept eventual consistency for a shopping cart?* When showing a stale item count for a few hundred milliseconds is cheaper than blocking checkout on a global lock.

## Sources

- Dan Pritchett, "BASE: An Acid Alternative" (ACM Queue, 2008)
- Kleppmann, *DDIA*, Ch. 9 (consistency and consensus)
- Wikipedia — [Eventual consistency](https://en.wikipedia.org/wiki/Eventual_consistency)
