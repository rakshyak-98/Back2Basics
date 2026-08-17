[[MongoDB]] [[mongodb replicaset]] [[System Design/database sharding]] [[mognodb indexing]] [[mongodb schema]] [[mongodb connection]] [[mongodb migration]]

# MongoDB sharding

> MongoDB sharding splits a collection across shards by shard key — mongos routes queries using the config servers' chunk map.

```txt
        MongoDB sharding ──┬── Interview
               ├── Sources
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Interview Relevance
- **Interview probes:** Interviewers ask sharding to test shard-key choice, scatter-gather risk, and …

## Sources
- [Sharding — MongoDB Manual](https://www.mongodb.com/docs/manual/sharding/) — deep-dive
- [Shard Keys — MongoDB Manual](https://www.mongodb.com/docs/manual/core/sharding-shard-key/) — overview

## Technical Details
- All administrator below runs against **mongos** (`mongosh` → cluster router),…

### 1. Deploy topology (lab sketch)

```txt
CSRS:     cfg1,cfg2,cfg3   --configsvr --replSet cfgRS
Shard A:  a1,a2,a3         --shardsvr --replSet shardA
Shard B:  b1,b2,b3         --shardsvr --replSet shardB
mongos:   --configdb cfgRS/cfg1:27019,cfg2:27019,cfg3:27019
```

- Initiate each replica set (`rs.initiate`), then connect to **mongos**.

### 2. Register shards + shard a collection

```js
// Add shard replica sets (empty RS preferred for first join)
sh.addShard('shardA/a1:27018,a2:27018,a3:27018')
sh.addShard('shardB/b1:27018,b2:27018,b3:27018')

// Optional since 6.0 — still useful to pin / create DB
sh.enableSharding('app')

// Index must exist if collection already has data
db.app.orders.createIndex({ userId: 'hashed' })

// Shard the collection
sh.shardCollection('app.orders', { userId: 'hashed' })

// MongoDB 8.0+: shard + rebalance faster than waiting on balancer alone
// sh.shardAndDistributeCollection('app.orders', { userId: 'hashed' })

sh.status()
```

- Ranged example (query-local):

```js
db.app.events.createIndex({ tenantId: 1, createdAt: 1 })
sh.shardCollection('app.events', { tenantId: 1, createdAt: 1 })
```

- Connection string (application → mongos):

```
mongodb://user:pass@mongos1:27017,mongos2:27017/app?authSource=admin
```

### 3. Scale out (add capacity)

```js
// 1. Stand up new empty replica set with --shardsvr
// 2. rs.initiate on the new set
// 3. Register with cluster:
sh.addShard('shardC/c1:27018,c2:27018,c3:27018')

sh.status()                 // new shard present, chunk count low
sh.isBalancerRunning()      // should migrate toward balance
sh.getBalancerState()
```

- Balancer moves chunks automatically.
- Watch until chunk counts / data size converge

```js
// Optional: window migrations off-peak
sh.setBalancerState(true)
sh.startBalancer()
// sh.stopBalancer()  // during heavy DDL / incident only — remember to restart
```

### 4. Scale in / de-scale (remove a shard)

- Drain data off a shard, then retire hardware.
- **Do not shut down the shard until drain completes.:** 

```js
// Start drain — returns immediately; work is async
use admin
db.adminCommand({ removeShard: 'shardC' })

// Poll until state is "completed"
db.adminCommand({ removeShard: 'shardC' })
// intermediate: "draining" — chunks + jumbo chunks must leave
// also moves unsharded DBs whose primaryShard was this shard (movePrimary)

sh.status()
```

- Checklist while draining:

```txt
1. Balancer on (required for chunk migrate)
2. No jumbo chunks stuck on the shard (split / reshard if needed)
3. movePrimary for any DB still primary on that shard
4. When removeShard reports completed → stop mongod on that RS
5. Update monitoring / connection docs; keep mongos count ≥ 2
```

- Move primary shard for unsharded data:

```js
db.adminCommand({ movePrimary: 'analytics', to: 'shardA' })
```

### 5. Day-2 ops

```js
sh.status()
db.getSiblingDB('config').chunks.aggregate([
  { $group: { _id: '$shard', n: { $sum: 1 } } },
])
db.collection.getShardDistribution()   // from mongos, per collection

// Change shard key (6.0+ online reshard — plan capacity first)
sh.reshardCollection('app.orders', { tenantId: 1, orderId: 1 })
```

## Mistakes to Avoid
> [!WARNING]
> **Low-cardinality or monotonically increasing keys** (`createdAt` alone, `country`) → hot shard / hotspot. Prefer high-cardinality + hash or compound with a random/high-card prefix.

> [!WARNING]
> **Shard key fields are immutable** on a document once inserted (must delete+reinsert or reshard strategy).

> [!WARNING]
> **Empty shard on `addShard`** — joining a non-empty replica set that already has conflicting data is an ops footgun; add empty shards.

> [!WARNING]
> **De-scale ≠ `removeShard` once** — first call starts drain; keep polling until `completed` before powering off nodes.

> [!WARNING]
> **Transactions / joins across shards** — multi-doc transactions work but cost more; design for single-shard affinity when you can.

| Symptom | Check | Fix |
|---------|-------|-----|
| One shard hot (CPU/disk/QPS) | `getShardDistribution()`, key cardinality | Better key / hashed; zone or reshard; add shards |
| Queries slow / scatter-gather | Explain plan; missing shard key in filter | Rewrite query to include shard key; compound key |
| Balancer not moving | `sh.getBalancerState()`, locks, jumbo chunks | Start balancer; split jumbo; free disk on donors/recipients |
| `removeShard` stuck draining | Chunks left; primaryShard; jumbo | `movePrimary`; fix jumbo; wait / increase migrate concurrency carefully |
| mongos flapping / stale routing | mongos logs; CSRS health | Fix config RS; bounce mongos; ensure majority CSRS |
| Writes fail `ShardKeyNotFound` / immutable key | Update tries to change shard key fields | Don't mutate shard key; delete+insert or redesign |
| Orphaned docs after failed migrate | Range deleter lag; disk | Let range deleter finish; check recipient health |

## Pros/Cons or Trade-offs
- Dataset and write QPS still fit one primary + [[mongodb replicaset]] secondar…
- Access pattern is mostly global scans / heavy cross-entity analytics
- You cannot pick a stable shard key aligned to queries
