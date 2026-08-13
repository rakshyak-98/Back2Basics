<!-- note-strategy: operational -->
[[postgres]] [[psql essential]] [[ACL (postgreSQL)]]

# psql table

> Postgres tables live in schemas; `updated_at` needs a trigger (no MySQL-style `ON UPDATE CURRENT_TIMESTAMP` column attribute).

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Database → schemas → tables; unqualified names follow `search_path`. Auto `updated_at` = `BEFORE UPDATE` trigger function that sets `NEW.updated_at`.

```txt
Server
└── Database
    ├── Schema public
    │     └── users
    └── Schema sales
          └── orders
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Schema** | Namespace inside a DB | “Not the same as MySQL ‘schema’=database.” |
| **search_path** | Resolution order | “Omitting schema uses path.” |
| **Trigger for updated_at** | No ON UPDATE column attr | “We write a small PL/pgSQL trigger.” |
| **OWNER** | Role that owns the table | “Owns ALTER/DROP by default.” |

---

## Standard config / commands

```sql
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_timestamp
BEFORE UPDATE ON your_table_name
FOR EACH ROW
EXECUTE FUNCTION update_modified_column();

CREATE SCHEMA IF NOT EXISTS ott;
SET search_path TO ott, public;
GRANT USAGE ON SCHEMA sales TO analyst;

\dn
\dt sales.*
```

| Knob | Why it matters |
|------|----------------|
| `search_path` | Avoid hardcoding schema in every query |
| `EXECUTE FUNCTION` vs `PROCEDURE` | PG15+ naming; older used `EXECUTE PROCEDURE` |
| `DROP SCHEMA … CASCADE` | Wipes all objects — intentional only |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| relation does not exist | `search_path` / schema | Qualify `sales.orders` or SET path |
| updated_at stale | No trigger | Add BEFORE UPDATE trigger |
| Permission denied for schema | USAGE missing | GRANT USAGE ON SCHEMA |
| Wrong table same name | Multiple schemas | Always qualify in migrations |

---

## Gotchas

> [!WARNING]
> **MySQL muscle memory** — Postgres won’t auto-bump timestamps from a column attribute alone.

> [!WARNING]
> **`public` default grants** — harden in prod; don’t assume PUBLIC is empty.

---

## When NOT to use

- **One schema forever with three tables** — `public` is fine; don’t invent namespaces for sport.
- **application-enforced updated_at only** — races; prefer trigger or DB default patterns you control.

---

## Related

[[psql essential]] [[ACL (postgreSQL)]] [[psql database dump]] [[postgres]]
