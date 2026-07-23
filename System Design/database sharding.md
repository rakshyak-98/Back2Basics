[[Distributed computing]] [[System design]] [[cache system]] [[connection pooling]]

# Database sharding

> Split one logical database into independent shards — **horizontal scale when single-node limits hit**, not day-one default.

---

## Mental model

**Sharding** partitions rows across **multiple databases** by a **shard key** (user_id, tenant_id, geo). Each shard holds a **subset** of data; the application **routes** queries to the correct shard(s). Cross-shard joins and transactions become **expensive or impossible** — design around shard-local access patterns.

```txt
         Router / app layer
        /        |        \
   Shard A     Shard B     Shard C
  users 0-1M  users 1-2M  users 2-3M
```

| Signal | Threshold (rule of thumb) | Action |
|--------|---------------------------|--------|
| **DB size** | Single node > few TB | Archive or shard |
| **Table size** | Hot table billions rows | Partition/shard |
| **RAM** | Indexes don't fit memory | Shard or read replicas |
| **Ops** | Backup/restore > SLA window | Smaller shards |
| **Write QPS** | Single primary maxed | Shard writes |

**Shard key choice is permanent-ish** — resharding is a major migration ([[migration]]).

---

## Standard config / commands

### Shard key selection

```txt
Good: tenant_id, user_id (high cardinality, query locality)
Bad:  country alone (skew — US shard huge)
Bad:  created_date (all writes hit "today" shard)

Goal: even distribution + most queries single-shard
```

### App routing (pseudocode)

```python
def shard_for_user(user_id: int) -> str:
    return f"shard_{user_id % NUM_SHARDS}"

def get_user(user_id):
    db = pools[shard_for_user(user_id)]
    return db.query("SELECT * FROM users WHERE id = %s", user_id)
```

### Avoid cross-shard queries

```txt
❌ SELECT * FROM orders JOIN users ON ...  (users on other shards)
✅ Denormalize tenant_id on orders; query within tenant shard
✅ Global lookup table: user_id → shard_id (small, cached)
```

### MySQL / Postgres alternatives before shard

```txt
Read replicas for read scale
Partitioning (time-based archives)
Connection pool tuning ([[connection pooling]])
Cache hot keys ([[cache system]])
```

See also [[mysql partitioning]].

### Resharding (double-write migration sketch)

```txt
1. Add new shard map
2. Dual-write old + new
3. Backfill historical data
4. Verify checksums
5. Switch reads to new
6. Stop old writes
```

### Monitoring per shard

```txt
Disk %, QPS, replication lag, p99 query time
Alert on shard skew (one shard 2× others)
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| One shard hot | Key skew | Rehash; salt hot keys |
| Cross-shard timeout | Scatter-gather query | Redesign schema; denormalize |
| User on wrong shard | Routing bug | Consistent hash; migration table |
| Replica lag read stale | Read from replica | Read-your-writes from primary |
| Transaction fails across shards | 2PC not used | Saga / outbox pattern |
| Backup uneven | One huge shard | Rebalance |
| Connection pool exhaustion | Per-shard pools | Size pools × shard count |

---

## Gotchas

> [!WARNING]
> **Shard too early** — operational complexity kills team; exhaust vertical scale + replicas first.

> [!WARNING]
> **Monotonic user_id on single shard until overflow** — plan modulo or consistent hashing upfront.

> [!WARNING]
> **Global unique email lookup** — needs global index service or duplicate check fan-out.

> [!WARNING]
> **JOIN across shards in ORM** — ORM hides cost; explodes latency.

> [!WARNING]
> **Auto-increment IDs** — collisions across shards; use UUID/snowflake.

---

## When NOT to use

- **< 100 GB with low QPS** — single Postgres + replicas sufficient.
- **Heavy cross-entity analytics** — warehouse (OLAP) not OLTP shard.
- **Strong global transactions** — shard fights ACID across boundaries.

---

## Related

[[Distributed computing]] [[System design]] [[cache system]] [[connection pooling]] [[Eventual consistency]] [[mysql partitioning]]
