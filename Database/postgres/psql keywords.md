[[postgres]] [[Database]] [[OLTP]] [[ACID]]

# PostgreSQL UPSERT keywords (EXCLUDED / conflict)

> `INSERT … ON CONFLICT` pseudo-table names — `EXCLUDED` is the proposed row that lost the conflict; misuse causes silent wrong updates or duplicate key errors.

## Mental model

PostgreSQL upsert = insert row; if unique/exclusion constraint violated, **do conflict action** instead of error.

```
INSERT new row ──► conflict on UNIQUE/PRIMARY KEY?
                         │
            YES ──► DO UPDATE / DO NOTHING
                         │
                   EXCLUDED = the row you tried to INSERT
                   table   = existing stored row
```

`EXCLUDED` exists **only** inside `ON CONFLICT DO UPDATE SET` — not in `DO NOTHING`, not in general queries.

## Standard config / commands

### Basic upsert

```sql
INSERT INTO users (id, email, name, updated_at)
VALUES (1, 'a@example.com', 'Alice', NOW())
ON CONFLICT (id) DO UPDATE SET
  email      = EXCLUDED.email,
  name       = EXCLUDED.name,
  updated_at = EXCLUDED.updated_at;
```

### Conflict target required for partial indexes

```sql
-- Unique index: CREATE UNIQUE INDEX uq_active_email ON users(email) WHERE deleted_at IS NULL;

INSERT INTO users (email, name)
VALUES ('a@example.com', 'Alice')
ON CONFLICT (email) WHERE deleted_at IS NULL
DO UPDATE SET name = EXCLUDED.name;
```

### DO NOTHING (idempotent insert)

```sql
INSERT INTO visit_log (user_id, day)
VALUES (42, CURRENT_DATE)
ON CONFLICT (user_id, day) DO NOTHING;
-- EXCLUDED not available here
```

### Conditional update (don't overwrite with stale data)

```sql
ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name
WHERE users.updated_at < EXCLUDED.updated_at;
```

### RETURNING

```sql
INSERT INTO counters (k, v) VALUES ('hits', 1)
ON CONFLICT (k) DO UPDATE SET v = counters.v + 1
RETURNING v;
```

### Multiple columns / composite key

```sql
ON CONFLICT (tenant_id, external_id) DO UPDATE SET
  payload = EXCLUDED.payload;
```

### vs `MERGE` (SQL:2023 / PG 15+)

```sql
-- MERGE is separate syntax for match/not-match; ON CONFLICT remains common for simple upserts
MERGE INTO inventory t
USING (VALUES ('sku1', 5)) AS s(sku, qty)
ON t.sku = s.sku
WHEN MATCHED THEN UPDATE SET qty = t.qty + s.qty
WHEN NOT MATCHED THEN INSERT (sku, qty) VALUES (s.sku, s.qty);
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `EXCLUDED` undefined error | Used outside DO UPDATE | Only reference in UPDATE SET / WHERE of upsert |
| Duplicate key still thrown | No matching conflict target | Add UNIQUE index; specify `(columns)` matching constraint |
| Upsert never updates | DO NOTHING or WHERE false | Use DO UPDATE; relax WHERE |
| Partial index not used | ON CONFLICT missing predicate | Mirror `WHERE` from index definition |
| Wrong row updated | Conflict target too narrow | Align ON CONFLICT cols with actual UNIQUE constraint |
| Serial/id overwritten | `id = EXCLUDED.id` in UPDATE | Omit immutable PK from SET list |
| Deadlock with concurrent upserts | Multiple rows lock order | Consistent key order; retry; reduce batch size |

## Gotchas

> [!WARNING]
> **`EXCLUDED` ≠ `NEW` (triggers)** — triggers use `NEW`/`OLD`; upsert uses `EXCLUDED` for proposed insert row.

> [!WARNING]
> **Constraint must exist** — `ON CONFLICT` requires a unique or exclusion constraint matching the conflict target; otherwise syntax/runtime error.

> [!WARNING]
> **Immutable column accidents** — `SET id = EXCLUDED.id` can break FK references; update only mutable columns.

> [!WARNING]
> **Replica identity / logical replication** — heavy upsert workloads need proper indexes; conflicts on subscribers differ in logical replication setups.

## When NOT to use

- **Bulk load initial data** — `COPY` + swap table faster than row-wise upsert.
- **Complex merge rules across tables** — use explicit transaction with SELECT FOR UPDATE or `MERGE`.
- **MySQL portability** — MySQL uses `ON DUPLICATE KEY UPDATE VALUES(col)` — different keyword (`VALUES` not `EXCLUDED`).

## Related

[[postgres]] [[Database]] [[OLTP]] [[ACID]] [[mysql]]
