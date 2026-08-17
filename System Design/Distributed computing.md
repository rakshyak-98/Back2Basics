[[distributed system]] [[marshalling]] [[Throughput]] [[race condition]] [[Raft]] [[Serialization]]

# Distributed computing

> Distributed computing splits one workload across networked machines that exchange messages — aggregate capacity paid for with coordination, partial failure, and serialization.

```txt
        Distributed comput ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Partition + idempotent tasks + checkpoints

## Sources
- Dean & Ghemawat, MapReduce (OSDI 2004) — deep-dive
- Gene Amdahl (1967) — parallel speedup limits — overview
- Kleppmann, *Designing Data-Intensive Applications* — deep-dive

## Key Concepts
- **Partition → workers → aggregate:** ; retry failed tasks.
- **Idempotent tasks:** under at-least-once retry.
- **Data locality:** move compute to data when possible.
- **Shared mutable state:** [[Raft]], queues, or CRDTs — not hope.

## Technical Details
```txt
Coordinator → partition input → workers → aggregate
                     ↘ retry failed tasks ↙
```

| Challenge | Mitigation |
|-----------|------------|
| Node death mid-task | Restart; checkpoint |
| Straggler | Speculative duplicate |
| Schema drift | Versioned [[marshalling]] / [[Serialization]] |
| Shared mutable state | Consensus / queues / CRDT |

- Checklist: independent chunks

| Symptom | Direction |
|---------|-----------|
| Stuck at 99% | Kill straggler; rerun partition |
| Duplicate outputs | Dedupe key |
| Worker OOM | Rebalance skewed keys |
| Wrong rare results | Non-determinism / [[race condition]] in combine |
| Coordinator SPOF | HA queue or elected leader |

## Mistakes to Avoid
- **Mistake:** Distributing jobs smaller than RTT overhead
- **Mistake:** Non-idempotent tasks under retry
- **Mistake:** Ignoring skew until one worker OOMs

## Pros/Cons or Trade-offs
- **Pro:** Aggregate CPU/IO beyond one box.
- **Con:** Network overhead; failure modes; harder debugging.
- **Trade-off:** fine-grained RPCs (chatty) vs coarse partitions.

## Comparison
- vs [[distributed system]]: computing = workload split; system = failure/consistency reality.
- vs single-node: wins only when parallel fraction beats network cost.


### Use cases
- MapReduce/Spark jobs, render farms, and microservice pipelines that fan out w…
