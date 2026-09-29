[[Distributed computing]] [[System design]] [[Cache]] [[connection pooling]]

**Database sharding** is a technique for splitting a very large database into **smaller database called shards,** usually distributed across multiple servers.
**Each shard contains different rows of the same logical dataset.**
- You need to define a **shard key**.

The main reason for doing sharding is **horizontal scalability.** Eventually, one database server may not have enough CPU, memory, storage, or I/O capacity. Sharding spreads the workload across multiple machines.

### Horizontal sharding
splitting a database by rows and distributing those rows across multiple database servers.
- Each database has the **same table structure,** but stores different rows.

"Same columns, different rows, distributed across different database servers."

**Shard key** is the field you use to decide **which shard stores a particular row.**
- for `users` table, `user_id` is a common shard key.
- "Given `user_id=104`, which database should I query?"

When we use a simple hashing/modulo

Vertical sharding splitting tables by columns.

## Sharding Algorithm
Sharding algorithm is the rule that takes a **shard key** and determines **which shard should store the row.** 

**Hash-based sharding**
`shard = hash(user_id) % number_of_shards`. The advantage is that hashing generally distributes keys relatively evenly, reducing the chance of a hot shard. Problem with this is if you change total number of shards, many rows get mapped to different shards. You may need to move a huge amount of data.

**Ranged-based sharding**
```txt
Shard 1 → user_id 1 - 1,000,000
Shard 2 → user_id 1,000,001 - 2,000,000
Shard 3 → user_id 2,000,001 - 3,000,000
```
when you frequently query ranges: `WHERE user_id BETWEEN 10000 AND 20000`

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
- mongodb + sharding

partitioning vs sharding
scope and infrastructure
sharding: multiple server, shard among independent server. Scale horizontal
partitioning: withing single database or server. Scale vertically

data consistency among shard
partitioning limited by single server

choose right sharding strategy
- Performance requirement, target response time, acceptable response latency
- data distribution, even spread shards, avoid single point of failure.
	- unique sharding key, equal distribution. Indexing shard key
	- robust data migration tools.
	- detailed documentation of data sharding planing.