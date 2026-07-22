[[mysql]] [[database migration]] [[mysql/mysql user]] [[Alter table]]

# mysqldump

> One-line: logical backup/export of schema and/or data — primary disaster-recovery baseline; know flags for schema-only, routines, triggers, and restore pitfalls.

## Mental model

`mysqldump` reads tables (consistent snapshot with `--single-transaction` on InnoDB) and emits SQL or delimited text. **Logical** backup — restore = replay SQL. Not a replacement for **binlog PITR** for minute-level RPO; combine full dump + binlogs for production.

```
mysqldump ──► .sql file ──► mysql < file   (restore)
           └── optional gzip → S3
```

Large DBs: parallel tools (mydumper), physical backup (Percona XtraBackup), or replica-based dump off primary.

## Standard config / commands

### Full database (schema + data)

```bash
mysqldump -u root -p \
  --single-transaction \
  --routines --events --triggers \
  --hex-blob \
  mydb | gzip > mydb_$(date +%F).sql.gz
```

### Schema only (DDL for migrations/bootstrap)

```bash
mysqldump -u root -p \
  --no-data \
  --routines --events --triggers \
  --skip-add-drop-table \
  --set-charset \
  mydb > schema.sql
```

### Single table DDL

```bash
mysqldump -u root -p --no-data mydb table_name > table.sql
```

### Data only one table

```bash
mysqldump -u root -p --no-create-info mydb table_name > table_data.sql
```

### Users and grants

```bash
mysqldump -u root -p --no-data mysql user db tables_priv > mysql_grants.sql
# or:
mysql -u root -p -N -e "SHOW GRANTS FOR 'app'@'%'" > app_grants.sql
```

### Restore

```bash
gunzip -c mydb.sql.gz | mysql -u root -p mydb
mysql -u root -p mydb < schema.sql
```

### Docker

```bash
docker exec mysql_container mysqldump -u root -psecret --all-databases > all.sql
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Dump locks writes | Missing `--single-transaction` on InnoDB | Add flag; use `--lock-tables=false` with care |
| Restore fails on TRIGGER | Definer user missing | Create users first; `--force` only in dev |
| Huge dump slow | Full table scan | mydumper parallel; exclude log tables |
| Partial restore | FK order | `--disable-keys`; disable FK checks session during import |
| Charset corruption | Mixed utf8/utf8mb4 | `--default-character-set=utf8mb4` |
| Empty routines in dump | Flag omitted | Add `--routines --events --triggers` |

## Gotchas

> [!WARNING]
> **Dump during peak without `--single-transaction`** — global read lock on MyISAM mix; InnoDB still prefers consistent snapshot.

> [!WARNING]
> **Secrets in dump** — user tables may include PII; encrypt at rest (S3 SSE).

> [!WARNING]
> **Restore ≠ migration** — test on scratch instance; version match major MySQL.

> [!WARNING]
> **`--skip-add-drop-table`** — safe for incremental schema apply; full restore usually wants DROP.

## When NOT to use

- **Multi-TB database hot backup** — physical/XtraBackup or replica snapshot.
- **Continuous RPO minutes** — binlog streaming + periodic full backup.

## Related

[[mysql]] [[database migration]] [[MySQL Triggers]] [[mysql/mysql user]] [[Database mistakes]]
