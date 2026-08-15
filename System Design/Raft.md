[[Quorum]] [[distributed system]] [[Eventual consistency]] [[Distributed computing]]

# Raft

> Raft is a consensus algorithm that elects a leader, replicates an append-only log to a majority of nodes, and commits only after durable replication — strong coordination without Paxos opacity.

## Interview Relevance

Walk leader election, log replication, commit = majority, odd voter counts, and when Raft is the wrong tool (cross-region user data).

## Sources

- Diego Ongaro & John Ousterhout, [In Search of an Understandable Consensus Algorithm](https://raft.github.io/raft.pdf) (USENIX ATC 2014) — deep-dive
- [Raft website](https://raft.github.io/) — overview
- etcd documentation — production Raft tuning — deep-dive

## Key Concepts

- **Roles:** Leader, Follower, Candidate; **Term** fences stale leaders.
- **Commit rule:** majority durable ack before apply/respond.
- **Safety:** two terms cannot both commit the same index with majority.
- **Learners:** non-voting; do not count toward quorum.

## Technical Details

```txt
Client → Leader → append entries → Followers
              └─ commit when majority ack → apply to state machine
```

| Role | Responsibility |
|------|----------------|
| **Leader** | Accepts client writes; replicates log entries |
| **Follower** | Receives entries; votes; classic Raft does not serve writes |
| **Candidate** | Contests leadership during elections |
| **Term** | Monotonic epoch; fences stale leaders |

1. Client → leader (or forward).
2. Leader appends + replicates in parallel.
3. Majority store → **committed**.
4. Apply to state machine; respond.
5. Followers apply in log order when they learn commit index.

| Knob | Trade-off |
|------|-----------|
| Cluster size (3, 5, 7) | Odd count; more nodes → higher write latency |
| Election timeout | Too low → flap; too high → slow failover |
| Heartbeat interval | Must be ≪ election timeout |
| Snapshotting | Bounds disk growth |

```bash
etcdctl endpoint health
etcdctl endpoint status -w table
```

| Symptom | Likely cause | Direction |
|---------|--------------|-----------|
| No leader | Lost majority | Restore connectivity; odd voters |
| Flapping | Aggressive timeouts / CPU starvation | Raise timeout; isolate noise |
| Disk full | Unbounded log | Snapshot/compact |
| Slow commits | Follower lag | Replace sick node; faster disk |

**Two-node clusters are a trap.** Wrong tool: planet-scale [[Eventual consistency]] data; single-process apps; sync cross-region Raft on every user write.

## Real-World Applications

etcd, Consul, TiKV, and many Kubernetes control-plane stores.

## Pros/Cons or Trade-offs

- **Pro:** Understandable strong consistency; clear leader.
- **Con:** Write latency tied to majority RTT; availability needs majority.
- **Trade-off:** more voters (resilience) vs slower commits.

## Comparison

- vs [[Quorum]] counting: Raft is full consensus (ordered log); Dynamo quorum is a response-count rule.
- vs Paxos: same problem class; Raft prioritizes teachability/ops clarity.

## Mistakes to Avoid

- Running two voters and calling it HA.
- Counting learners toward failover.
- Using global Raft for every product write across continents.
