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

Used by: etcd, CockroachDB, TiKV, Consul.