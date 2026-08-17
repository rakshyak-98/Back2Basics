[[Horizontal vs Vertical Scaling]] [[database sharding]] [[database migration]] [[mysql]] [[postgres]] [[BASE]] [[ACID]]

# Scaling data migration

> Moving data between database servers or nodes while scaling — much harder for relational databases introducing sharding than for partition-native NoSQL; replication and sharding solve different problems.





## Interview Relevance
Dual-write/backfill/cutover; checksums; expand-contract; rollback criteria.

## Sources
- Martin Kleppmann, *Designing Data-Intensive Applications* — partitioning and rebalancing — deep-dive
- Expand-Contract pattern (parallel change) — overview
- Vitess / Citus resharding guides — deep-dive

## Technical Details
### How it works

### 1. Relational database — [[mysql]] / [[postgres]]

Suppose you start with:

```text
             ┌──────────────┐
Users ──────►│ MySQL        │
             │ Single Node  │
             └──────────────┘
```

Now you want to scale horizontally:

```text
             ┌──────────┐
             │ Node 1   │
             ├──────────┤
             │ Node 2   │
             ├──────────┤
             │ Node 3   │
             └──────────┘
```

You need to decide **how to partition the existing data**.

For example:

```text
users 1–1,000,000     → Node 1
users 1,000,001–2M   → Node 2
users 2M–3M           → Node 3
```

This is **[[database sharding]]**.

The migration is difficult because existing data has to be redistributed while the application may still be writing to the database.

You might have:

```text
Old DB
 ├── User 1
 ├── User 2
 ├── User 3
 ├── ...
 └── User 3M
        │
        ▼
    Repartition
        │
   ┌────┼────┐
   ▼    ▼    ▼
 Node1 Node2 Node3
```

The hard part is not simply copying rows. You have to deal with:

* foreign keys
* [[ACID]] transactions
* unique constraints
* indexes
* JOINs
* concurrent writes
* consistency during migration

### 2. NoSQL database

Many NoSQL databases are designed around **partitioning from the beginning** ([[BASE]] tradeoffs).

For example:

```text
                    user_id
                       │
             ┌─────────┼─────────┐
             ▼         ▼         ▼
          Node A     Node B     Node C
          users      users      users
          1–100      101–200    201–300
```

If you add Node D:

```text
Before:

A ─── users 1–100
B ─── users 101–200
C ─── users 201–300


After:

A ─── users 1–75
B ─── users 76–150
C ─── users 151–225
D ─── users 226–300
```

The database can **automatically rebalance partitions**.

This makes scaling and migration easier operationally.

However, it still is not free. Data has to physically move between nodes, and during rebalancing the system has to maintain availability and consistency.

### The big difference

Think of it like this:

#### Traditional SQL

You often start with:

```text
              ONE DATABASE
                   │
        ┌──────────┼──────────┐
        │          │          │
      Users      Orders     Payments
```

Then later decide:

> "We need to split this across machines."

That can be a significant architectural change.

#### Distributed NoSQL

You often start with:

```text
                 Partition Key
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
     Partition A   Partition B   Partition C
        │              │              │
      Node A         Node B         Node C
```

Distribution is already part of the database's design.

### 3. Migration during scaling is particularly important

Imagine an IPTV backend with:

```text
10 million users
100,000 channels
1 billion viewing records
```

Initially:

```text
                  MySQL
                    │
              1 large machine
```

Eventually you need:

```text
              ┌───────────┐
              │ Sharding  │
              └─────┬─────┘
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
     MySQL 1     MySQL 2     MySQL 3
```

You cannot simply say:

```text
CREATE NODE 3;
```

and expect all data to magically be redistributed while everything continues normally.

You need a migration strategy.

A common approach is:

```text
                 Existing DB
                     │
              ┌──────┴──────┐
              │             │
          Old data       New writes
              │             │
              ▼             ▼
          Copy data      Dual/redirect
              │
              ▼
          Verify data
              │
              ▼
       Switch application
              │
              ▼
          New shards
```

This is why **database migrations become a major concern when horizontally scaling SQL databases**.

> **Note:** This is different from versioned **schema** migrations ([[database migration]]) — here we mean **data redistribution** across nodes while the system stays live.

### 4. Replication vs sharding

This distinction is very important.

#### Replication

Copies the **same data**:

```text
             Primary
            /       \
           ▼         ▼
       Replica 1  Replica 2
       SAME DATA  SAME DATA
```

Useful for:

* read scaling
* high availability
* failover

But it does not fundamentally solve storage or write scaling.

#### Sharding

Splits **different data**:

```text
          Database
             │
       ┌─────┼─────┐
       ▼     ▼     ▼
     Shard1 Shard2 Shard3
      A-F    G-M    N-Z
```

