[[Quorum]] [[distributed system]] [[Eventual consistency]] [[Distributed computing]]

# Raft

> Raft is a consensus algorithm that elects a leader, replicates an append-only log to a majority of nodes, and commits entries only after durable replication — giving strongly consistent coordination without the opacity of Paxos.

---

## Roles and terms

```txt
Client → Leader → append entries → Followers
              └─ commit when majority ack → apply to state machine
```

| Role | Responsibility |
|------|----------------|
| **Leader** | Accepts client writes; replicates log entries |
| **Follower** | Receives entries; votes in elections; does not serve writes (in classic Raft) |
| **Candidate** | Contests leadership during elections |
| **Term** | Monotonic epoch number; fences stale leaders |

If a partitioned former leader receives writes, followers reject them because its term is outdated — this prevents split-brain commits when combined with majority rules.

## How an entry becomes committed

1. Client sends command to leader (or is forwarded to leader).
2. Leader appends entry to its local log and replicates to followers in parallel.
3. Once a **majority** of nodes store the entry, the leader marks it **committed**.
4. Leader applies committed entries to the **state machine** (key-value store, configuration, and so on) and responds to the client.
5. Followers apply committed entries in log order when they learn the commit index.

Safety property: if two leaders in different terms both claim commitment for the same log index, they cannot both have majority acknowledgment — the term and index pairing detects conflicts.

## Operational parameters

| Knob | Trade-off |
|------|-----------|
| Cluster size (3, 5, 7) | Odd count avoids tied elections; more nodes = higher write latency |
| Election timeout | Too low → flapping elections; too high → slow failover |
| Heartbeat interval | Must be « election timeout |
| Snapshotting | Bounds disk growth; required for long-lived logs |

```bash
# etcd (Raft-based) health checks
etcdctl endpoint health
etcdctl endpoint status -w table
```

Raft powers **etcd**, **Consul**, **TiKV**, and many control-plane stores.

## Failure modes

| Symptom | Likely cause | Direction |
|---------|--------------|-----------|
| No leader | Lost majority (network partition or too many down nodes) | Restore connectivity; maintain odd voter count |
| Flapping leadership | Aggressive timeouts or central processing unit starvation | Increase election timeout; isolate noisy neighbors |
| Disk full | Unbounded log without compaction | Snapshot and compact; expand volume |
| Slow commits | Follower lag (slow disk or network) | Replace sick node; faster storage |

**Two-node clusters are a trap:** one failure removes majority — use three voters minimum for production.

Non-voting **learners** do not count toward quorum; do not assume they provide failover votes.

## When Raft is the wrong tool

- Planet-scale eventually consistent data — partition tolerance and availability beat global consensus latency.
- Single-process applications — a local database transaction suffices.
- Cross-region synchronous Raft on every write — round-trip time dominates; prefer regional leaders and asynchronous replication for user data.

*What breaks first under load?* Disk append latency on the leader or the slowest follower in the replication path.

## Sources

- Diego Ongaro & John Ousterhout, [In Search of an Understandable Consensus Algorithm](https://raft.github.io/raft.pdf) (USENIX ATC 2014).
- [Raft website](https://raft.github.io/) — visualizations and student guide.
- etcd documentation — production tuning for Raft clusters.
