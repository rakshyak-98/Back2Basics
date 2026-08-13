[[mysql]] [[database migration]] [[mysql data migrations]] [[psql database dump]]

# mysql dump

> Logical backup with `mysqldump`—SQL or delimited output of schema and data for restore, cloning, and disaster recovery drills.

## Common invocations

```bash
# Full database
mysqldump -h host -u backup --single-transaction --routines --triggers mydb > mydb.sql

# Schema only
mysqldump --no-data mydb > schema.sql

# One table
mysqldump mydb orders > orders.sql
```

## InnoDB consistent snapshot

`--single-transaction` uses a consistent read—no global read lock on InnoDB tables.

## Restore

```bash
mysql mydb < mydb.sql
```

Test restores regularly—an untested backup is wishful thinking.

## Sources

- MySQL Reference Manual — [mysqldump](https://dev.mysql.com/doc/refman/en/mysqldump.html)
- MySQL Reference Manual — [Backup and Recovery](https://dev.mysql.com/doc/refman/en/backup-and-recovery.html)
