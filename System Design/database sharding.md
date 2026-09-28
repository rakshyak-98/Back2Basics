[[Distributed computing]] [[System design]] [[Cache]] [[connection pooling]]

**Database sharding** is a technique for splitting a very large database into **smaller database called shards,** usually distributed across multiple servers.
**Each shard contains different rows of the same logical dataset.**
- You need to define a **shard key**.

The main reason for doing sharding is **horizontal scalability.** Eventually, one database server may not have enough CPU, memory, storage, or I/O capacity. Sharding spreads the workload across multiple machines.

Horizontal sharding.
Vertical sharding splitting tables by columns.

Sharding key specific or set of column in your data, designed as bases for shard data.
- all active user come to one single shard
Sharding algo
- MOD (modulo sharding) MOD3.
- Consistent hash (hash function).
- Range sharding
- Tag sharding

Implementation of sharding
query pattern, understanding data distribution.
migrating the existing data

how to move without taking application down, partitioning, incremental data apply, solid ways to verify the data got moved correcly, and switch traffic to new cluster.

- partition with choossen algo
- process database transaction modes from original system. Capture changes and apply to the shard data
- Data verification, comparing every single cell, comparing in between (check sum technique), 
- Shifting new traffic to new shard data, stop write operation during the migration. Automatic traffic shifting.

well design sharding system
easy to setup and understand, maintainablity
High availability
- elastic scale out
- Highly distributed system.
- Observability, monitoring
- Low overhead for migration and shutdown

## Related

[[Distributed computing]] [[System design]] [[Cache]] [[connection pooling]] [[Eventual consistency]] [[mysql partitioning]]
