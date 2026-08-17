[[migration]] [[Alter table]] [[Database design]] [[mysql data migrations]] [[relocatable schema]]

# database migration

> Versioned, repeatable schema changes applied in order across environments—so production structure matches what the application code expects.





## Interview Relevance
Migrations probe zero-downtime thinking: expand/contract, online DDL, and never-mix-manual-hotfixes. Interviewers want ordered scripts in source control and a story for large-table ALTER without long locks.

## Sources
- [PostgreSQL Documentation — DDL](https://www.postgresql.org/docs/current/ddl.html) — overview
- [MySQL Reference Manual — Online DDL](https://dev.mysql.com/doc/refman/en/innodb-online-ddl-operations.html) — deep-dive
- Kleppmann, *Designing Data-Intensive Applications*, Ch. 4 — overview

## Key Concepts
- **Forward-only scripts** in source control (down migrations only in development if needed).
- **Idempotent guards** where reruns are possible (`IF NOT EXISTS`).
- **Expand/contract** for zero-downtime: add column → dual-write → backfill → switch reads → drop old.
- **One tool per service:** Flyway, Liquibase, Alembic, Rails `db/migrate`, golang-migrate — record every production change.

## Technical Details
```txt
v001_create_users.sql ──► v002_add_email_index.sql ──► v003_partition_orders.sql
```

Online DDL considerations:

- [[Alter table]] on large MySQL tables may rebuild entire table — use `ALGORITHM=INPLACE, LOCK=NONE` when supported
- PostgreSQL `ADD COLUMN ... DEFAULT` is fast on recent versions (no full rewrite for constant default)

Tooling examples: Flyway, Liquibase, Alembic, Rails `db/migrate`, golang-migrate — pick one per service and never mix manual hotfixes without recording them.

## Real-World Applications
Shipping `email_verified_at` across staging and production with the same versioned files. Example: expand with nullable column, deploy dual-write, backfill, then contract by dropping the legacy flag column next release.

## Pros/Cons or Trade-offs
- **Pro:** Environments stay aligned; rollouts are reviewable and repeatable.
- **Con:** Poorly written migrations lock tables; long-running data backfills need separate batch jobs ([[mysql data migrations]]).

## Comparison
vs [[migration]]: “migration” is the broad term (schema + data); **database migration** here means versioned schema DDL. vs [[Alter table]]: ALTER is the statement; migrations package ALTER (and related steps) into ordered files.

## Mistakes to Avoid
- Manual production DDL that never lands in the migration history — environment drift.
- Mixing multiple migration tools in one service.
- Combining destructive DROP with additive changes in one risky deploy.
- Skipping expand/contract on hot tables.
