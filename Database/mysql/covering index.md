[[mysql index]] [[mysql query]] [[show query]] [[OLTP]] [[MySQL storage]]

# covering index

> Secondary index that contains **all columns the query needs** — InnoDB skips the clustered-index lookup — **High Performance MySQL** (Schwartz et al.).

## Mental model

InnoDB secondary indexes store `(index_cols…, PK)` in a B+ tree. Non-covering query:

```
Secondary index seek → collect PKs → random I/O into clustered index (bookmark lookup) → row
```

Covering index:

```
Secondary index seek → all columns already in leaf → done (Using index in EXPLAIN)
```

```
Query: SELECT status, created_at FROM orders WHERE user_id = 42;

Index (user_id)           Index (user_id, status, created_at)  ← covering
     │                              │
     └── needs clustered lookup     └── answer in index leaf
```

**Trade-off:** wider index = more disk, slower writes, better read latency. Add columns you SELECT/WHERE, not entire table.

## Standard config / DDL

### MySQL 8.0+ — invisible columns via INCLUDE-style pattern

MySQL has no separate `INCLUDE` clause like SQL Server/Postgres. **Add columns to the index** or use **generated invisible column** tricks sparingly.

```sql
-- Cover: WHERE user_id = ? RETURNING status, created_at
CREATE INDEX idx_orders_user_status_created
  ON orders (user_id, status, created_at);

-- Prefix-friendly: equality cols left, range right
CREATE INDEX idx_events_tenant_time
  ON events (tenant_id, event_type, created_at);
```

### Before MySQL 8.0

Only option: add trailing columns to index definition (same as covering, just no optimizer hints like `INCLUDE`).

```sql
-- Bad: index only user_id, query selects title, body
CREATE INDEX idx_posts_user ON posts (user_id);

-- Good
CREATE INDEX idx_posts_user_cover ON posts (user_id, title);  -- body too large? don't cover blobs
```

### EXPLAIN patterns (memorize these)

```sql
EXPLAIN FORMAT=TRADITIONAL
SELECT status, created_at FROM orders WHERE user_id = 42;
```

| Extra column | Meaning |
|--------------|---------|
| `Using index` | **Covering** — no clustered lookup |
| `Using index condition` | Index Condition Pushdown (ICP) — filters in index, may still lookup |
| `Using where` | Filter after index access — often needs clustered read |
| `Using filesort` | Sort not satisfied by index order — check composite order |

```sql
-- JSON + detailed tree (8.0.18+)
EXPLAIN ANALYZE SELECT status, created_at FROM orders WHERE user_id = 42;

-- Index usage stats — find dead indexes
SELECT object_schema, object_name, index_name, count_star
FROM performance_schema.table_io_waits_summary_by_index_usage
WHERE index_name IS NOT NULL
ORDER BY count_star DESC;
```

### Composite index column order

```sql
-- Query: WHERE tenant_id = 1 AND status = 'open' ORDER BY created_at DESC
CREATE INDEX idx ON tickets (tenant_id, status, created_at);
-- NOT (created_at, tenant_id) — left-prefix rule breaks
```

Rule: **equality → equality → range → ORDER BY columns** in one index.

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Query fast in staging, slow in prod | `EXPLAIN ANALYZE`; rows examined vs returned | Add/adjust covering index; fix cardinality stats (`ANALYZE TABLE`) |
| Index exists but not used | Wrong column order; function on column (`LOWER(email)`) | Match index to predicate; generated stored column |
| `Using index` but still slow | Index too wide (many BIGINT+TEXT); buffer pool cold | Trim covered cols; warm cache; partition |
| Writes degraded after "fix" | Too many secondary indexes | Cover only top 3 read paths; drop unused |
| Optimizer picks wrong index | `optimizer_switch`; stale stats | `ANALYZE TABLE`; `FORCE INDEX` as last resort in query hint |

## Gotchas

> [!WARNING]
> **`SELECT *` kills covering** — pulls every column; optimizer must hit clustered index. List columns explicitly in API/ORM selects.

> [!WARNING]
> **Covering TEXT/BLOB** — InnoDB may require overflow pages; index-only access partial. Prefer hash/id lookup for large payloads.

- **Secondary index includes PK implicitly** — `(user_id)` index already carries PK for lookup; covering means *non-PK SELECT list* cols.
- **Low-cardinality leading column** — index `(status, user_id)` when `status` has 3 values → optimizer may ignore.
- **Duplicate indexes** — `(a,b)` makes `(a)` redundant for reads but MySQL won't auto-drop; maintenance cost doubles.
- **`ORDER BY` mismatch** — `DESC` vs index ASC may filesort unless 8.0+ descending indexes defined.

## When NOT to use

- **Wide rows / rare query** — index size exceeds benefit; accept lookup cost.
- **Write-heavy table** — every extra indexed column slows INSERT/UPDATE.
- **Covering every report query** — move analytics to replica/warehouse ([[OLAP]]).

## Related

[[mysql index]] [[mysql query]] [[show query]] [[OLTP]] [[MySQL storage]] [[partitioning]]
