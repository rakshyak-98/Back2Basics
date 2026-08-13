[[Distributed computing]] [[Raft]] [[Quorum]] [[Eventual consistency]] [[backpressure]]

# distributed system

> A distributed system is software whose parts run on multiple networked machines and must coordinate despite delayed messages, partial failures, and clocks that disagree.

---

## Why distribution exists

Single machines eventually hit limits on central processing unit, memory, disk input/output, and fault tolerance. Distribution trades **complexity** for **scale** and **availability** — but only when the problem genuinely needs it ([[System design]]).

```txt
Client → load balancer → service replicas → replicated data store
                              ↘ message queue / events ↙
```

Every arrow is a network hop: latency, packet loss, and partition are normal, not exceptional.

## The hard problems

| Problem | What goes wrong | Typical tools |
|---------|-----------------|---------------|
| Partial failure | One node dies; others keep running | Health checks, redundancy, graceful degradation |
| Replication | Copies diverge after a crash | Write-ahead log, [[Raft]], primary-replica |
| Consistency | Readers see stale or conflicting data | [[Quorum]] reads/writes, linearizable stores |
| Coordination | Who is the leader? | Consensus, leases, fencing tokens |
| Time | Ordering events across hosts | Logical clocks, version vectors, monotonic identifiers |

The [CAP theorem](https://en.wikipedia.org/wiki/CAP_theorem) (Brewer) is often misquoted as "pick two." In practice: under network partition, you choose between strong consistency and availability for a given operation — design that choice explicitly ([[Eventual consistency]]).

## Failure-first design checklist

- **Failure domains** — availability zone, region, dependency; avoid single points without a failover story.
- **Replication factor** — how many copies, and what acknowledgment policy (`acks=all` versus `acks=1`).
- **Timeouts everywhere** — waiting forever is not reliability; pair with bounded retries and jitter.
- **Idempotent consumers** — at-least-once delivery plus duplicate handling beats pretending exactly-once exists everywhere.
- **Backups and restore drills** — replication is not backup; test recovery ([[scaling data migration]] practices apply).

## Symptom → direction (for this topic)

| What you see | Likely cause | Direction |
|--------------|--------------|-----------|
| Different answers from different replicas | Stale read or lost [[Quorum]] | Tune read consistency; verify leader |
| Cascading outage | Retry storm on a sick dependency | Circuit breakers, bulkheads, [[backpressure]] |
| Data loss after crash | Acknowledged before durable | Synchronous commit, fsync policy |
| Both sides accepting writes during partition | Split brain | Consensus, fencing, or conflict resolution strategy |
| Authentication failures at random | Clock skew | Network Time Protocol sync; prefer monotonic identifiers |

## Exactly-once is a composition

True exactly-once end-to-end is rare. Production systems usually implement:

```txt
at-least-once delivery + idempotent handlers + deduplication keys
```

Design for observable duplicates rather than denying they happen.

## When not to distribute

- A single node meets service level objectives with headroom — distribution adds operational load.
- You need multi-row atomic transactions across unrelated services — rethink service boundaries.
- The team cannot operate consensus, queues, and multi-region failover yet — complexity kills reliability.

*What breaks first when the network partitions?* Whatever assumed "the other side always responds."

## Sources

- Martin Kleppmann, *Designing Data-Intensive Applications* (O'Reilly, 2017), chapters on replication and consistency.
- [Raft paper](https://raft.github.io/raft.pdf) — Ongaro & Ousterhout, USENIX ATC 2014.
- Google SRE Book — handling overload, cascading failures, distributed tracing.
