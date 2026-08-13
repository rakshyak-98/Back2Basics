[[SQL/postgres]] [[mysql dump]] [[database migration]]

# psql database dump

> Logical backups with `pg_dump` and `pg_dumpall`—schema, data, and globals for restore, cloning, and version upgrades.

## Database dump

```bash
pg_dump -h host -U backup -Fc mydb > mydb.dump   # custom format
pg_dump -h host -U backup --schema-only mydb > schema.sql
```

## Restore

```bash
pg_restore -d mydb mydb.dump
psql mydb < schema.sql
```

## Globals

```bash
pg_dumpall --globals-only > globals.sql
```

Use `-Fc` for parallel `pg_restore` on large databases.

## Sources

- PostgreSQL Documentation — [pg_dump](https://www.postgresql.org/docs/current/app-pgdump.html)
- PostgreSQL Documentation — [Backup and Restore](https://www.postgresql.org/docs/current/backup.html)
