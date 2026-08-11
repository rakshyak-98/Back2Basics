[[ACID]] [[covering index]] [[mysql index]] [[connection pooling]] [[Data access patterns]] [[WAL (Write-Ahead Log)]]

# Database mistakes

> Schema and modeling errors that pass code review but fail in production — **Kleppmann (DDIA)** + years of migration pain.

---

## Mental model

Most production DB pain is **modeling and access-pattern mismatch**, not missing indexes alone.

```txt
App assumes: flexible, mutable, fast joins
Reality:       migrations lock, rows are wide, history vanishes, FKs cascade at 3am
```

Design for **how data is queried and how it changes** — not how objects look in application code.

---

## Standard config / commands

### Surrogate primary keys (not business natural keys)

```sql
-- ❌ Business key as PK — value changes, merges, regional formats
CREATE TABLE users (
  email VARCHAR(255) PRIMARY KEY
);

-- ✅ Surrogate + unique on business key
CREATE TABLE users (
  id BIGSERIAL PRIMARY KEY,
  email VARCHAR(255) NOT NULL UNIQUE
);
```

**Why:** email changes, SSO linkage, GDPR erasure — entity identity must survive attribute changes.

### Never store derived age

```sql
-- ❌ Stale on birthday
age INT

-- ✅ Store birth date; compute in query or app
birth_date DATE NOT NULL
-- SELECT age(birth_date) or date diff at read time
```

### Optional type-specific columns (sparse matrix)

```sql
-- ❌ phone_type_1, phone_type_2, fax, fax2 ...
-- ✅ EAV or JSONB with check constraints — or separate child table
CREATE TABLE contact_methods (
  user_id BIGINT REFERENCES users(id),
  kind TEXT CHECK (kind IN ('email','phone','slack')),
  value TEXT NOT NULL,
  PRIMARY KEY (user_id, kind, value)
);
```

### Referential integrity at DB layer

```sql
CREATE TABLE orders (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE RESTRICT
);
-- App-only FK checks race under concurrency
```

### Money as integer minor units

```sql
amount_cents BIGINT NOT NULL,
currency CHAR(3) NOT NULL,
CHECK (amount_cents >= 0)
-- Never FLOAT/DOUBLE for money
```

### Soft delete vs hard delete

```sql
deleted_at TIMESTAMPTZ NULL
-- Index partial: WHERE deleted_at IS NULL
-- Every query must filter — enforce in ORM scope or views
```

### Migration safety

```sql
-- Expand-contract pattern for column renames
-- 1. Add new column
-- 2. Dual-write in app
-- 3. Backfill
-- 4. Switch reads
-- 5. Drop old column
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Duplicate "unique" business rows | Missing UNIQUE | Add constraint; dedupe script; merge strategy |
| Orphan child rows | FK not enforced | Add FK RESTRICT; backfill parents |
| Report numbers wrong vs finance | Float money / timezone dates | Minor units; `TIMESTAMPTZ`; store UTC |
| Migration locked prod hours | `ACCESS EXCLUSIVE` | `CONCURRENTLY` indexes; online schema tools |
| Query slow after "simple" feature | Full table scan new filter | Index matching [[Data access patterns]]; EXPLAIN |
| Cascade deleted half catalog | ON DELETE CASCADE | Change to RESTRICT; soft delete |
| JSON column unqueryable slow | No GIN index | Index paths you filter; normalize hot fields |
| Connection storms | No [[connection pooling]] | PgBouncer / RDS proxy; fix connection leaks |

---

## Gotchas

> [!WARNING]
> **UUID v4 as PK on Postgres** — random insert order fragments B-tree; consider UUIDv7/time-ordered or BIGSERIAL.

> [!WARNING]
> **Polymorphic associations** (`commentable_type`, `commentable_id`) — no FK; orphans guaranteed — use join tables or STI with constraints.

> [!WARNING]
> **Storing lists in CSV column** — can't index elements; can't query sanely — normalize or JSONB + GIN.

> [!WARNING]
> **Default `NULL` for "empty"** — three-valued logic bugs; prefer NOT NULL + sentinel or separate table.

> [!WARNING]
> **Optimistic locking omitted** — lost updates when two tabs save — add `version` column or `updated_at` check.

---

## When NOT to use

- **Over-normalizing read-heavy dashboards** — materialized views or OLAP store ([[OLAP]]) for analytics.
- **JSONB for every column** — loses constraints; schema drift without migration discipline.
- **Premature sharding** — fix indexes and query shapes first ([[covering index]]).

---

## Related

[[ACID]] · [[connection pooling]] · [[covering index]] · [[mysql index]] · [[Data access patterns]] · [[WAL (Write-Ahead Log)]] · [[psql essential]]
