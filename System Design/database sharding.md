[[Distributed computing]] [[System design]] [[scaling data migration]] [[Horizontal vs Vertical Scaling]] [[connection pooling]] [[cache system]]

# database sharding

> Database sharding splits one logical database into independent physical databases keyed by a shard column — horizontal write scale at the cost of cross-shard queries and transactions.

## Interview Relevance

When to shard, how to pick a shard key, avoid cross-shard joins, and sketch a safe reshard (dual-write) plan.

## Sources

- Martin Kleppmann, *Designing Data-Intensive Applications*, ch. 6 Partitioning — deep-dive
- Vitess documentation — MySQL sharding patterns — deep-dive
- AWS DynamoDB best practices — partition key design — overview

## Key Concepts

- **Justify first:** size, write QPS, RAM, backup RTO — after vertical/replicas/pool/cache.
- **Shard key:** high cardinality + query locality; avoid skew.
- **Single-shard queries:** goal for hot paths.
- **Resharding:** dual-write + backfill + checksum + cutover ([[scaling data migration]]).

## Technical Details

| Signal | Rule of thumb |
|--------|---------------|
| DB size | Beyond operational comfort (often TB) |
| Write QPS | Primary saturated after scale-up/tuning |
| Memory | Hot indexes no longer fit RAM |
| Ops | Backup/restore exceeds RTO |

```txt
Good: tenant_id, user_id
Poor: country alone (skew); created_date (all writes hit “today”)
```

```python
def shard_for_user(user_id: int) -> str:
    return f"shard_{user_id % NUM_SHARDS}"
```

Avoid cross-shard JOINs; denormalize tenant_id; keep global lookup (user→shard) small/cached. Prefer consistent hashing / logical shard IDs over raw modulo churn.

```txt
1. Deploy new shard map
2. Dual-write old+new
3. Backfill
4. Checksums
5. Switch reads
6. Stop old writes
```

Monitor per-shard disk/QPS/lag/p99; alert on 2× skew.

| Mistake | Consequence |
|---------|-------------|
| Shard day one | N DBs without need |
| Auto-increment across shards | Collisions — UUID/snowflake |
| Global unique email | Fan-out or separate index service |
| Naive 2PC | Fragile distributed tx |

## Real-World Applications

Multi-tenant SaaS, Vitess/Citus rollouts, and DynamoDB partition design.

## Pros/Cons or Trade-offs

- **Pro:** Write scale beyond one primary.
- **Con:** Cross-shard pain; reshard migrations; ops surface.
- **Trade-off:** modulo simplicity vs consistent-hash flexibility.

## Comparison

- vs [[Horizontal vs Vertical Scaling]]: sharding is the write-scale horizontal lever.
- vs read replicas: replicas help reads only.

## Mistakes to Avoid

- Queries that forget the shard key and scatter to all partitions.
- Hot keys that pin one shard.
- Treating ORM “transparency” as free cross-shard joins.
