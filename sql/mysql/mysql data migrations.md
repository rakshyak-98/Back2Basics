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
