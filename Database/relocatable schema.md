[[database migration]] [[Database design]] [[SQL/postgres]] [[psql essential]]

# relocatable schema

> PostgreSQL pattern: put objects in a schema you can move with `ALTER … SET SCHEMA` — useful for extensions, tenant modules, and portable fixtures.

## Interview Relevance
Shows schema-as-namespace fluency beyond `public`, including search_path pitfalls during blue/green schema cutovers.

## Sources
- [Schemas](https://www.postgresql.org/docs/current/ddl-schemas.html) — overview
- [ALTER TABLE SET SCHEMA](https://www.postgresql.org/docs/current/sql-altertable.html) — deep-dive

## Key Concepts
- **Schema namespace:** Tables live in `schema.table`; search_path resolves bare names.
- **Relocation:** `ALTER TABLE … SET SCHEMA` moves ownership of the name into another schema.
- **Side-by-side versions:** `app_v1` / `app_v2` for expand/contract cutovers.
- **Extensions:** Often install into their own schemas.

## Technical Details
```sql
CREATE SCHEMA app_v2;
CREATE TABLE app_v2.users (...);

-- Later, promote or relocate
ALTER TABLE app_v2.users SET SCHEMA public;
```

Always set `search_path` intentionally in apps and migrations (`SET search_path TO app, public`).

## Real-World Applications
Blue/green schema versions in one database; packaging logical modules; cloning schema-only dumps into test DBs.

## Pros/Cons or Trade-offs
- **Pro:** Fast logical isolation without a new cluster.
- **Con:** Cross-schema foreign keys and permissions complicate moves.
- **Trade-off:** Schema relocation vs separate databases per tenant/module.

## Comparison
vs MySQL: database/schema synonymy means “move between schemas” is a different operational story (often dump/restore between databases).

## Mistakes to Avoid
- Moving tables while apps still depend on old search_path.
- Forgetting grants after relocation.
- Assuming extension objects happily move without extension-aware procedures.
