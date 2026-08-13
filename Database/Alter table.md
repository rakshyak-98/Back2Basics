[[database migration]] [[mysql table]] [[psql table]] [[Database design]]

# Alter table

> SQL DDL for changing existing table structure—add/drop columns, constraints, and indexes—with lock and rewrite behavior that can stall production if ignored.

## Common operations

```sql
ALTER TABLE orders ADD COLUMN shipped_at TIMESTAMPTZ;
ALTER TABLE orders ADD CONSTRAINT orders_total_nonneg CHECK (total_cents >= 0);
ALTER TABLE orders DROP COLUMN legacy_status;
```

## Locking reality

| Engine | Risk on big tables |
|--------|-------------------|
| PostgreSQL | Many `ADD COLUMN` operations are fast; some require full rewrite |
| MySQL InnoDB | `ALGORITHM=COPY` rebuilds entire table — hours on large data |

Always check `EXPLAIN` / `ALGORITHM` / `LOCK` hints and test on a snapshot.

## Zero-downtime sequence

1. Add nullable column
2. Deploy code that writes new column
3. Backfill
4. Add `NOT NULL` + default if needed
5. Remove old column in later release

## Sources

- PostgreSQL Documentation — [ALTER TABLE](https://www.postgresql.org/docs/current/sql-altertable.html)
- MySQL Reference Manual — [ALTER TABLE](https://dev.mysql.com/doc/refman/en/alter-table.html)
