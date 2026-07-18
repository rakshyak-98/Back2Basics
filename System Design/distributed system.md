Where data must survive even when nodes fail. This is a classic distributed systems problem, and it's solved through a combination of replication, consensus, and durable storage strategies.

> [!INFO]
> Never let a single node be the only owner of any place of data.

### Replication

- Every piece of data is copied to multiple nodes (replicas). If one node dies, other still have the data
	- Synchronous replication -> A write is only acknowledged after all replicas confirm they've written it. Zero data loss, but higher latency.
	- Asynchronous replication -> A write is acknowledged after just the primary writes it, and replicas catch up later. Faster, but if the primary dies before replication completes, you lose that data.


> [!NOTE]
> For zero data loss, you want synchronous replication

#### Write Quorums (W + R > N)

This is the formula behind systems like Cassandra, DynamoDB, and Riak.

- **N** = total replicas
- **W** = how many nodes must confirm a write
- **R** = how many nodes must respond to a read

If **W + R > N**, you're guaranteed to always read the latest write.

Example with N=3: if W=2 and R=2, even if one node is dead, your reads/writes still work and data is safe.


#### Consensus Protocols (Raft / Paxos)

For strong consistency (not just availability), you need all nodes to _agree_ on the state of data. This is what consensus protocols solve.

**Raft** is the more approachable one:

- One node is elected **leader**
- All writes go through the leader
- The leader replicates the write to followers before acknowledging success
- If the leader dies, followers elect a new one — and no committed data is lost

Used by: `etcd`, `CockroachDB`, `TiKV`, `Consul`.

#### Write-Ahead Log (WAL)

Before data is written to the actual storage, it's first appended to a log on disk. If a node crashes mid-write, on recovery it replays the log to restore state.

This guarantees **no partial writes** are silently lost.

#### Persistent, Durable Storage

RAM is volatile -> if a node dies, RAM is gone. So any data that must survive node failure needs to be on disk (or SSD), ideally with `fsync` to ensure the OS actually flushes it to hardware.

### What happens when Nodes Die One by One?

With proper replication (say N=3, W=2)
- 1 node dies -> system keeps working, data intact (2 replicas remain).
- 2 nodes die -> system may become unavailable (can't reach quorum), but data is not lost, the surviving node still has it.
- All 3 die simultaneously -> data loss is possible if some writes hadn't fully replicated yet.

> [!NOTE]
> So the guarantee is -> you can lose up to N-W nodes without losing data, Beyond that, you're trading availability.

### CAP Theorem Reminder

In distributed systems, when nodes fail (partition), you must choose:
- CP (Consistency + Partition tolerance) -> System may go unavailable but data is never lost or stale, Raft-based systems do this.
- AP (Availability + Partition tolerance) -> System stays up but might return stale data.

