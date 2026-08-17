[[mysql]] [[database migration]] [[mysql data migrations]] [[psql database dump]]

# mysql dump

> Logical backup with `mysqldump`—SQL or delimited output of schema and data for restore, cloning, and disaster recovery drills.

```txt
        mysql dump ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Backup reviews expect `--single-transaction` for InnoDB consistent snapsho…

## Sources
- [MySQL Reference Manual — mysqldump](https://dev.mysql.com/doc/refman/en/mysqldump.html) — deep-dive
- [MySQL Reference Manual — Backup and Recovery](https://dev.mysql.com/doc/refman/en/backup-and-recovery.html) — overview

## Key Concepts
- **Logical backup:** SQL statements (or delimited data) that recreate schema/data.
- **Consistent InnoDB snapshot:** `--single-transaction` avoids global read lock for InnoDB.
- **Scoped dumps:** full DB, schema-only, or single table.
- **Restore is part of backup:** untested dumps are wishful thinking.

## Technical Details
```bash
# Full database
mysqldump -h host -u backup --single-transaction --routines --triggers mydb > mydb.sql

# Schema only
mysqldump --no-data mydb > schema.sql

# One table
mysqldump mydb orders > orders.sql
```

- InnoDB consistent snapshot: `--single-transaction` uses a consistent read—no …

```bash
mysql mydb < mydb.sql
```

- Test restores regularly—an untested backup is wishful thinking.

## Mistakes to Avoid
- **Mistake:** Dumping without `--single-transaction` on busy InnoDB (unnecessa…
- **Mistake:** Never practicing restore until ransomware/outage day
- **Mistake:** Treating dump alone as PITR

## Pros/Cons or Trade-offs
- **Pro:** Portable, human-inspectable, easy partial restores; great for small/medium databases.
- **Con:** Slow and large for multi-TB data; long dumps can still affect performance; physical/snapshot backups scale better at huge sizes.

## Comparison
- vs [[psql database dump]]: same logical-backup idea for PostgreSQL (`pg_dump`…


### Use cases
- Cloning staging from production (scrubbed), schema capture for review, and DR…
