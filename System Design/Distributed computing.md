[[System Design]] [[distributed system]] [[marshalling]] [[race condition]]

# Distributed computing

> Distributed computing — split a job across networked machines; pay for coordination, partial failure, and serialization.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Many computers pass messages to finish one workload (map-reduce, microservices, HPC). Hard parts: failures mid-job, skew, and “what time is it?”

```txt
Coordinator → tasks → workers → results → reduce
                 ↘ retry failed tasks ↙
```

| Challenge | Mitigation |
|-----------|------------|
| Node death | Restart tasks; checkpoint |
| Stragglers | Speculative execution |
| Data gravity | Move compute to data |
| Schema drift | Versioned [[marshalling]] |

---

## Standard config / commands

```txt
# Job shape
1. Partition input
2. Pure tasks (idempotent)
3. Deterministic combine when possible
4. Persist checkpoints
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Job hangs 99% | Straggler worker | Speculative task; kill slow node |
| Duplicate outputs | At-least-once retry | Idempotent writes; dedupe keys |
| OOM on worker | Skewed partition | Rebalance keys; memory limits |
| Wrong results rare | Non-determinism / race | Pure functions; seed RNG |
| Coord SPOF | Single master | HA coordinator / queue |

---

## Gotchas

> [!WARNING]
> **Shared mutable NFS “coordination”** — races and locks; prefer explicit consensus/queue.

> [!WARNING]
> **Assuming identical clocks** — use logical time / job epochs.

> [!WARNING]
> **Chatty fine-grained RPC** — overhead eats speedup (Amdahl).

---

## When NOT to use

- **CPU-bound tiny jobs** — single machine faster.
- **Strong interactive latency** — distribution adds hops.
- **Unpartitionable state** — fix data model first.

---

## Related

[[distributed system]] [[Raft]] [[marshalling]] [[Throughput]] [[race condition]]
