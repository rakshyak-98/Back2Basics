[[OLAP]] [[ACID]] [[connection pooling]] [[Database design]] [[Data access patterns]] [[mysql]] [[postgres essential]]

# OLTP

> Online Transaction Processing — many small, concurrent read/write operations with latency SLOs; schema normalized, indexes hot — **Designing Data-Intensive Applications** (Kleppmann, Ch. 3).

## Mental model

OLTP is the **operational path**: checkout, auth, inventory decrement, ticket update. Workload shape:

```
Many clients ──► short queries ──► indexed point/range lookups ──► ms latency
                      │
                      ├── INSERT/UPDATE/DELETE (few rows)
                      ├── FK constraints enforced
                      └── Transactions + [[ACID]] expected
```

Contrast [[OLAP]]: scan millions of rows, aggregations, columnar storage, batch ETL, seconds–minutes OK.

| Dimension | OLTP | OLAP |
|-----------|------|------|
| Query pattern | `WHERE id = ?` | `GROUP BY region, month` |
| Schema | 3NF, many tables | Star/snowflake, denormalized |
| Index strategy | B-tree on hot paths | Columnar, minimal indexes |
| Consistency | Strong, transactional | Eventual / snapshot OK |
| Scale lever | Read replicas, sharding, pooling | Warehouse, column store |

**One database doing both** without separation → reporting queries lock/contend with checkout. Pattern: OLTP primary + CDC/replica → OLAP warehouse.

## Standard config / architecture

### Connection path (every ms counts)

```
App ──► pool (PgBouncer / HikariCP / pgxpool) ──► primary
         │
         └── avoid: new TCP + auth per HTTP request
```

See [[connection pooling]] — pool size ≈ `(cores * 2) + spindle`, not `threads * 10`.

### Index discipline

- Composite index column order matches **equality filters first, then range, then ORDER BY**.
- Cover hot queries — see [[covering index]].
- Drop unused indexes (`performance_schema` / `pg_stat_user_indexes`).

### Read scaling

```
        ┌── replica (read-only, lag seconds)
Primary ┤
        └── replica
```

- Route **read-your-writes** paths to primary (session after login, post-checkout receipt).
- Replicas for dashboards, search autocomplete — tolerate lag label in UI.

### Sharding (when single primary dies)

Shard key = tenant_id / user_id — co-locate related rows. Cross-shard joins are expensive; design them out.

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| p99 latency spike, CPU low | Lock waits: PG `pg_locks`, MySQL `innodb_lock_waits` | Shorten txs; index the WHERE; kill idle in transaction |
| Connection storm | `max_connections`; pool exhaustion | PgBouncer; lower app pool; raise PG max carefully |
| Replica lag growing | `pg_stat_replication`; long queries on replica | Kill analytics on replica; parallel apply; bigger replica |
| Single query melts CPU | `EXPLAIN ANALYZE`; missing index | Add index; rewrite N+1 to batch JOIN |
| Write throughput ceiling | WAL/checkpoint metrics; disk IOPS | Faster disk; batch writes; partition; async where safe |
| "Works in dev" | Dev has 100 rows; prod seq scan | Load test with realistic cardinality |

## Gotchas

> [!WARNING]
> **ORM N+1** — 1 HTTP request → 200 queries. OLTP killer at scale. Use JOIN, `IN (...)`, or dataloaders.

> [!WARNING]
> **SELECT *** on wide rows** — breaks covering indexes, fills network. Project columns explicitly.

- **Hot row updates** — single counter (`UPDATE views SET n=n+1`) serializes; use sharded counters or async aggregate.
- **Advisory locks forgotten** — migration tool holds lock; OLTP blocked for minutes.
- **UUID v4 PK** — random insert pattern fragments B-tree; consider v7/sequential or `BIGSERIAL`.
- **Long transactions + MVCC** — bloat, replication slot hold, undo log growth.
- **Caching without invalidation** — OLTP reads stale inventory; cache TTL ≠ consistency.

## When NOT to use

- **Heavy analytics on OLTP primary** — export to warehouse / materialized view on replica.
- **Document store for money movement** — use relational OLTP + constraints unless you know the compensating patterns.
- **Graph traversal at OLTP latency** — relationship DB or dedicated graph tier.

## Related

[[OLAP]] [[ACID]] [[Data access patterns]] [[Database design]] [[connection pooling]] [[mysql index]] [[MVCC]] [[migration]]
