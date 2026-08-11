[[System design]] [[database sharding]] [[ACID]] [[BASE]] [[mysql]] [[postgres]] [[connection pooling]]

# Horizontal vs Vertical Scaling

> Horizontal scaling adds machines; vertical scaling adds power to one machine — relational databases are generally harder to scale horizontally than many NoSQL designs, especially for writes and cross-node transactions.

---

## Mental model

**Say it in one breath:** Horizontal scaling means adding more database nodes; vertical scaling means making one node bigger — SQL engines default to vertical scale and read replicas because [[ACID]] transactions, foreign keys, JOINs, and unique constraints are expensive to preserve across shards.

Horizontal scaling is generally **more difficult with relational (SQL) databases** than with NoSQL databases.

### Why?

Horizontal scaling means **adding more machines**:

```text
                    ┌──────────┐
                    │  Client  │
                    └────┬─────┘
                         │
             ┌───────────┼───────────┐
             ▼           ▼           ▼
          DB Node 1   DB Node 2   DB Node 3
```

For a relational database such as **[[mysql]]** or **[[postgres]]**, the difficulty comes from maintaining:

* **[[ACID]] transactions**
* **strong consistency**
* **foreign-key relationships**
* **JOINs across data**
* **unique constraints**
* **transactions involving multiple rows/tables**

For example:

```sql
BEGIN;

UPDATE accounts
SET balance = balance - 100
WHERE id = 1;

UPDATE accounts
SET balance = balance + 100
WHERE id = 2;

COMMIT;
```

If `accounts` is distributed across different database nodes, maintaining the atomicity of that transaction becomes significantly more complicated.

### SQL databases commonly scale vertically first

```text
Vertical scaling:

        ┌──────────────────┐
        │  Bigger DB       │
        │                  │
        │  More CPU        │
        │  More RAM        │
        │  Faster Disk     │
        └──────────────────┘
```

Then they can use **read replicas** for horizontal scaling:

```text
                    ┌──────────┐
                    │  Primary │
                    └────┬─────┘
                         │
              ┌──────────┼──────────┐
              ▼          ▼          ▼
           Replica     Replica    Replica
           (read)      (read)     (read)
```

But this does not horizontally scale writes in the same straightforward way.

### NoSQL was often designed for horizontal scaling

Systems such as DynamoDB, Cassandra, and some distributed document databases are designed around partitioning ([[database sharding]]):

```text
                    Data
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
       Node A      Node B      Node C
       users 1-3   users 4-6   users 7-9
```

A **partition/shard key** determines which node stores the data.

So the short answer is:

> **Traditional relational databases are generally harder to horizontally scale, especially for writes and cross-node transactions.**

But it is important not to conclude that **SQL databases cannot horizontally scale**. Modern distributed SQL databases such as CockroachDB, Google Spanner, and YugabyteDB are specifically designed to do this — they just pay additional complexity and cost to preserve relational semantics and consistency.

| Approach | Scales | Tradeoff |
|----------|--------|----------|
| Vertical (bigger box) | Reads + writes on one primary | Hardware ceiling; downtime for big jumps |
| Read replicas | Read throughput | Replication lag; writes still on primary |
| Sharding / partition key | Write throughput | Cross-shard JOINs and transactions hard ([[database sharding]]) |
| Distributed SQL (Spanner-style) | Writes + relational semantics | Coordination overhead; ops complexity |

## Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Horizontal scale** | Add nodes to spread load | "Shard by tenant_id so most queries stay local." |
| **Vertical scale** | Bigger CPU/RAM/disk on one node | "First move before sharding — simpler ops." |
| **Read replica** | Copy primary for SELECT traffic | "Does not fix write bottleneck on primary." |
| **Shard key** | Column that routes row to a node | "Bad key = hot shard; resharding is painful." |
| **Distributed SQL** | SQL with cross-node transactions | "Spanner/Cockroach pay latency for global consistency." |

---

## Standard config / commands

### Scale path (typical OLTP)

```txt
1. Vertical — more CPU/RAM/IO on primary
2. Tune queries + indexes ([[covering index]], [[connection pooling]])
3. Read replicas for read-heavy workloads
4. Cache hot keys ([[cache system]])
5. Shard when single primary write QPS or disk is the limit ([[database sharding]] — plan [[scaling data migration]])
```

### Before sharding relational data

```txt
Ask: Can most queries include the shard key?
Ask: Are cross-table transactions required across shards?
If yes to transactions across shards → distributed SQL, saga, or redesign — not naive modulo sharding
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Primary CPU/disk maxed | `SHOW PROCESSLIST` / `pg_stat_activity` | Vertical scale; optimize hot queries first |
| Reads slow, writes OK | Replica lag, cache hit rate | Add read replicas; route analytics off primary |
| Writes maxed, reads OK | Primary QPS vs replica count | Shard writes or distributed SQL — replicas won't help |
| Cross-shard transfer fails | Rows on different shards | Saga / outbox; colocate related rows by shard key |
| "Works on one node" only | Assumed global JOINs after shard | Denormalize; query within shard |
| Hot shard | Per-shard metrics | Reshard; salt skewed keys |

---

## Gotchas

> [!WARNING]
> **Read replicas are not write scale** — all writes still hit the primary until you shard or use distributed SQL.

> [!WARNING]
> **Shard too early** — vertical scale + replicas + cache often buys years; sharding is a major operational commitment ([[database sharding]]).

> [!WARNING]
> **NoSQL ease ≠ no design cost** — partition keys and access patterns must be chosen upfront; ad-hoc JOINs disappear.

> [!WARNING]
> **Distributed SQL is not free** — global transactions add coordination latency and licensing/ops complexity.

---

## When NOT to use

- **Horizontal shard on day one** — exhaust vertical scale and read replicas unless you have proven multi-TB or write-QPS need.
- **NoSQL only for "scale"** — if you need cross-row transactions and ad-hoc relational queries, relational or distributed SQL may fit better.
- **Assume SQL cannot scale horizontally** — CockroachDB, Spanner, and YugabyteDB exist for workloads that need both SQL and distribution.

---

## Related

[[System design]] [[database sharding]] [[scaling data migration]] [[ACID]] [[BASE]] [[mysql]] [[postgres]] [[connection pooling]] [[cache system]] [[Eventual consistency]] [[Distributed computing]]
