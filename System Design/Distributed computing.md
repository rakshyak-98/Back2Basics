[[distributed system]] [[marshalling]] [[Throughput]] [[race condition]] [[Raft]]

# Distributed computing

> Distributed computing splits one workload across networked machines that exchange messages — gaining aggregate capacity while paying for coordination, partial failure, and serialization.

---

## Map of the problem space

```txt
Coordinator → partition input → workers execute tasks → aggregate results
                     ↘ retry failed tasks ↙
```

| Challenge | Mitigation |
|-----------|------------|
| Node death mid-task | Restart task; checkpoint progress |
| Straggler worker | Speculative duplicate execution |
| Data gravity | Move compute to data (locality) |
| Schema drift | Versioned [[marshalling]] / [[Serialization]] |
| Shared mutable state | Consensus ([[Raft]]), queues, or conflict-free structures |

**Distributed computing** is the workload pattern (map-reduce, render farm, microservice pipeline). **[[distributed system]]** is the operational reality those workloads run on — partial failure, replication, consistency.

## Job design checklist

```txt
1. Partition input into independent chunks where possible
2. Tasks should be idempotent (retries happen)
3. Combine step should be deterministic when feasible
4. Persist checkpoints for long jobs
5. Measure speedup — Amdahl's law limits parallel gain
```

## Failure signatures

| Symptom | Direction |
|---------|-----------|
| Job stuck at 99% | Straggler — kill slow worker, rerun partition |
| Duplicate outputs | At-least-once retry without deduplication key |
| Worker out of memory | Skewed partition — rebalance keys |
| Rare wrong results | Non-determinism or [[race condition]] in combine |
| Coordinator single point of failure | Highly available queue or elected leader |

## When distribution hurts

- Central processing unit-bound jobs smaller than network round-trip overhead — one machine wins.
- Strong interactive latency — every hop adds milliseconds.
- Workload cannot be partitioned — fix the data model before adding nodes.

*What breaks first?* Chatty fine-grained remote procedure calls — overhead eats [[Throughput]] gains.

## Sources

- Dean & Ghemawat, "MapReduce: Simplified Data Processing on Large Clusters" (OSDI 2004).
- Gene Amdahl, "Validity of the Single Processor Approach" (1967) — parallel speedup limits.
- Martin Kleppmann, *Designing Data-Intensive Applications*.
