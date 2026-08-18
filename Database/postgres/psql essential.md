[[postgres]] [[connection pooling]] [[ACID]]

# psql essential

> `psql` is Postgres’s CLI — connect, inspect, change schema, and manage roles without leaving the terminal.

## Mental model

**Say it in one breath:** Backslash commands (`\c`, `\dt`, `\d`) are `psql` meta-commands; SQL is for data and DDL — know which is which.

```txt
psql
  \c db          → switch database
  \dt / \d t     → list / describe
  SQL            → SELECT / DDL / GRANT
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **`\c`** | Connect to another DB | “Same session tool; new database context.” |
| --- | --- | --- |
| **`\d` / `\d+`** | Describe table (+ storage) | “Columns, indexes, FKs in one shot.” |
| **TRUNCATE** | Empty table fast | “Resets identity depending on options; DDL-ish locks.” |
| **GRANT chain** | CONNECT → USAGE → table privs | “Missing schema USAGE looks like ‘no tables’.” |
| **REASSIGN / DROP OWNED** | Move or drop role objects | “Required before DROP USER.” |
| **pg_terminate_backend** | Kill a session | “Drop user only after clearing backends.” |

## Standard config / commands

```sql
\conninfo
\c database_name
\l
\dt
\d table_name
\d+ table_name
```

```sql
CREATE TABLE t (id bigserial PRIMARY KEY, name text);
ALTER TABLE t ADD COLUMN col int;
ALTER TABLE t DROP COLUMN col;
TRUNCATE t;
```

```sql
CREATE USER wateradmin WITH PASSWORD 'secure_password';
GRANT CONNECT ON DATABASE your_database TO wateradmin;
GRANT USAGE, CREATE ON SCHEMA public TO wateradmin;
-- then GRANT SELECT,INSERT,... ON tables / DEFAULT PRIVILEGES as needed

ALTER USER wateradmin WITH PASSWORD 'new_password';
ALTER USER wateradmin VALID UNTIL 'infinity';
```

Drop user safely:

```sql
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE usename = 'wateradmin' AND pid <> pg_backend_pid();

REASSIGN OWNED BY wateradmin TO postgres;
DROP OWNED BY wateradmin;
DROP USER IF EXISTS wateradmin;
```

| Knob | Why it matters |

| Meta vs SQL | `\dt` won’t work in JDBC |
| --- | --- |
| Schema USAGE | Without it, `\dt` looks empty |
| Terminate backends | DROP USER fails if sessions remain |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| `\dt` empty but tables exist | `search_path` / USAGE | `\dn+`; GRANT USAGE ON SCHEMA |
| DROP USER fails | `pg_stat_activity` | Terminate; REASSIGN/DROP OWNED |
| Password auth fails | `pg_hba.conf` | Fix auth method for that host |
| Can’t connect to DB | CONNECT privilege | GRANT CONNECT ON DATABASE |
| Truncate blocked | Locks / FKs | Truncate children or CASCADE carefully |

## Gotchas

> [!WARNING]
> **Backslash commands are not SQL** — they won’t run via app drivers.

> [!WARNING]
> **DROP USER without REASSIGN/DROP OWNED** — fails if the role owns objects.

> [!WARNING]
> **TRUNCATE vs DELETE** — TRUNCATE is faster but takes stronger locks and interacts with FKs differently.

## When NOT to use

- **application runtime data access** — use a driver + pool, not shelling out to `psql`.
- **Killing backends casually in production** — can abort in-flight txns; coordinate first.
- **Granting CREATE on `public` to every application role** — tighten schema ownership in shared clusters.

## Related

[[postgres]] [[connection pooling]] [[psql user acl]] [[psql table]] [[psql database dump]] [[ACID]] [[Database mistakes]]
