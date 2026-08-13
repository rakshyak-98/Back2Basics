[[database sharding]] [[scaling data migration]] [[ACID]] [[connection pooling]] [[cache system]]

# Horizontal vs Vertical Scaling

> Vertical scaling makes one machine bigger; horizontal scaling adds machines — relational databases usually scale up and out for reads first, because cross-node atomic transactions are expensive.

---

## Two directions

```txt
Vertical:   one bigger database (more CPU, RAM, faster disk)
Horizontal: more database nodes (replicas, shards, distributed SQL)
```

| Approach | Scales | Trade-off |
|----------|--------|-----------|
| Vertical | Reads and writes on one primary | Hardware ceiling; downtime for large jumps |
| Read replicas | Read throughput | Replication lag; writes still on primary |
| Sharding ([[database sharding]]) | Write throughput | Cross-shard joins and transactions are hard |
| Distributed SQL (Spanner, CockroachDB) | Writes with relational semantics | Coordination latency and operational complexity |

## Why SQL resists naive horizontal write scaling

Relational engines preserve [[ACID]] transactions, foreign keys, joins, and unique constraints on one node by default. A transfer between two accounts on different shards cannot use a single local transaction without distributed coordination:

```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
```

If row 1 and row 2 live on different shards, atomicity requires two-phase commit, saga, or redesign so related rows share a **shard key**.

## Typical scale path for online transaction processing

```txt
1. Vertical — bigger primary
2. Query tuning + indexes ([[covering index]], [[connection pooling]])
3. Read replicas for read-heavy workloads
4. Cache hot keys ([[cache system]])
5. Shard when single primary write queries per second or disk is the limit
```

Read replicas **do not** fix a write-saturated primary — they only spread `SELECT` traffic.

## NoSQL and partition-first design

Systems like Apache Cassandra and Amazon DynamoDB assume **partition keys** upfront — horizontal scale is natural, but ad-hoc relational queries disappear. [[BASE]] (Basically Available, Soft state, Eventual consistency) contrasts with strict [[ACID]] on one node.

Modern **distributed SQL** (Google Spanner, CockroachDB, YugabyteDB) targets both — at the cost of complexity and latency.

## Decision prompts

| Question | If yes → |
|----------|----------|
| Writes maxed, reads fine? | Shard writes or distributed SQL — replicas will not help |
| Most queries include tenant or user identifier? | Good shard key candidate |
| Cross-shard transactions required? | Saga, outbox, or distributed SQL — not naive modulo sharding |
| Under 100 gigabytes, moderate queries per second? | Vertical + replicas may suffice for years |

*When would you shard before exhausting vertical scale?* Proven multi-terabyte growth or write queries per second with no bigger instance available — not interview cargo-cult.

## Sources

- Martin Kleppmann, *Designing Data-Intensive Applications* (O'Reilly, 2017), chapters on partitioning and replication.
- Amazon Dynamo paper (DeCandia et al., SOSP 2007) — partition-tolerant design.
- Google Spanner paper (Corbett et al., OSDI 2012) — globally distributed SQL.
