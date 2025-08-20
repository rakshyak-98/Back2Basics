
```mysql
pager less -S; # -S no wrap, set a pager for output result;
nopager; # to reset the pager to stdout (default);

tee <file to log to>; # everyting you will type is directed to the file;
```

```bash
mysql --auto-rehash -u user -p db_name; # enable auto complete
```
### Import DB

- before execution create database
```bash
mymysql -u <username> -p <db name> < <sql file>;
mymysql -u root -p testDB < db.sql;
```

```bash
mysqldump --user=user --passwrod=pass --host=localhost \ --skip-comments --no-create-info --tab=/tmp --fields-terminated-by=',' dbname tablename;
```
> [!INFO]
> then convert the CSV output to JSON using a tool like

- Then convert the CSV output to JSON using this tool
```bash
cat /tmp/tablename.txt | jq -R -s -c 'split("\n")' | map(split(","))'
```
 ```mysql
SHOW databases;
SHOW COLUMNS FROM <table>;
SHOW INDEX FROM <table>;
SHOW tables;
```

```mysql
SELECT VERSION();
SELECT DATABASE();
```

```mysql
SELECT JSON_OBJECT('id', id, 'name', name) FROM your_table;
SELECT * FROM table_name/G; -- Each column shown on its own line
```
> [!INFO]
> User `pager` to Customise output (like CSV, JSON, no-wrap)

```txt
EXPLAIN SELECT * FROM table_name where condition; 
```

```mysql
DROP VIEW <viewname>;
```

```mysql
SELECT DATABASE(); # view current database.
```

## Range
```mysql
SELECT * FROM reservations
ORDER BY check_in
LIMIT 10 OFFSET 20;
```

## Dates
```mysql
SELECT DATE_SUB(CURDATE(), interval 1 day);
```
### Cascade
```mysql
```
### Transaction
```mysql
START Transaction;

update user set name = "Alice" where id = 1000;

select * from users where id = 1000;
-- decide if OK
commit;

-- if not ok
rollback;
```

```mysql
SELECT id, name, role, shift CASE
    WHEN role = 'admin' AND shift = 'Morning' THEN email
    WHEN role = 'manager' AND department = 'IT' THEN department
    ELSE NULL
  END AS conditional_info,
  
  CASE
    WHEN role = 'guest' OR shift = 'Night' THEN 'Restricted'
    ELSE 'Allowed'
  END AS access_status
FROM users;

```


```mysql
SHOW INDEX FROM jobDepartment WHERE Column_name = 'id';
```

```mysql
ALTER TABLE jobDepartment ADD PRIMARY KEY (id);

-- or if primary key exists on another column and you want unique only:
ALTER TABLE jobDepartment ADD UNIQUE INDEX uq_id (id);
```


### How to update to column in single query
```txt
	UPDATE <table name> 
SET 
	<column> = <value>,
	<column2> = <value2>,
	<column3> = <vlaue3>,
<condition>
```

## List matching
```mysql
SELECT col1
	FROM table
WHERE column_name IN ('val1', 'val2', 'val3');
```

## View
```mysql
SHOW FULL TABLES
WHERE Table_type = "VIEW";
```

```mymysql
SHOW CREATE VIEW view_name;
```

```mysql
CREATE VIEW active_housekeepings_jobgs AS
SELECT id, jobDepartment, createdTime
FROM <tablename>; 
where <condition>;
```


```mysql
FOREIGN KEY (...) REFERENCES ... ON DELETE CASCADE ON UPDATE CASCADE
```
- `CASCADE` -> auto delete/update child rows
- `SET NULL` -> sets child to `NULL` on parent delete
- `RESTRICT/NO ACTIOn` -> blocks delete/update

### `ERROR 1553 (HY000): Cannot drop index 'customerNumber': needed in a foreign key constraint`
- you're trying to drop an index that is automatically created to enforce a foreign key constraint.
- drop the foreign key first, then the index
```mysql
SELECT CONSTRAINT_NAME
FROM information_schema.KEY_COLUMN_USAGE
WHERE TABLE_NAME = 'your_table' AND COLUMN_NAME = 'your_table_column_name'

```

```mysql
SHOW CREATE TABLE your_table;
```

#### Drop the foreign key constraint
```mysql
ALTER TABLE your_table DROP FOREIGN KEY fk_name;

```

### Manipulation
```mysql
SELECT JSON_OBJECT(
  'col1', col1,
  'col2', col2
) AS json_data
FROM users;
```

### View size of a table
```mysql
SELECT 
  table_schema AS database_name,
  table_name,
  ROUND((data_length + index_length) / 1024 / 1024, 2) AS size_mb
FROM 
  information_schema.tables
WHERE 
  table_schema = 'your_database' AND table_name = 'your_table';
```
