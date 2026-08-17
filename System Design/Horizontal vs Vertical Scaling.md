[[database sharding]] [[scaling data migration]] [[ACID]] [[connection pooling]] [[cache system]] [[BASE]] [[covering index]]

# Horizontal vs Vertical Scaling

> Vertical scaling makes one machine bigger; horizontal scaling adds machines — relational databases usually scale up and out for reads first, because cross-node atomic transactions are expensive.





## Interview Relevance
Walk the typical OLTP scale path (vertical → tune → replicas → cache → shard) and explain why read replicas do not fix a write-saturated primary.

## Sources
- Martin Kleppmann, *Designing Data-Intensive Applications* — partitioning and replication — deep-dive
- Amazon Dynamo paper (DeCandia et al., SOSP 2007) — overview
- Google Spanner paper (Corbett et al., OSDI 2012) — deep-dive

## Recall Cues
- Walk the typical OLTP scale path (vertical → tune → replicas → cache → shard) and explain why read replicas do not fix a write-saturated primary?
- What is step 1: Vertical — bigger primary?
- What is step 3: Read replicas for read-heavy workloads?
- What is step 4: Cache hot keys ([[cache system]])?
- What is step 5: Shard when single primary write QPS or disk is the limit?
- What mistake is **Sharding on day one without evidence**?
- What mistake is **Expecting replicas to absorb write load**?
- What mistake is **Ignoring shard-key locality for multi-row transactions**?

## Technical Details
```txt
Vertical:   one bigger database
Horizontal: more database nodes (replicas, shards, distributed SQL)
```

| Approach | Scales | Trade-off |
|----------|--------|-----------|
| Vertical | Reads and writes on one primary | Hardware ceiling; downtime for large jumps |
| Read replicas | Read throughput | Lag; writes still on primary |
| Sharding ([[database sharding]]) | Write throughput | Cross-shard joins/tx hard |
| Distributed SQL | Writes with relational semantics | Coordination latency |

```txt
1. Vertical — bigger primary
2. Query tuning + indexes ([[covering index]], [[connection pooling]])
3. Read replicas for read-heavy workloads
4. Cache hot keys ([[cache system]])
5. Shard when single primary write QPS or disk is the limit
```

[[BASE]] NoSQL is partition-first; Spanner/CockroachDB/Yugabyte target distributed SQL.

| Question | If yes → |
|----------|----------|
| Writes maxed, reads fine? | Shard / distributed SQL — replicas will not help |
| Queries include tenant/user id? | Good shard key candidate |
| Cross-shard tx required? | Saga/outbox/distributed SQL |
| Under ~100 GB, moderate QPS? | Vertical + replicas may suffice |

## Mistakes to Avoid
- Sharding on day one without evidence.
- Expecting replicas to absorb write load.
- Ignoring shard-key locality for multi-row transactions.

## Comparison
- vs [[database sharding]]: sharding is one horizontal write strategy.
- vs [[scaling data migration]]: migration pain often appears when you finally shard.

## Real-World Applications
Growing SaaS Postgres/MySQL fleets and deciding when Vitess/Citus/Dynamo-style partitions are worth the ops cost.

## Pros/Cons or Trade-offs
- **Vertical pro:** simple semantics; **con:** ceiling and blast radius.
- **Horizontal pro:** capacity and failover; **con:** coordination and ops.
- **Trade-off:** shard early vs exhaust cheaper levers first.
