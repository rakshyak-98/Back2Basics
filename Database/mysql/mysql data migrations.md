[[mysql]]

# mysql data migrations

> One-line: what / why for **mysql data migrations** — source TBD.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#How to do a table migration between database]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

…

## Standard config / commands

…

## How to do a table migration between database

#### If different server
```bash
mysqldump -u user -p source_db table_name > table_dump.sql

```

```bash
mysql -u user -p target_db < table_dump.sql

```
#### If server is same

> [!NOTE]
> Both column should of same data type
> Foreign reference column should have unique constraint (or primary key).
```mysql
CREATE TABLE target_db.table_name AS SELECT * FROM source_db.table_name;

-- copy structure only
CREATE TABLE target_db.table_name LIKE source_db.table_name;

### Update table after query with join
```mysql
UPDATE hkAppNotification AS hk
LEFT JOIN jobDepartment AS jd
  ON jd.jobDepartmentName = hk.department
SET hk.department = jd.id;
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| … | … | … |

## Gotchas

> [!WARNING]
> …


### Gotchas


> [!WARNING]
> …


### Gotchas


> [!WARNING]
> …


### Gotchas


> [!WARNING]
> …


### Gotchas


> [!WARNING]
> …


### Gotchas


> [!WARNING]
> …

## When NOT to use

…


### When NOT to use


…


### When NOT to use


…


### When NOT to use


…


### When NOT to use


…


### When NOT to use


…

## Related

[[…]]


### Related


[[…]]


### Related


[[…]]


### Related


[[…]]


### Related


[[…]]


### Related


[[…]]
