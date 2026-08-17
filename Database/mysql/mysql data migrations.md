[[database migration]] [[migration]] [[mysql dump]] [[Alter table]]

# mysql data migrations

> Moving or transforming data within or between MySQL instances—batch updates, `pt-online-schema-change`, and cutover plans that avoid long table locks.

```txt
        mysql data migrati ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** MySQL-specific migration interviews focus on online schema change tools (gh-o…

## Sources
- [MySQL Reference Manual — Online DDL](https://dev.mysql.com/doc/refman/en/innodb-online-ddl-operations.html) — deep-dive
- [Percona — pt-online-schema-change](https://docs.percona.com/percona-toolkit/pt-online-schema-change.html) — deep-dive

## Key Concepts
- **Online schema change tools:** gh-ost, pt-online-schema-change when `ALGORITHM=INPLACE` is not enough.
- **Batch backfill:** chunked UPDATEs with sleep to limit lag and locks.
- **Cross-instance:** dump/restore or replication promote — plan for lag and dual-write.

## Technical Details
- Online schema change tools:

- **gh-ost:** — GitHub online schema migration
- **pt-online-schema-change:** — Percona Toolkit

- Use when native `ALGORITHM=INPLACE` cannot avoid copy.

```sql
UPDATE users SET migrated = 1 WHERE id BETWEEN 10000 AND 19999 AND migrated = 0;
-- repeat with sleep between batches
```

- Cross-instance: `mysqldump` + restore ([[mysql dump]]), or replication chain …

## Mistakes to Avoid
- **Mistake:** Running unbounded UPDATEs on huge tables during peak traffic
- **Mistake:** Using only dump/restore for live cutover while writes continue
- **Mistake:** Skipping replication lag monitoring during online schema change

## Pros/Cons or Trade-offs
- **Pro:** Large changes without multi-hour outages; controlled lag via batching.
- **Con:** Tools add operational complexity; dual-write windows need careful app coordination.

## Comparison
- vs [[database migration]]: versioned schema files orchestrate change


### Use cases
- Adding a non-nullable column to a multi-hundred-GB orders table during busine…
