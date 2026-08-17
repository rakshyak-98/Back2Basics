[[Raft]] [[distributed system]] [[Eventual consistency]] [[Distributed computing]] [[database sharding]]

# Quorum

> A quorum is the minimum number of replicas that must participate in a read or write for the operation to count — the lever that trades availability against staleness.

```txt
        Quorum ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** State `R + W > N`, give a Dynamo-style example, and distinguish quorum counti…

## Sources
- Giuseppe DeCandia et al., "Dynamo: Amazon's Highly Available Key-value Store" (SOSP 2007) — deep-dive
- Martin Kleppmann, *Designing Data-Intensive Applications* — replication chapter — deep-dive

## Key Concepts
- **N / W / R:** replicas, write acks, read responses.
- **Overlap rule:** `R + W > N` ⇒ read/write sets intersect.
- **Majority:** `floor(N/2)+1` — also used in Raft, different mechanism.
- **Not consensus:** counting rule ≠ single ordered log.

## Technical Details
| Parameter | Meaning |
|-----------|---------|
| **N** | Replication factor |
| **W** | Nodes that must ack a write |
| **R** | Nodes consulted for a read |

- **Example:** N=3, W=2, R=2 → R+W=4 > 3.

| Configuration | Effect |
|---------------|--------|
| W=N, R=1 | Durable writes; reads may be stale if careless |
| W=1, R=N | Fast writes; expensive consistent reads |
| W=majority, R=majority | Survives one failure in a 3-node cluster |

```txt
Cassandra: WRITE/READ CONSISTENCY QUORUM
MongoDB: writeConcern/readConcern majority
etcd / Raft: implicit majority on commit
```

| Symptom | Likely cause | Direction |
|---------|--------------|-----------|
| Write timeouts | W high while nodes down | Repair; lower W only with accepted risk |
| Stale reads | R+W ≤ N | Raise R or W |
| Quorum lost | Majority unavailable | Stop unsafe writes; restore nodes |
| Hot partition | Skewed shard key | Reshard; cache ([[database sharding]]) |

- Accept W=1 for high-ingest telemetry

## Mistakes to Avoid
- **Mistake:** Claiming consistency when R+W ≤ N
- **Mistake:** Computing N from stale membership during reconfiguration
- **Mistake:** Split-brain “fixes” that accept writes without quorum

## Pros/Cons or Trade-offs
- **Higher W/R:** stronger freshness; lower availability under failure.
- **Lower W/R:** faster/more available; stale or divergent reads.
- **Trade-off:** per-operation quorum vs always-on Raft for metadata.

## Comparison
- vs [[Raft]]: Raft = consensus log; quorum = how many must answer.
- vs [[Eventual consistency]]: weak quorums enable eventual models.


### Use cases
- Cassandra/Dynamo-style stores, MongoDB majority concerns, and any replica set…
