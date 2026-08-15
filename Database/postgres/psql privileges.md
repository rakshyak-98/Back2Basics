[[psql user]] [[ACL (postgreSQL)]] [[SQL/postgres]]

# psql privileges

> `GRANT` / `REVOKE` on PostgreSQL objects — tables, sequences, schemas, functions — plus default privileges for objects created later.

## Interview Relevance
Operational security: least privilege, `ALTER DEFAULT PRIVILEGES`, and column-level grants. Sequence `USAGE` is the classic missing grant.

## Sources
- [GRANT](https://www.postgresql.org/docs/current/sql-grant.html) — deep-dive
- [Privileges](https://www.postgresql.org/docs/current/ddl-priv.html) — overview

## Key Concepts
- **Explicit GRANT/REVOKE:** Per object, per role.
- **Default privileges:** Future tables/sequences inherit grants for a creating role.
- **Column privileges:** Narrow updates to specific columns.
- **Schema USAGE:** Required to access contained objects.

## Technical Details
```sql
GRANT SELECT, INSERT ON orders TO app_user;
REVOKE DELETE ON orders FROM app_user;

ALTER DEFAULT PRIVILEGES IN SCHEMA app
  GRANT SELECT ON TABLES TO app_read;

GRANT UPDATE (status) ON orders TO fulfillment;
```

Also grant `USAGE, SELECT` on sequences backing serial/identity columns.

## Real-World Applications
CI migration role creates objects; default privileges auto-grant to `app_read` / `app_write` so deploys do not require manual re-grants.

## Pros/Cons or Trade-offs
- **Pro:** Precise access control; defaults scale with schema growth.
- **Con:** Easy to forget defaults → works in dev (superuser), fails in prod.
- **Trade-off:** Broad schema grants vs per-table grants (simplicity vs least privilege).

## Comparison
vs [[ACL (postgreSQL)]]: catalog/RLS theory; this note is day-to-day GRANT practice. vs [[mysql Privileges]]: similar verbs, different role/host model.

## Mistakes to Avoid
- Granting table DML without schema `USAGE`.
- Skipping sequence grants for `SERIAL`/`IDENTITY` inserts.
- Relying on superuser in application connection strings.
