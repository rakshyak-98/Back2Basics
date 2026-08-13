[[System Design]] [[Quorum]] [[Raft]] [[Distributed computing]] [[Eventual consistency]]

# distributed system

> Distributed system — multiple machines coordinate over the network; design for partial failure, replication, and clocks that lie.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Data must survive node loss via replication; coordination (leader/quorum) decides truth; networks delay and partition.

```txt
Client → LB → Service replicas → Replicated store
                      ↘ events / queues ↙
```

| Problem | Toolkit |
|---------|---------|
| Durability | Replicated log, fsync policy |
| Consistency | Quorum / consensus ([[Raft]]) |
| Availability | Redundancy, failover |
| Latency | Caching, locality |

---

## Standard config / commands

```txt
Checklist
[ ] Failure domains (AZ/region)
[ ] Replication factor + ack policy
[ ] Idempotent consumers
[ ] Timeouts + retries with jitter
[ ] Backups / restore drill
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Split answers | Stale replica / no quorum | Tune R/W; fence leaders |
| Cascading outage | Retry storm | Circuit break; bulkhead |
| Data loss after crash | Ack before durable | Sync commit; fix W |
| Partition “both sides write” | No leader election | Consensus or CRDT/strategy |
| Clock-skew auth | NTP | Sync time; prefer monotonic ids |

---

## Gotchas

> [!WARNING]
> **Network is not reliable** — timeouts are part of the API.

> [!WARNING]
> **Exactly-once is usually at-least-once + idempotency**.

> [!WARNING]
> **More replicas ≠ always safer** — ops complexity and lag grow.

---

## When NOT to use

- **Single-box fits SLO** — don’t distribute for fashion.
- **Strong multi-row transactions across services** — rethink boundaries.
- **Team can’t operate it** — complexity kills.

---

## Related

[[Distributed computing]] [[Raft]] [[Quorum]] [[Eventual consistency]] [[backpressure]]
