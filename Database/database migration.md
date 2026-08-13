[[migration]] [[Alter table]] [[Database design]] [[mysql data migrations]] [[relocatable schema]]

# database migration

> Versioned, repeatable schema changes applied in order across environments—so production structure matches what the application code expects.

## Principles

1. **Forward-only scripts** in source control (with companion down migrations only in development if needed)
2. **Idempotent guards** where reruns are possible (`IF NOT EXISTS`)
3. **Expand/contract** for zero-downtime: add column → dual-write → backfill → switch reads → drop old

```txt
v001_create_users.sql ──► v002_add_email_index.sql ──► v003_partition_orders.sql
```

## Online DDL considerations

- [[Alter table]] on large MySQL tables may rebuild entire table — use `ALGORITHM=INPLACE, LOCK=NONE` when supported
- PostgreSQL `ADD COLUMN ... DEFAULT` is fast on recent versions (no full rewrite for constant default)

## Tooling examples

Flyway, Liquibase, Alembic, Rails `db/migrate`, golang-migrate — pick one per service and never mix manual hotfixes without recording them.

## Sources

- PostgreSQL Documentation — [DDL](https://www.postgresql.org/docs/current/ddl.html)
- MySQL Reference Manual — [Online DDL](https://dev.mysql.com/doc/refman/en/innodb-online-ddl-operations.html)
- Kleppmann, *DDIA*, Ch. 4 (schema evolution)
