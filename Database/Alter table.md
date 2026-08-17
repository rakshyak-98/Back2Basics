[[database migration]] [[mysql table]] [[psql table]] [[Database design]] [[mysql data migrations]]

# Alter table

> SQL DDL for changing existing table structure—add/drop columns, constraints, and indexes—with lock and rewrite behavior that can stall production if ignored.

```txt
        Alter table ──┬── Interview
               ├── Sources
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers ask about `ALTER TABLE` to see whether you know online DDL vs ta…

## Sources
- [PostgreSQL Documentation — ALTER TABLE](https://www.postgresql.org/docs/current/sql-altertable.html) — deep-dive
- [MySQL Reference Manual — ALTER TABLE](https://dev.mysql.com/doc/refman/en/alter-table.html) — deep-dive
- [MySQL Reference Manual — Online DDL Operations](https://dev.mysql.com/doc/refman/en/innodb-online-ddl-operations.html) — deep-dive

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

- Always check `EXPLAIN` / `ALGORITHM` / `LOCK` hints and test on a snapshot.

- Zero-downtime sequence:

1. Add nullable column
2. Deploy code that writes new column
3. Backfill
4. Add `NOT NULL` + default if needed
5. Remove old column in later release

## Mistakes to Avoid
- **Mistake:** Running `ALGORITHM=COPY` ALTER on multi-GB tables during peak tr…
- **Mistake:** Adding `NOT NULL` before backfill completes
- **Mistake:** Dropping a column still referenced by old app versions still rol…
- **Mistake:** Skipping staging rehearsal with production-sized data

## Pros/Cons or Trade-offs
- **Pro:** Schema evolves with the product; constraints document invariants next to data.
- **Con:** Naive ALTER on large tables causes lock storms and replication lag; multi-step migrations add operational complexity.

## Comparison
- vs [[database migration]]: `ALTER TABLE` is the SQL statement


### Use cases
- Shipping a new `shipped_at` column without taking checkout offline
