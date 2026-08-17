[[Distributed computing]] [[Raft]] [[Quorum]] [[Eventual consistency]] [[backpressure]] [[System design]] [[scaling data migration]]

# distributed system

> A distributed system is software whose parts run on multiple networked machines and must coordinate despite delayed messages, partial failures, and disagreeing clocks.

```txt
        distributed system ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Name partial failure, replication, consistency, coordination, and time

## Sources
- Martin Kleppmann, *Designing Data-Intensive Applications* — deep-dive
- [Raft paper](https://raft.github.io/raft.pdf) — deep-dive
- Google SRE Book — overload and cascading failure — deep-dive

## Key Concepts
- **Distribution trades complexity for scale/availability:** — only when needed.
- **Partial failure is normal:** — design for it.
- **CAP under partition:** choose consistency vs availability per operation.
- **Exactly-once is composed:** at-least-once + idempotent handlers + dedupe keys.

## Technical Details
```txt
Client → load balancer → service replicas → replicated data store
                              ↘ message queue / events ↙
```

| Problem | What goes wrong | Typical tools |
|---------|-----------------|---------------|
| Partial failure | One node dies; others run | Health checks, redundancy |
| Replication | Copies diverge | WAL, [[Raft]], primary-replica |
| Consistency | Stale/conflicting reads | [[Quorum]], linearizable stores |
| Coordination | Who is leader? | Consensus, leases, fencing |
| Time | Ordering across hosts | Logical clocks, version vectors |

- Failure-first: failure domains, replication factor + ack policy, timeouts+jit…

| What you see | Likely cause | Direction |
|--------------|--------------|-----------|
| Different answers from replicas | Stale read / lost quorum | Tune consistency; verify leader |
| Cascading outage | Retry storm | Circuit breakers, [[backpressure]] |
| Data loss after crash | Ack before durable | Sync commit / fsync |
| Split brain writes | Both sides accept | Consensus/fencing/conflict policy |
| Random auth failures | Clock skew | NTP; monotonic ids |

## Mistakes to Avoid
- **Mistake:** Distributing before SLOs require it
- **Mistake:** Assuming exactly-once messaging exists end-to-end
- **Mistake:** Infinite retries without jitter/backoff ([[backpressure]])

## Pros/Cons or Trade-offs
- **Pro:** Capacity and fault domains beyond one box.
- **Con:** Ops load, subtle consistency bugs, slower debugging.
- **Trade-off:** distribute early vs stay on one well-operated node.

## Comparison
- vs [[Distributed computing]]: computing emphasizes split workloads
- vs single-node: simpler ACID; harder HA/scale.


### Use cases
- Multi-AZ microservices, replicated datastores, and event pipelines that must …
