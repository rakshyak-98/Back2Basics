[[SQL/postgres]] [[mysql dump]] [[database migration]] [[psql essential]]

# psql database dump

> Logical backups with `pg_dump` / `pg_dumpall` — schema, data, and globals for restore, cloning, and version upgrades.

```txt
        psql database dump ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Ops staple: custom format (`-Fc`) for parallel restore, globals dump for role…

## Sources
- [pg_dump](https://www.postgresql.org/docs/current/app-pgdump.html) — deep-dive
- [Backup and Restore](https://www.postgresql.org/docs/current/backup.html) — overview

## Key Concepts
- **pg_dump:** One database (schema/data).
- **pg_dumpall:** Cluster globals (roles, tablespaces) or all DBs.
- **Custom format `-Fc`:** Enables `pg_restore` parallelism and selective restore.
- **Schema-only:** Migration review and empty environment bootstrap.

## Technical Details
```bash
pg_dump -h host -U backup -Fc mydb > mydb.dump
pg_dump -h host -U backup --schema-only mydb > schema.sql
pg_restore -d mydb mydb.dump
psql mydb < schema.sql
pg_dumpall --globals-only > globals.sql
```

## Mistakes to Avoid
- **Mistake:** Dumping data but forgetting globals (roles missing on restore)
- **Mistake:** Never testing `pg_restore` into a scratch instance
- **Mistake:** Using plain SQL dumps for multi-hundred-GB databases without a t…

## Pros/Cons or Trade-offs
- **Pro:** Portable, inspectable, selective restore.
- **Con:** Slow on huge clusters versus physical backups; not a complete PITR story alone.
- **Trade-off:** Plain SQL vs custom format — readability versus restore features.

## Comparison
- vs [[mysql dump]]: same logical-backup niche


### Use cases
- Nightly logical backups, cloning QA databases, capturing roles before major u…
