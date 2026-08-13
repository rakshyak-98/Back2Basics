[[psql essential]] [[psql privileges]] [[ACL (postgreSQL)]] [[SQL/postgres]]

# psql user

> PostgreSQL roles (`CREATE ROLE`)—login users and groups with password, connection limits, and membership in role hierarchies.

## Create role

```sql
CREATE ROLE app_user LOGIN PASSWORD 'secret' CONNECTION LIMIT 50;
GRANT CONNECT ON DATABASE mydb TO app_user;
GRANT USAGE ON SCHEMA app TO app_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA app TO app_user;
```

## Roles as groups

```sql
CREATE ROLE app_read NOLOGIN;
GRANT app_read TO human_user;
```

## Inspect

```sql
\du
SELECT rolname, rolcanlogin FROM pg_roles;
```

PostgreSQL uses **roles** for both users and groups (unlike MySQL `user`@`host`).

## Sources

- PostgreSQL Documentation — [Database Roles](https://www.postgresql.org/docs/current/user-manag.html)
- PostgreSQL Documentation — [CREATE ROLE](https://www.postgresql.org/docs/current/sql-createrole.html)
