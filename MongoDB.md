[[mongosh]] [[mongoose/mongoose]] [[mongodb connection]] [[mognodb indexing]] [[mongodb replicaset]] [[mongodb sharding]] [[INDEX]]

# MongoDB

> MongoDB is a document database — flexible JSON-like documents, horizontal scale via sharding, and replica sets for failover; the first production pain is usually schema drift, index misses, or connection pool exhaustion.

---

## What MongoDB provides

MongoDB stores **BSON documents** in collections. Unlike rigid relational rows, documents can vary in shape within a collection (schema flexibility), with **indexes** for query paths and **replication** for availability.

| Capability | Vault notes |
|------------|-------------|
| Shell & admin | [[mongosh]] · [[mongodb shell]] |
| Application ODM | [[mongoose/mongoose]] · [[mongoose schema]] |
| Connections | [[mongodb connection]] · pool sizing in app layer |
| Indexes | [[mognodb indexing]] |
| High availability | [[mongodb replicaset]] |
| Scale-out | [[mongodb sharding]] |
| Query patterns | [[mongosh query]] · [[MongoDB data populate]] |

```txt
App ──► driver pool ──► mongod (primary)
                           │
                           ├── secondary replicas ([[mongodb replicaset]])
                           └── shard routers if sharded ([[mongodb sharding]])
```

## Where to go next

| Symptom / need | Go to |
|----------------|-------|
| Slow queries | [[mognodb indexing]] · explain plans in [[mongosh query]] |
| Failover / elections | [[mongodb replicaset]] |
| Connection storms | [[mongodb connection]] |
| Schema migrations | [[mongodb migration]] |
| Aggregation / `$lookup` | [[mongodb lookup query]] · [[mongoDB Group query]] |

## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| `MongoServerSelectionError` | Replica set health; DNS | Fix primary; verify `replicaSet` URI |
| Query timeout | Missing index; collscan | Add compound index; review [[mognodb indexing]] |
| Duplicate key | Unique index vs app idempotency | Align `_id` generation; upsert pattern |
| OOM on mongod | WiredTiger cache | Lower cache GB; add RAM or shard |
| Stale reads after write | Read preference `secondary` | Use `primary` for read-your-writes |

## Sources

- [MongoDB Manual — Introduction](https://www.mongodb.com/docs/manual/introduction/)
- [Wikipedia — MongoDB](https://en.wikipedia.org/wiki/MongoDB)
