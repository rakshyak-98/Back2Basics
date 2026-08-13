[[psql user]] [[ACL (postgreSQL)]] [[SQL/postgres]]

# psql privileges

> `GRANT` / `REVOKE` on PostgreSQL objects—tables, sequences, schemas, functions—with default privileges for future objects.

## Table privileges

```sql
GRANT SELECT, INSERT ON orders TO app_user;
REVOKE DELETE ON orders FROM app_user;
```

## Default privileges

```sql
ALTER DEFAULT PRIVILEGES IN SCHEMA app
  GRANT SELECT ON TABLES TO app_read;
```

## Column-level

```sql
GRANT UPDATE (status) ON orders TO fulfillment;
```

## Sources

- PostgreSQL Documentation — [GRANT](https://www.postgresql.org/docs/current/sql-grant.html)
- PostgreSQL Documentation — [Privileges](https://www.postgresql.org/docs/current/ddl-priv.html)
