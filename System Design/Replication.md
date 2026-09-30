## Problem with Replication Lag

Leader replication: it requires all the writes to go through a single node, but read-only queries can go to any replica.

[[read-scaling Architecture]] increase the capacity for serving read-only requests simply by adding more followers.

Reasons why you might want to replication data:
- To scale out the number of machines that can sere read queries (and thus increase read throughput)

> If the data that you're replication does not change over time, then replication is easy: you just need to copy the data to every node once. All the difficulty in replication lies in handling changes to replicated data.

**All the difficulty in replication lies in handling changes to replication data.**

## Algorithms for replicating changes between nodes
