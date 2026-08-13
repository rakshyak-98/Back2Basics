[[Database]] [[SQL normalization]] [[Data access patterns]] [[Database mistakes]] [[mysql table]]

# Database design

> Modeling tables, keys, and constraints so the database enforces invariants, queries stay fast, and schema changes remain possible as the product evolves.

## Start from access patterns

List the **queries and writes** the application performs before drawing entities. A normalized model that cannot serve hot paths without ten joins is a design failure ([[Data access patterns]]).

```txt
User stories ──► read/write paths ──► tables + indexes ──► constraints
```

## Core decisions

| Decision | Guiding question |
|----------|------------------|
| Primary keys | Surrogate (BIGINT/UUID) vs natural key stability |
| Foreign keys | Enforce referential integrity in DB or only in app? |
| Normalization | [[SQL normalization]] level — avoid update anomalies |
| Denormalization | Accept redundancy for read speed? Document invariants |
| Time | Store UTC `timestamptz`; never trust client clocks for expiry |

## Constraints as documentation

```sql
CREATE TABLE orders (
  id          BIGSERIAL PRIMARY KEY,
  user_id     BIGINT NOT NULL REFERENCES users(id),
  total_cents INTEGER NOT NULL CHECK (total_cents >= 0),
  status      TEXT NOT NULL CHECK (status IN ('pending','paid','shipped'))
);
```

## Migration-friendly shapes

- Prefer additive changes ([[Alter table]] ADD COLUMN) over destructive rewrites
- Use [[relocatable schema]] patterns when multiple tenants or environments share tooling
- Version schema with [[database migration]] files, not manual production DDL

## Sources

- Codd, E.F., "A Relational Model of Data for Large Shared Data Banks" (1970)
- Kleppmann, *DDIA*, Ch. 2 (data models)
- PostgreSQL Documentation — [DDL](https://www.postgresql.org/docs/current/ddl.html)
