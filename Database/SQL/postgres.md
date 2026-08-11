[[Database]] [[psql essential]] [[connection pooling]] [[ACID]]

# postgres

> PostgreSQL is a relational database with strong SQL — connections, roles, and constraints are first-class ops concerns.

---

## Mental model

**Say it in one breath:** Apps use a client or a pool to talk to Postgres; roles own privileges; FKs enforce relationships but **do not** auto-create indexes on the referencing column.

```txt
App ── client | pool ──► postgres
                           │
                           ├─ roles / GRANTs
                           ├─ databases / schemas / tables
                           └─ constraints (UNIQUE, FK, CHECK)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Role** | User or group of privileges | “LOGIN roles connect; others are grant bundles.” |
| **Database / schema** | Catalog vs namespace inside it | “`public` is the default schema — still GRANT USAGE.” |
| **Pool** | Reused backends | “Web apps pool; each backend is expensive.” |
| **FK without index** | Child column may be unindexed | “We index referencing columns for deletes/joins.” |
| **Partial unique index** | UNIQUE with WHERE | “Enforce uniqueness only for non-null combos.” |
| **Cluster (pg_ctlcluster)** | Debian/Ubuntu PG instance | “Version + name (e.g. 16/main) is the unit.” |

### How the story goes (4 steps)

1. **Connect** — `psql` or driver (`host/port/user/db`).
2. **Authorize** — role + GRANT on DB/schema/tables.
3. **Model** — tables, FKs, **explicit** indexes on FK columns.
4. **Run** — pool in apps; observe with `pg_stat_activity`.

---

## Standard config / commands

```bash
sudo -u postgres psql
psql -h localhost -p 5432 -U username -d database_name
pg_lsclusters
sudo systemctl start postgresql@16-main
```

```sql
\du          -- roles
\l           -- databases
\c dbname    -- connect
\dt          -- tables
\d tablename -- columns / indexes / FKs
```

Partial unique index example:

```sql
CREATE UNIQUE INDEX unique_fsd_not_null
ON hkAppNotification (floorNumber, shiftName, department)
WHERE floorNumber IS NOT NULL
  AND shiftName IS NOT NULL
  AND department IS NOT NULL;
```

Reset a Debian cluster (destructive — lab only):

```bash
sudo pg_ctlcluster 16 main stop
# sudo pg_dropcluster 16 main          # wipes data
# sudo pg_createcluster 16 main --start
```

| Knob | Why it matters |
|------|----------------|
| Client vs pool | Scripts vs concurrent HTTP |
| FK indexes | Parent DELETE/JOIN performance |
| Cluster unit | Ubuntu packages manage versioned clusters |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Auth failed | `pg_hba.conf` + role LOGIN | Fix method/host; `\du` |
| Slow parent DELETE | FK child without index | Index referencing columns |
| Too many connections | `max_connections` / pools | Lower pool sizes; PgBouncer |
| Cluster won’t start | `pg_lsclusters` / logs | Fix port conflict; repair config |
| Unique violations on “empty” combos | NULLs in UNIQUE | Partial unique index with WHERE |

---

## Gotchas

> [!WARNING]
> **FK ≠ index in Postgres** — unlike InnoDB’s habit, you must create the child index yourself for performance.

> [!WARNING]
> **`DROP`/`createcluster` destroys data** — never run on prod without backup intent.

> [!WARNING]
> **Schema USAGE** — CONNECT on the database is not enough; grant schema privileges too.

---

## When NOT to use

- **Simple embedded single-file needs** — SQLite.
- **Pure cache / ephemeral keys** — Redis.
- **Destroy/recreate clusters to “fix” prod** — restore + diagnose instead.

---

## Related

[[psql essential]] [[connection pooling]] [[ACID]] [[SQL Configurations]] [[OLTP]] [[write-ahead logging]] [[Database mistakes]]
