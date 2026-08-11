[[mysql]] [[migration]] [[mysql dump]]

# mysql data migrations

> Move table data between databases or reshape columns — dump/restore across hosts, or `CREATE … AS SELECT` / UPDATE…JOIN on the same server.

---

## Mental model

**Say it in one breath:** Cross-host → `mysqldump` then load; same host → `CREATE TABLE … LIKE` / `AS SELECT` or INSERT…SELECT; backfills often use UPDATE with JOIN once types and keys match.

```txt
Different servers:  mysqldump → file → mysql < file
Same server:        CREATE … AS SELECT / INSERT…SELECT
Backfill:           UPDATE a JOIN b SET a.col = b.id
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Logical copy** | SQL dump of rows | “Not a raw `.ibd` file copy.” |
| **LIKE vs AS SELECT** | Structure vs structure+data | “AS SELECT drops indexes/constraints.” |
| **Backfill** | Fill new column from old | “Batch UPDATE to avoid long locks.” |
| **Expand/contract** | Safe DDL pattern | “Add nullable → backfill → enforce.” |

---

## Standard config / commands

```bash
# Different server
mysqldump -u user -p source_db table_name > table_dump.sql
mysql -u user -p target_db < table_dump.sql
```

```sql
-- Same server
CREATE TABLE target_db.t AS SELECT * FROM source_db.t;      -- data, weak indexes
CREATE TABLE target_db.t LIKE source_db.t;                   -- structure only
INSERT INTO target_db.t SELECT * FROM source_db.t;

UPDATE hkAppNotification AS hk
LEFT JOIN jobDepartment AS jd ON jd.jobDepartmentName = hk.department
SET hk.department = jd.id;
```

| Knob | Why it matters |
|------|----------------|
| Matching types | JOIN/FK backfills fail on type mismatch |
| Unique parent key | FK/join targets need uniqueness |
| Batches | Large UPDATE locks; chunk by PK |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Truncated / wrong charset | Dump flags / table charset | `--default-character-set=utf8mb4` |
| Missing indexes after copy | Used AS SELECT only | `LIKE` + INSERT, or re-add indexes |
| FK fails mid-load | Order / orphan rows | Disable FK checks carefully or load parents first |
| Long lock on UPDATE JOIN | Huge table | Batched updates by id range |

---

## Gotchas

> [!WARNING]
> **`CREATE … AS SELECT` is not a full clone** — no indexes, FKs, or triggers.

> [!WARNING]
> **`SET foreign_key_checks=0`** — only in controlled migrations; verify integrity after.

---

## When NOT to use

- **Schema versioning for the application** — use a migration tool ([[migration]]), not one-off dumps as process.
- **Zero-downtime large DDL** — use online schema change tools / expand-contract.

---

## Related

[[migration]] [[mysql dump]] [[mysql table]] [[database migration]]
