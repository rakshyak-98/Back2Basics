[[Raft]] [[distributed system]] [[Eventual consistency]] [[Distributed computing]]

# Quorum

> A quorum is the minimum number of replicas that must participate in a read or write for the operation to count — the lever that trades availability against how stale or divergent data may be.

---

## The overlap rule

In a cluster of **N** replicas, choose **W** write acknowledgments and **R** read responses such that:

```txt
R + W > N
```

Then read and write sets **overlap** — at least one node saw the latest write. This is the classic Dynamo-style tunable consistency model (DeCandia et al., 2007).

| Parameter | Meaning |
|-----------|---------|
| **N** | Replication factor (copies of data) |
| **W** | Nodes that must acknowledge a write |
| **R** | Nodes consulted for a read |

**Example:** N=3, W=2, R=2 → R+W=4 > 3 → read-your-writes style behavior if membership is stable.

## Majority versus custom quorums

**Majority** (`floor(N/2) + 1`) appears in [[Raft]] leader election and commit — a different mechanism than Dynamo quorums, though both use counting votes.

| Configuration | Effect |
|---------------|--------|
| W=N, R=1 | Durable writes; reads may be stale if not designed carefully |
| W=1, R=N | Fast writes; expensive reads for consistency |
| W=majority, R=majority | Survives one failure in a three-node cluster |

## Database examples

```txt
Apache Cassandra: WRITE CONSISTENCY QUORUM / READ CONSISTENCY QUORUM
MongoDB: writeConcern majority / readConcern majority
etcd / Raft: implicit majority on commit
```

## Failure behavior

| Symptom | Likely cause | Direction |
|---------|--------------|-----------|
| Write timeouts | W too high while nodes are down | Repair nodes; temporarily lower W only with accepted risk |
| Stale reads | R+W ≤ N or reading lagging replica | Raise R or W; use stronger read concern |
| "Quorum lost" | Majority of cluster unavailable | Stop accepting writes; restore nodes — do not split-brain |
| Hot partition | Skewed shard key | Reshard; cache ([[database sharding]]) |

Quorum overlap assumes correct membership during reconfiguration — clients with stale topology can compute wrong N.

## Quorum is not consensus

[[Raft]] implements **consensus** (one ordered log, one leader). Quorum is a **counting rule** for how many replicas must respond. You can use quorums without full consensus when your conflict model allows it ([[Eventual consistency]]).

*When would you accept W=1?* High-ingest telemetry where duplicate or briefly invisible writes are tolerable — not ledger balances.

## Sources

- Giuseppe DeCandia et al., "Dynamo: Amazon's Highly Available Key-value Store" (SOSP 2007).
- Martin Kleppmann, *Designing Data-Intensive Applications* (O'Reilly, 2017), chapter on replication.
