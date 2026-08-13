[[SQL/postgres]] [[psql table]] [[psql user]] [[postgres Error]]

# psql essential

> `psql` interactive terminal—connect, run meta-commands, inspect schema, and script [[SQL]] against PostgreSQL.

## Connect

```bash
psql "postgresql://user:pass@host:5432/mydb?sslmode=require"
psql -h host -U user -d mydb
```

## Meta-commands

| Command | Purpose |
|---------|---------|
| `\l` | List databases |
| `\dt` | Tables in search_path |
| `\d table` | Describe table |
| `\timing` | Show query duration |
| `\x` | Expanded output |
| `\copy` | Client-side COPY |

## Useful session settings

```sql
SET search_path TO app, public;
SET statement_timeout = '30s';
```

## Sources

- PostgreSQL Documentation — [psql](https://www.postgresql.org/docs/current/app-psql.html)
- PostgreSQL Documentation — [Meta-Commands](https://www.postgresql.org/docs/current/app-psql.html#APP-PSQL-META-COMMANDS)
