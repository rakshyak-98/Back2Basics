[[database migration]] [[Database design]] [[SQL/postgres]]

# relocatable schema

> PostgreSQL pattern of creating objects inside a schema that can be moved between databases with `ALTER ... SET SCHEMA`—useful for extensions, tenant modules, and portable test fixtures.

## Mechanism

```sql
CREATE SCHEMA app_v2;
CREATE TABLE app_v2.users (...);

-- Later, promote or relocate
ALTER TABLE app_v2.users SET SCHEMA public;
```

## Use cases

- Blue/green schema versions side by side
- Packaging logical modules (similar to Oracle tablespaces conceptually)
- Test databases cloned with schema-only dumps

## Caveats

- Search path must include the schema (`SET search_path`)
- Cross-schema foreign keys complicate moves
- Extensions may install into their own schema

## Sources

- PostgreSQL Documentation — [Schemas](https://www.postgresql.org/docs/current/ddl-schemas.html)
- PostgreSQL Documentation — [ALTER TABLE SET SCHEMA](https://www.postgresql.org/docs/current/sql-altertable.html)
