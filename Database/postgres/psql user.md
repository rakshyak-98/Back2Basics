[[psql essential]] [[psql privileges]] [[ACL (postgreSQL)]] [[SQL/postgres]] [[mysql user]]

# psql user

> PostgreSQL roles (`CREATE ROLE`) — login users and groups with passwords, connection limits, and membership hierarchies.

```txt
        psql user ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Postgres treats users and groups as roles

## Sources
- [Database Roles](https://www.postgresql.org/docs/current/user-manag.html) — overview
- [CREATE ROLE](https://www.postgresql.org/docs/current/sql-createrole.html) — deep-dive

## Key Concepts
- **Role = user or group:** `LOGIN` marks a role that can connect.
- **Membership:** Groups are `NOLOGIN` roles granted to humans/apps.
- **Connection limits:** Per-role caps protect the cluster.
- **Privileges separate:** Creating a role does not grant table access ([[psql privileges]]).

## Technical Details
```sql
CREATE ROLE app_user LOGIN PASSWORD 'secret' CONNECTION LIMIT 50;
GRANT CONNECT ON DATABASE mydb TO app_user;
GRANT USAGE ON SCHEMA app TO app_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA app TO app_user;

CREATE ROLE app_read NOLOGIN;
GRANT app_read TO human_user;

\du
SELECT rolname, rolcanlogin FROM pg_roles;
```

## Mistakes to Avoid
- **Mistake:** Application login as a superuser role
- **Mistake:** Forgetting `CONNECT` / schema `USAGE` after creating a login role
- **Mistake:** Sharing one powerful role across many services

## Pros/Cons or Trade-offs
- **Pro:** One abstraction for users and groups; clean role graphs.
- **Con:** Easy to over-grant `LOGIN` on group roles by mistake.
- **Trade-off:** Password roles vs peer/cert/IAM auth in managed Postgres.

## Comparison
- vs [[mysql user]]: MySQL `user`@`host` vs Postgres roles


### Use cases
- `app_write` / `app_read` group roles
