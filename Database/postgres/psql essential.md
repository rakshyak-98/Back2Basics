[[SQL/postgres]] [[psql table]] [[psql user]] [[postgres Error]] [[SQL]]

# psql essential

> `psql` — the interactive PostgreSQL terminal for connecting, meta-commands, schema inspection, and scripting [[SQL]].





## Interview Relevance
Comfort with `\d`, `\dt`, `\timing`, and connection URIs signals you can debug without a GUI.

## Sources
- [psql](https://www.postgresql.org/docs/current/app-psql.html) — deep-dive
- [Meta-Commands](https://www.postgresql.org/docs/current/app-psql.html#APP-PSQL-META-COMMANDS) — overview

## Key Concepts
- **Connection strings:** URI or `-h/-U/-d` flags; `sslmode` for TLS.
- **Meta-commands:** Backslash commands for introspection (not sent as SQL).
- **Session GUCs:** `search_path`, `statement_timeout`, etc.
- **Client vs server COPY:** `\copy` runs client-side.

## Technical Details
```bash
psql "postgresql://user:pass@host:5432/mydb?sslmode=require"
psql -h host -U user -d mydb
```

| Command | Purpose |
|---------|---------|
| `\l` | List databases |
| `\dt` | Tables in search_path |
| `\d table` | Describe table |
| `\timing` | Show query duration |
| `\x` | Expanded output |
| `\copy` | Client-side COPY |

```sql
SET search_path TO app, public;
SET statement_timeout = '30s';
```

## Real-World Applications
Incident debugging, one-off DDL, and scripted migrations wrapped in `psql -v ON_ERROR_STOP=1 -f`.

## Pros/Cons or Trade-offs
- **Pro:** Always available, scriptable, closest to server truth.
- **Con:** Easy to run dangerous SQL on production without guardrails.
- **Trade-off:** GUI tools for exploration vs `psql` for precision and automation.

## Comparison
vs MySQL `mysql` CLI: similar role; meta-commands differ (`\d` vs `DESCRIBE` / `SHOW`).

## Mistakes to Avoid
- Forgetting `search_path` and altering the wrong schema’s tables.
- Running unrestricted scripts without `ON_ERROR_STOP`.
- Pasting passwords into shell history — prefer `.pgpass` or env-based auth.
