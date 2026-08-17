[[psql user]] [[ACL (postgreSQL)]] [[SQL/postgres]]

# psql privileges

> `GRANT` / `REVOKE` on PostgreSQL objects — tables, sequences, schemas, functions — plus default privileges for objects created later.

```txt
        psql privileges ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Operational security: least privilege, `ALTER DEFAULT PRIVILEGES`, and column…

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

- Also grant `USAGE, SELECT` on sequences backing serial/identity columns.

## Mistakes to Avoid
- **Mistake:** Granting table DML without schema `USAGE`
- **Mistake:** Skipping sequence grants for `SERIAL`/`IDENTITY` inserts
- **Mistake:** Relying on superuser in application connection strings

## Pros/Cons or Trade-offs
- **Pro:** Precise access control; defaults scale with schema growth.
- **Con:** Easy to forget defaults → works in dev (superuser), fails in prod.
- **Trade-off:** Broad schema grants vs per-table grants (simplicity vs least privilege).

## Comparison
- vs [[ACL (postgreSQL)]]: catalog/RLS theory


### Use cases
- CI migration role creates objects
