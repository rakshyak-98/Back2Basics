[[migration]] [[Alter table]] [[Database design]] [[mysql data migrations]] [[relocatable schema]]

# database migration

> Versioned, repeatable schema changes applied in order across environments—so production structure matches what the application code expects.

```txt
        database migration ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Migrations probe zero-downtime thinking: expand/contract, online DDL, and nev…

## Sources
- [PostgreSQL Documentation — DDL](https://www.postgresql.org/docs/current/ddl.html) — overview
- [MySQL Reference Manual — Online DDL](https://dev.mysql.com/doc/refman/en/innodb-online-ddl-operations.html) — deep-dive
- Kleppmann, *Designing Data-Intensive Applications*, Ch. 4 — overview

## Key Concepts
- **Forward-only scripts:** in source control (down migrations only in development if needed).
- **Idempotent guards:** where reruns are possible (`IF NOT EXISTS`).
- **Expand/contract:** for zero-downtime: add column → dual-write → backfill → switch reads → drop o…
- **One tool per service:** Flyway, Liquibase, Alembic, Rails `db/migrate`, golang-migrate

## Technical Details
```txt
v001_create_users.sql ──► v002_add_email_index.sql ──► v003_partition_orders.sql
```

- Online DDL considerations:

- [[Alter table]] on large MySQL tables may rebuild entire table
- PostgreSQL `ADD COLUMN ..

- Tooling examples: Flyway, Liquibase, Alembic, Rails `db/migrate`, golang-migr…

## Mistakes to Avoid
- **Mistake:** Manual production DDL that never lands in the migration history
- **Mistake:** Mixing multiple migration tools in one service
- **Mistake:** Combining destructive DROP with additive changes in one risky de…
- **Mistake:** Skipping expand/contract on hot tables

## Pros/Cons or Trade-offs
- **Pro:** Environments stay aligned; rollouts are reviewable and repeatable.
- **Con:** Poorly written migrations lock tables; long-running data backfills need separate batch jobs ([[mysql data migrations]]).

## Comparison
- vs [[migration]]: “migration” is the broad term (schema + data)


### Use cases
- Shipping `email_verified_at` across staging and production with the same vers…
