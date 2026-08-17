[[Quorum]] [[distributed system]] [[cache system]] [[Concurrent modification]] [[DNS]]

# Eventual consistency

> Eventual consistency means replicas may disagree right after a write, but if updates stop, they converge — availability and latency now, sameness later.

```txt
        Eventual consisten ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Define eventual vs strong, name client guarantees (read-your-writes), and pic…

## Sources
- Werner Vogels, "Eventually Consistent" (ACM Queue, 2008) — overview
- Martin Kleppmann, *Designing Data-Intensive Applications* — deep-dive
- [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) — document “eventual” in contracts — overview

## Key Concepts
- **Async replication:** ack now; other replicas catch up later.
- **Staleness window:** define SLO for how stale is OK.
- **Client strategies:** sticky primary, tokens, bounded lag, UI honesty.
- **Merge policy required:** otherwise divergence never ends.

## Technical Details
```txt
Write → replica A (ack to client)
     ↘ async replication → replicas B, C (later)
Read from B before replication completes → stale value
```

| Domain | Eventual behavior example |
|--------|---------------------------|
| DNS | Old IP until TTL ([[DNS]]) |
| [[cache system]] | Stale until invalidate/TTL |
| CDN | Edge lags origin |
| Multi-region DB | Cross-region lag |
| CQRS read models | Projection catches up |

| Guarantee | How to approximate |
|-----------|-------------------|
| Read-your-writes | Sticky primary / session affinity |
| Monotonic reads | Consistency token |
| Bounded staleness | Max lag SLO |
| Tolerate stale | UI “updating…” / version |

- Stronger: higher [[Quorum]] R/W, sync replication, or leader reads.

| Policy | Behavior |
|--------|----------|
| Last-write-wins | Simple; clock skew surprises |
| Version vectors / CAS | Detect; app merges |
| CRDTs | Mathematically mergeable |
| Read repair | Background fix |

- Poor fit: money/inventory, security revocation, global unique constraints.

## Mistakes to Avoid
- **Mistake:** No conflict policy ([[Concurrent modification]] disasters)
- **Mistake:** “Eventually revoked” access for security-critical rights
- **Mistake:** Calling it fine for ledger balances without reservations/sagas

## Pros/Cons or Trade-offs
- **Pro:** Lower latency, higher availability under partition.
- **Con:** Stale reads; conflict complexity.
- **Trade-off:** staleness SLO vs coordination cost.

## Comparison
- vs strong/linearizable stores: agree before ack vs converge later.
- vs [[Quorum]]: quorums tune how eventual/strong a given op is.


### Use cases
- CDN/DNS caches, multi-region user profiles, and social feeds where brief stal…
