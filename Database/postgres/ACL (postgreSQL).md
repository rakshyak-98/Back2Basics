[[psql privileges]] [[psql user]] [[mysql Privileges]]

# ACL (postgreSQL)

> PostgreSQL access control lists—catalog-stored privileges on every object, evaluated per statement based on role membership and `SET ROLE`.

## ACL column

```sql
SELECT relname, relacl FROM pg_class WHERE relname = 'orders';
```

Shows grantee/grantor privilege letters (`arwdDxt` for tables).

## Object types

| Object | Privileges |
|--------|------------|
| Table | SELECT, INSERT, UPDATE, DELETE, TRUNCATE, REFERENCES, TRIGGER |
| Sequence | USAGE, SELECT, UPDATE |
| Schema | USAGE, CREATE |
| Function | EXECUTE |

## Row Level Security

RLS policies further restrict visible rows per role—orthogonal to table GRANT.

## Sources

- PostgreSQL Documentation — [Privileges](https://www.postgresql.org/docs/current/ddl-priv.html)
- PostgreSQL Documentation — [Row Security Policies](https://www.postgresql.org/docs/current/ddl-rowsecurity.html)
