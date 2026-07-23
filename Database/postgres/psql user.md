[[postgres/psql essential]] [[postgres/psql keywords]] [[mysql/mysql user]] [[IAM]]

# PostgreSQL users & roles

> One-line: Postgres **roles** unify users and groups — login role = user; grant least privilege; never app-connect as superuser.

## Mental model

Postgres uses **roles**. A role with `LOGIN` is a user. Roles can **inherit** membership in other roles (group pattern). Permissions attach to roles on databases, schemas, tables, sequences.

```
CREATE ROLE app_user LOGIN PASSWORD '…'
GRANT CONNECT ON DATABASE mydb TO app_user
GRANT USAGE ON SCHEMA public TO app_user
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO app_user
```

Default superuser `postgres` is for admin — apps use scoped role. Peer auth on Unix socket maps OS user → PG role (common source of "role does not exist" errors).

## Standard config / commands

### psql meta-commands

```sql
\du          -- list roles
\du+         -- with descriptions
\l           -- databases
\c mydb      -- connect
\dp          -- table privileges
```

### Create app user + database

```sql
CREATE ROLE myuser WITH LOGIN PASSWORD 'strong-password' NOSUPERUSER NOCREATEDB;
CREATE DATABASE mydb OWNER myuser;
GRANT CONNECT ON DATABASE mydb TO myuser;
```

### Schema grants (Postgres 15+ public schema)

```sql
REVOKE CREATE ON SCHEMA public FROM PUBLIC;  -- harden default
GRANT USAGE ON SCHEMA public TO myuser;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO myuser;
```

### Role flags (use sparingly)

```sql
ALTER ROLE myuser CREATEDB;      -- can create databases
ALTER ROLE myuser WITH SUPERUSER; -- break-glass only
```

### Change password

```sql
ALTER ROLE myuser WITH PASSWORD 'new-secret';
```

### pg_hba.conf auth modes

```conf
# TYPE  DATABASE  USER     ADDRESS       METHOD
local   all       postgres               peer
host    mydb      myuser   10.0.0.0/8    scram-sha-256
```

Reload after edit: `SELECT pg_reload_conf();`

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `role "ubuntu" does not exist` | Peer auth uses OS username | Create role; or `-U postgres`; fix pg_hba |
| `password authentication failed` | Wrong secret; scram vs md5 | Reset password; align pg_hba method |
| `permission denied for table` | Missing GRANT | Grant table/sequence; default privileges |
| `must be owner` | DDL as app user | Migration role separate from runtime role |
| Too many connections one user | No pool | [[connection pooling]]; lower app pool max |
| `remaining connection slots` | Superuser reserved | Terminate idle; raise max_connections carefully |

## Gotchas

> [!WARNING]
> **SUPERUSER in app connection string** — full cluster compromise on SQL injection.

> [!WARNING]
> **Peer auth surprise** — `psql` as ubuntu tries role ubuntu, not postgres.

> [!WARNING]
> **Public schema CREATE granted to PUBLIC by old defaults** — revoke on new clusters.

## When NOT to use

- **IAM DB auth (RDS/IAM)** — token-based user still maps to PG role; different connection flow.
- **Row-level security** — complements grants; see app-specific policies.

## Related

[[postgres/postgres Error]] [[postgres/psql essential]] [[connection pooling]] [[mysql/mysql user]]
