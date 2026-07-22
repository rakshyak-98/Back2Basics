[[MongoDB]] [[mongodb connection]] [[Database/ACID]]

# MongoDB replica set

> Primary + secondaries + oplog for durability and automatic failover — **MongoDB Manual** (Kleppmann-style distributed ops).

## Mental model

A replica set is a group of mongod processes that replicate the same data. One **primary** accepts writes; **secondaries** pull from the primary's **oplog** (capped collection of operations). **Arbiters** vote in elections but hold no data. Members heartbeat each other; primary loss triggers election (~seconds).

```
Client writes → Primary → oplog
                ↓ replicate
            Secondaries (async lag possible)
            Arbiter (vote only)
```

| Role | Writes | Reads | Data |
|------|--------|-------|------|
| Primary | Yes | Yes | Full |
| Secondary | No | Yes (if allowed) | Full |
| Arbiter | No | No | None |

## Standard config / commands

### Initiate (lab / first deploy)

```js
rs.initiate({
  _id: 'rs0',
  members: [
    { _id: 0, host: 'mongo1:27017' },
    { _id: 1, host: 'mongo2:27017' },
    { _id: 2, host: 'mongo3:27017', arbiterOnly: true },
  ],
});
```

### Operations checklist

```js
rs.status()                    // health, lag, primary
rs.conf()                      // member config
rs.add('mongo4:27017')         // add secondary
rs.stepDown(60)                // planned maintenance failover
db.printReplicationInfo()      // oplog window
```

### Connection string (app)

```
mongodb://user:pass@mongo1,mongo2,mongo3/mydb?replicaSet=rs0&w=majority
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| No primary / RECOVERING | `rs.status()` | Fix network; restore member; re-sync secondary |
| High replication lag | `rs.printSlaveReplicationInfo()` | Scale primary load; disk I/O; index hot writes |
| Rollback after failover | Logs "rollback" | Re-sync affected secondary from backup |
| Split-brain (two primaries) | `rs.conf()` priorities, votes | Odd number of voting members; fix network partition |
| Writes fail during election | Brief window | Retry with backoff; tune `serverSelectionTimeoutMS` |
| Arbiter-only RS (even count) | Design review | Prefer 3 data-bearing nodes; arbiter is cost hack with risk |

## Gotchas

> [!WARNING]
> **Read from secondary without `secondaryOk`** — driver defaults to primary for consistency.
>
> **Write concern `{ w: 1 }` only** — ack from primary ≠ replicated; data loss if primary dies before replicate.
>
> **Hidden/delayed secondaries** — good for DR/analytics; don't point prod reads at delayed node.

## When NOT to use

- Don't run production on standalone mongod — no failover, no oplog backup story.
- Don't use arbiters as a substitute for a third data node when you care about durability.

## Related

[[mongodb connection]] [[Database/WAL (Write-Ahead Log)]] [[connection pooling]]
