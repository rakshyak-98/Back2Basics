[[database migration]] [[mysql table]] [[psql table]] [[Database design]] [[mysql data migrations]]

# Alter table

> SQL DDL for changing existing table structure—add/drop columns, constraints, and indexes—with lock and rewrite behavior that can stall production if ignored.

## Interview Relevance

Interviewers ask about `ALTER TABLE` to see whether you know online DDL vs table rebuild, expand/contract migrations, and how PostgreSQL and MySQL differ on big tables. Signal: you plan zero-downtime schema change, not “run ALTER in production and hope.”

## Sources

- [PostgreSQL Documentation — ALTER TABLE](https://www.postgresql.org/docs/current/sql-altertable.html) — deep-dive
- [MySQL Reference Manual — ALTER TABLE](https://dev.mysql.com/doc/refman/en/alter-table.html) — deep-dive
- [MySQL Reference Manual — Online DDL Operations](https://dev.mysql.com/doc/refman/en/innodb-online-ddl-operations.html) — deep-dive

## Key Concepts

- **DDL mutates structure:** add/drop columns, constraints, indexes on live tables → lock and rewrite cost depend on engine and operation.
- **In-place vs copy:** some changes are metadata-only; others rebuild the whole table → hours of lock/IO on large InnoDB tables with `ALGORITHM=COPY`.
- **Expand/contract:** additive, reversible steps beat one destructive rewrite → keep old and new shapes overlapping during deploys.

## Technical Details

```sql
ALTER TABLE orders ADD COLUMN shipped_at TIMESTAMPTZ;
ALTER TABLE orders ADD CONSTRAINT orders_total_nonneg CHECK (total_cents >= 0);
ALTER TABLE orders DROP COLUMN legacy_status;
```

| Engine | Risk on big tables |
|--------|-------------------|
| PostgreSQL | Many `ADD COLUMN` operations are fast; some require full rewrite |
| MySQL InnoDB | `ALGORITHM=COPY` rebuilds entire table — hours on large data |

Always check `EXPLAIN` / `ALGORITHM` / `LOCK` hints and test on a snapshot.

Zero-downtime sequence:

1. Add nullable column
2. Deploy code that writes new column
3. Backfill
4. Add `NOT NULL` + default if needed
5. Remove old column in later release

## Real-World Applications

Shipping a new `shipped_at` column without taking checkout offline. Example: add nullable column, dual-write from the app, batch backfill, then enforce `NOT NULL` after coverage hits 100%.

## Pros/Cons or Trade-offs

- **Pro:** Schema evolves with the product; constraints document invariants next to data.
- **Con:** Naive ALTER on large tables causes lock storms and replication lag; multi-step migrations add operational complexity.

## Comparison

vs [[database migration]]: `ALTER TABLE` is the SQL statement; migrations are versioned, ordered scripts that apply ALTER (and data backfills) across environments. vs [[mysql data migrations]]: online tools like gh-ost wrap ALTER-like rebuilds when native online DDL is insufficient.

## Mistakes to Avoid

- Running `ALGORITHM=COPY` ALTER on multi-GB tables during peak traffic.
- Adding `NOT NULL` before backfill completes — migration fails or locks forever.
- Dropping a column still referenced by old app versions still rolling out.
- Skipping staging rehearsal with production-sized data.
