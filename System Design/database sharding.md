[[Distributed computing]] [[System design]] [[scaling data migration]] [[Horizontal vs Vertical Scaling]] [[connection pooling]]

# database sharding

> Database sharding splits one logical database into independent physical databases keyed by a shard column — horizontal write scale at the cost of cross-shard queries and transactions.

---

## When sharding is justified

| Signal | Rule of thumb |
|--------|---------------|
| Database size | Single node exceeds operational comfort (often terabytes) |
| Write queries per second | Primary saturated after vertical scale and tuning |
| Memory | Hot indexes no longer fit RAM |
| Operations | Backup or restore exceeds recovery time objective |

Exhaust **vertical scaling**, **read replicas**, **[[connection pooling]]**, and **[[cache system]]** before sharding — operational burden is high and **resharding** is a major [[scaling data migration]].

## Shard key selection

```txt
Good: tenant_id, user_id — high cardinality, query locality
Poor: country alone — skew (one hot shard)
Poor: created_date — all writes hit "today" shard
```

Goal: **even distribution** and **most queries single-shard**.

```python
def shard_for_user(user_id: int) -> str:
    return f"shard_{user_id % NUM_SHARDS}"

def get_user(user_id):
    db = pools[shard_for_user(user_id)]
    return db.query("SELECT * FROM users WHERE id = %s", user_id)
```

## Avoid cross-shard work

```txt
Avoid: JOIN across shards in application hot path
Prefer: denormalize tenant_id on child tables
Prefer: global lookup table (user_id → shard_id), small and cached
```

Object-relational mappers can hide scatter-gather cost until production latency explodes.

## Resharding sketch (double-write)

```txt
1. Deploy new shard map
2. Dual-write to old and new routing
3. Backfill historical rows
4. Verify checksums per shard
5. Switch reads to new map
6. Stop writes to old map
```

Plan **consistent hashing** or logical shard IDs so adding physical nodes does not require modulo churn on every row.

## Monitoring per shard

```txt
Disk utilization, queries per second, replication lag, p99 query time
Alert when one shard is 2× hotter than peers (skew)
```

## Common mistakes

| Mistake | Consequence |
|---------|-------------|
| Shard on day one | Team operates N databases without need |
| Auto-increment identifiers across shards | Collisions — use UUID or snowflake identifiers |
| Global unique email lookup | Fan-out to all shards or separate index service |
| Cross-shard two-phase commit without saga | Fragile distributed transactions |

*What breaks first?* A query that forgets the shard key and hits every partition.

## Sources

- Martin Kleppmann, *Designing Data-Intensive Applications* (O'Reilly, 2017), chapter 6 — Partitioning.
- Vitess documentation — MySQL sharding router patterns.
- AWS DynamoDB best practices — partition key design.
