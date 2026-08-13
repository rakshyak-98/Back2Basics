[[database migration]] [[migration]] [[mysql dump]] [[Alter table]]

# mysql data migrations

> Moving or transforming data within or between MySQL instances—batch updates, `pt-online-schema-change`, and cutover plans that avoid long table locks.

## Online schema change tools

- **gh-ost** — GitHub online schema migration
- **pt-online-schema-change** — Percona Toolkit

Use when native `ALGORITHM=INPLACE` cannot avoid copy.

## Batch backfill

```sql
UPDATE users SET migrated = 1 WHERE id BETWEEN 10000 AND 19999 AND migrated = 0;
-- repeat with sleep between batches
```

## Cross-instance

`mysqldump` + restore, or replication chain with promoted replica—plan for replication lag and application dual-write.

## Sources

- MySQL Reference Manual — [Online DDL](https://dev.mysql.com/doc/refman/en/innodb-online-ddl-operations.html)
- Percona — [pt-online-schema-change](https://docs.percona.com/percona-toolkit/pt-online-schema-change.html)
