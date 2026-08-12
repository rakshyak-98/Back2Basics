[[postgres/psql essential]] [[postgres/psql user]] [[connection pooling]]

# PostgreSQL connection errors

> PostgreSQL connection errors — client connects → libpq resolves host/port → TCP or Unix socket → Postgres postmaster spawns backend → authentication (pg_hba) → database session.

---

## Mental model

Client connects → **libpq** resolves host/port → TCP or Unix socket → Postgres **postmaster** spawns backend → **authentication** (pg_hba) → database session.

```
psql/app ──► socket/TCP:5432 ──► pg_hba.conf match ──► auth method ──► database
```

Errors before authentication are network/configuration; FATAL after connect attempt are usually role/password/database/pg_hba.

## Standard config / commands

### `role "ubuntu" does not exist`

Unix **peer** authentication maps OS user to same-named PG role.

```bash
sudo -u postgres psql -c "CREATE ROLE ubuntu WITH LOGIN SUPERUSER;"
# or connect explicitly:
psql -U postgres -h localhost
```

Fix pg_hba if you want password authentication instead:

```conf
local   all   all   scram-sha-256
```

### `password authentication failed`

```bash
psql "postgresql://myuser:wrong@localhost:5432/mydb"
sudo -u postgres psql -c "ALTER ROLE myuser WITH PASSWORD 'newpass';"
```

### `connection refused`

```bash
ss -lntp | grep 5432
sudo systemctl status postgresql
grep listen_addresses /etc/postgresql/*/main/postgresql.conf
```

### `no pg_hba.conf entry`

Log shows client IP and rejected line. Add matching rule and reload.

### `too many connections`

```sql
SELECT count(*), usename FROM pg_stat_activity GROUP BY usename;
SELECT pg_terminate_backend(pid) FROM pg_stat_activity
  WHERE state = 'idle' AND state_change < now() - interval '1 hour';
```

### SSL errors

```bash
psql "postgresql://host:5432/db?sslmode=require"
openssl s_client -connect host:5432 -starttls postgres
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `role X does not exist` | `\du`; OS username | Create role or `-U` correct user |
| `database X does not exist` | `\l` | `CREATE DATABASE`; fix connection string db name |
| Peer auth on TCP | pg_hba `local` vs `host` | Use scram/host rule for remote |
| Works psql, fails app | SSL mode; URL encoding | `sslmode`; escape password in URL |
| Intermittent timeout | Pool wait; network | [[connection pooling]] sizing; security groups |
| `FATAL: remaining connection slots` | max_connections | Kill idle; PgBouncer; raise limit |

## Gotchas

> [!WARNING]
> **Special chars in password unescaped in URL** — URL-encode `@`, `:`, `/`.

> [!WARNING]
> **`localhost` vs `127.0.0.1`** — may hit socket vs TCP different pg_hba lines.

> [!WARNING]
> **RDS requires SSL** — `sslmode=require` in prod.

## When NOT to use

- **Query/runtime SQL errors** — different class (`syntax error`, deadlock, [[postgres/postgres parameter type error]]); check application logs and `pg_stat_activity`.

## Related

[[postgres/postgres parameter type error]] [[postgres/psql user]] [[postgres/psql essential]] [[connection pooling]] [[half-open connections]]

## Permission problem

```txt
error: permission denied for database drm_streaming
code: '42501'
```
The postgreSQL user used by your backend does not have permission to connect to `drm_streaming`

- first check the database is reachable and created, and check for the role name access Privilege column
```sql
\d <database name>
```

check with `\du` if you see "Cannot login" that means you have forget to execute LOGIN when creating role
```txt
postgres=# \du
                               List of roles
   Role name   |                         Attributes
---------------+------------------------------------------------------------
 developer     |
 drm_developer | Cannot login
 drm_tester    |
 postgres      | Superuser, Create role, Create DB, Replication, Bypass RLS
 wateradmin    |
 
```
solution: `ALTER ROLE <role> LOGIN PASSWORD '<password>';`

- if not present, on login to the database access will be denied 
```
GRANT CONNECT ON DATABASE <db name> TO <role>;
```

- if the role cannot access the database table
```txt
drm_streaming=> select * from ott.users;
ERROR:  permission denied for schema ott
LINE 1: select * from ott.users;
```

```sql
SELECT has_table_privilege(
	'drm_developer',
	'ott.users',
	'SELECT'
)
```
- view all the available functions `\df`