Useful for:

* write scaling
* storage scaling
* distributing workload

But it makes application and database architecture more complicated.

### In one sentence

**SQL databases:** migration becomes difficult mainly when you introduce sharding because relationships, transactions, and existing data need to be redistributed safely.

**Distributed NoSQL databases:** migration and rebalancing is usually more built-in because partitioning is a fundamental part of their architecture.

**Distributed SQL** (CockroachDB / Spanner-style): tries to give you SQL semantics while automatically moving data between nodes — a third category between manual SQL sharding and partition-native NoSQL.

| Pattern | What moves | Solves | Does not solve |
|---------|------------|--------|----------------|
| Replication | Full copy to replicas | Read scale, HA | Write or storage ceiling on primary |
| Sharding | Subset per node | Write + storage scale | Cross-shard transactions without redesign |
| NoSQL rebalance | Partition ranges | Add nodes with less app change | Zero cost — data still physically moves |
| Distributed SQL | Automatic range moves | SQL + distribution | Coordination latency and ops complexity |


### Configuration and commands

### SQL sharding migration (common phases)

```txt
1. Choose shard key; design routing layer
2. Stand up empty target shards
3. Dual-write (or write to old + async replicate to new)
4. Backfill historical rows in batches
5. Verify row counts / checksums per shard
6. Switch reads to new routing
7. Stop writes to old single node; decommission
```

See also [[database sharding]] resharding sketch and [[mysql data migrations]] for row-copy mechanics.

### NoSQL add-node checklist

```txt
1. Add node to cluster ring / token range
2. Monitor rebalance progress (bytes moved, pending ops)
3. Watch latency during move — throttle if needed
4. Confirm even partition distribution after settle
```

### Distinguish from schema migration

```txt
Schema migration ([[database migration]]): ALTER TABLE, versioned DDL
Scaling data migration (this note): move rows across nodes while scaling
```

---

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Resharding** | Change shard map and move rows | "Dual-write, backfill, verify, cut over." |
| **Rebalancing** | NoSQL moves partition ranges | "Built-in but still moves bytes on the wire." |
| **Dual-write** | App writes old + new during migration | "Bridge until backfill catches up." |
| **Replication** | Same data, more copies | "Read scale — not write scale." |
| **Cutover** | Switch reads/writes to new topology | "Needs checksums and rollback plan." |

---

## Real-World Applications
Sharding an existing OLTP database, region migrations, and major engine upgrades under live write traffic.

## Pros/Cons or Trade-offs
- **Sharding migration before exhausting replicas + vertical scale** — see [[Horizontal vs Vertical Scaling]].
- **Full resharding for a one-time archive** — time-based partition drop or cold storage may be simpler.
- **Cross-shard transactions without saga** — if money paths need atomicity across shards, redesign or use distributed SQL first.

---



- **Pro:** Live migration avoids long read-only windows.
- **Con:** Dual-write bugs and lag create hard-to-debug divergence.
- **Trade-off:** brief downtime cutover vs longer dual-running complexity.

## Comparison
- vs [[database sharding]]: sharding is why many migrations exist; this note is the move itself.
- vs [[Horizontal vs Vertical Scaling]]: scale decision precedes the migration plan.

## Mistakes to Avoid
> [!WARNING]
> **Replication ≠ sharding** — adding read replicas does not remove the need for a scaling data migration when writes or disk outgrow one primary.

> [!WARNING]
> **"CREATE NODE" fantasy** — SQL has no magic redistribute; plan dual-write and verification ([[database sharding]]).

> [!WARNING]
> **NoSQL rebalance is not instant** — large partitions still move over the network; plan capacity and client timeouts.

> [!WARNING]
> **Do not confuse with [[database migration]]** — schema version scripts do not replace shard cutover planning.

> [!WARNING]
> **IPTV-scale example** — billions of viewing rows make backfill time dominate; batch by time range or tenant.

---

| Symptom | Check | Fix |
|---------|-------|-----|
| Duplicate rows after cutover | Dual-write window overlap | Idempotent keys; dedupe job |
| Missing rows on new shard | Backfill lag vs cutover too early | Pause cutover; resume backfill |
| FK violations during copy | Child rows copied before parent | Order by dependency; disable FKs only with care |
| Unique constraint clash | Same email on two shards | Global index service or pre-migration dedupe |
| App still hits old node | Routing config / connection pool | Feature flag shard map; drain old pool |
| Rebalance never finishes | Node down; token imbalance | Cluster health; manual move ranges |
| Writes spike during rebalance | Hot partition | Salt keys; add capacity before rebalance |

---
