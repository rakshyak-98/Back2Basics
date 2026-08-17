[[Database]] [[SQL normalization]] [[Data access patterns]] [[Database mistakes]] [[mysql table]] [[Alter table]] [[database migration]] [[relocatable schema]]

# Database design

> Modeling tables, keys, and constraints so the database enforces invariants, queries stay fast, and schema changes remain possible as the product evolves.





## Interview Relevance
Design interviews judge whether you start from access patterns, choose keys/constraints deliberately, and plan migration-friendly shapes. Expect normalization vs denormalization tradeoffs and UTC/`timestamptz` hygiene.

## Sources
- Codd, E.F., "A Relational Model of Data for Large Shared Data Banks" (1970) — deep-dive
- Kleppmann, *Designing Data-Intensive Applications*, Ch. 2 — overview
- [PostgreSQL Documentation — DDL](https://www.postgresql.org/docs/current/ddl.html) — overview

## Key Concepts
- **Access patterns first:** queries and writes before entity drawings → a normalized model that needs ten joins for hot paths is a design failure ([[Data access patterns]]).
- **Keys and FKs:** surrogate vs natural; enforce referential integrity in DB when possible.
- **Normalization level:** [[SQL normalization]] to avoid update anomalies; denormalize only with documented refresh rules.
- **Migration-friendly shapes:** prefer additive [[Alter table]] changes; version with [[database migration]] files.

## Technical Details
```txt
User stories ──► read/write paths ──► tables + indexes ──► constraints
```

| Decision | Guiding question |
|----------|------------------|
| Primary keys | Surrogate (BIGINT/UUID) vs natural key stability |
| Foreign keys | Enforce referential integrity in DB or only in app? |
| Normalization | [[SQL normalization]] level — avoid update anomalies |
| Denormalization | Accept redundancy for read speed? Document invariants |
| Time | Store UTC `timestamptz`; never trust client clocks for expiry |

Constraints as documentation:

```sql
CREATE TABLE orders (
  id          BIGSERIAL PRIMARY KEY,
  user_id     BIGINT NOT NULL REFERENCES users(id),
  total_cents INTEGER NOT NULL CHECK (total_cents >= 0),
  status      TEXT NOT NULL CHECK (status IN ('pending','paid','shipped'))
);
```

Migration-friendly practices:

- Prefer additive changes ([[Alter table]] ADD COLUMN) over destructive rewrites
- Use [[relocatable schema]] patterns when multiple tenants or environments share tooling
- Version schema with [[database migration]] files, not manual production DDL

## Real-World Applications
Greenfield orders/users schema and evolving SaaS multi-tenant layouts. Example: introduce `status` with a `CHECK` constraint and an index matching the admin filter `(status, created_at)` before launch traffic arrives.

## Pros/Cons or Trade-offs
- **Pro:** Constraints catch bad writes early; clear keys make joins and migrations safer.
- **Con:** Over-normalization hurts read latency; premature denormalization creates drift without refresh rules.

## Comparison
vs [[Data access patterns]]: patterns are the workload inputs; design is the resulting tables/indexes/constraints. vs [[Database mistakes]]: mistakes catalog failure modes when design or ops ignore these principles.

## Mistakes to Avoid
- Designing only from ER diagrams without QPS and query shapes.
- Storing local time without time zone — DST and expiry bugs.
- Enforcing all integrity only in the application — drift and race windows.
- Manual production DDL instead of versioned migrations.
