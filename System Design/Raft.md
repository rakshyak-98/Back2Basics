[[System Design]] [[Quorum]] [[distributed system]] [[Eventual consistency]]

# Raft

> Raft — consensus algorithm: elect a leader, replicate a log, stay consistent if a majority of nodes are up.

## Mental model

**Say it in one breath:** Followers elect a leader; clients write to the leader; entries commit when a majority replicates them; term numbers fence old leaders.

```txt
Client → Leader → append entries → Followers
              └─ commit when majority ack → apply FSM
```

| Role | Job |
| --- | --- |
| Leader | Handles client writes |
| Follower | Replicates log |
| Candidate | Election contestant |
| Term | Logical clock / epoch |

Used by etcd, Consul, TiKV, many “strongly consistent” stores.

## Standard config / commands

```bash
# etcd health mental check
etcdctl endpoint health
etcdctl endpoint status -w table
```

| Knob | Why |
| --- | --- |
| Odd cluster size (3/5) | Clear majority |
| Snapshotting | Bound log disk |
| Heartbeat / election timeout | Stability vs failover speed |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| No leader | Network partition / majority loss | Restore connectivity; odd members |
| Flapping elections | Timeout too aggressive; CPU starve | Tune timeouts; isolate noisy neighbors |
| Disk full on peer | Log growth | Snapshot/compact; enlarge disk |
| Split votes | Even members | Add/remove to odd |
| Slow commits | Follower lag | Faster disk/net; remove sick node |

## Gotchas

> [!WARNING]
> **2-node “cluster”** — one failure = no majority; use 3.

> [!WARNING]
> **Learners / non-voters** — don’t count them in majority math.

> [!WARNING]
> **Clock sync** — Raft doesn’t need perfect sync, but extreme skew + ops tooling still hurts.

## When NOT to use

- **High-scale AP data** — use quorum/DHT styles, not global Raft.
- **Single process apps** — SQLite/Postgres alone.
- **Cross-region chatty Raft** — latency kills; regional leaders + async.

## Related

[[Quorum]] [[distributed system]] [[Distributed computing]] [[Eventual consistency]]
