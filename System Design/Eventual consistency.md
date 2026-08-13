[[Quorum]] [[distributed system]] [[cache system]] [[Concurrent modification]]

# Eventual consistency

> Eventual consistency means replicas may disagree immediately after a write, but if updates stop, all replicas will converge to the same value — availability and latency now, sameness later.

---

## Why systems choose it

Under network partition or geographic distance, forcing every replica to agree before responding increases latency and can block availability (see CAP trade-offs in [[distributed system]]). Many large-scale systems acknowledge writes quickly and replicate asynchronously.

```txt
Write → replica A (ack to client)
     ↘ async replication → replicas B, C (later)

Read from B before replication completes → stale value
```

| Domain | Eventual behavior example |
|--------|---------------------------|
| Domain Name System | Old Internet Protocol address until time-to-live expires ([[DNS]]) |
| [[cache system]] | Stale until invalidation or time-to-live |
| Content delivery network | Edge copy lags origin |
| Multi-region databases | Cross-region replication lag |
| Command Query Responsibility Segregation read models | Projection catches up after write |

## Client-visible strategies

| Guarantee | How to approximate |
|-----------|-------------------|
| Read-your-writes | Route session to primary or sticky replica |
| Monotonic reads | Consistency token passed with each read |
| Bounded staleness | Maximum replication lag service level objective |
| Tolerate stale | User interface shows "updating…" or version number |

Stronger guarantees require higher [[Quorum]] R and W, synchronous replication, or reading from the leader.

## Conflict resolution

When two writers update concurrently, replicas diverge until a **merge policy** runs:

| Policy | Behavior |
|--------|----------|
| Last-write-wins (timestamp) | Simple; clock skew causes surprises |
| Version vectors / compare-and-swap | Detect conflict; application merges |
| Conflict-free Replicated Data Types | Mathematically mergeable structures |
| Read repair | Background compare and fix divergent replicas |

*What breaks first?* Undefined conflict policy — data never converges or silently loses updates ([[Concurrent modification]]).

## Where eventual consistency is a poor fit

- **Money movement and inventory** — use strong consistency, reservations, or sagas with explicit compensation.
- **Security revocation** — "eventually revoked" access is a vulnerability window.
- **Unique constraints across replicas** — needs coordination, not hope.

[[Eventual consistency]] is not "consistency does not matter" — define the acceptable staleness window and conflict rule in the service level objective.

## Sources

- Werner Vogels, "Eventually Consistent" (ACM Queue, 2008).
- Martin Kleppmann, *Designing Data-Intensive Applications* (O'Reilly, 2017).
- [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) terminology — document what "eventual" means in your application programming interface contract.
