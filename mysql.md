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
pager less -S; # -S no wrap, set a pager for output result;
nopager; # to reset the pager to stdout (default);

less <file to log to>; # everyting you will type is directed to the file;
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
## Permission
```mysql
GRANT ALL PRIVILEGES ON db_name.* TO 'user'@'host';
```

#### Grant specific privileges
```mysql
GRANT SELECT, INSERT, UPDATE, DELETE ON db_name.* TO 'user'@'host';

```

## Table
```txt
CREATE TABLE table_name (
	column1 datatype constraints,
	column2 datatype constraints,
	...
)
```

```mysql
CREATE TABLE users(
	id INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(100) NOT NULL,
	role VARCHAR(50) DEFAULT 'guest'
)
```

### Cascade
```mysql
```

```mysql
update <tablename> Set <columnname> = <value> <condition>;
update employee Set name = "ram" where emp_id = 1000;
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

## Constraint
```mysql
ALTER TABLE hkAppNotification
ADD CONSTRAINT unique_floor_shift_department
UNIQUE (floorNumber, shiftName, department);
```
> [!NOTE]
> If **any of the 3 columns can be NULL**, then uniqueness is not guaranteed across rows with NULLs (as per SQL standard: `NULL != NULL`).

## How to do a table migration between database

#### If different server
```bash
mysqldump -u user -p source_db table_name > table_dump.sql

```

```bash
mysql -u user -p target_db < table_dump.sql

```


#### if server is same
```mysql
CREATE TABLE target_db.table_name AS SELECT * FROM source_db.table_name; 

-- copy structure only
CREATE TABLE target_db.table_name LIKE source_db.table_name;
 
-- Copy structure + insert data
INSERT INTO target_db.table_name SELECT * FROM source_db.table_name;

```
> [!WARNING]
> Loses indexes, constraints - recreate manually if needed.

### Update table after query with join
```mysql
UPDATE hkAppNotification AS hk
LEFT JOIN jobDepartment AS jd
  ON jd.jobDepartmentName = hk.department
SET hk.department = jd.id;

```
> [!NOTE]
> Both column should of same data type
> Foreign reference column should have unique constraint (or primary key).

```mysql
SHOW INDEX FROM jobDepartment WHERE Column_name = 'id';
```

```mysql
ALTER TABLE jobDepartment ADD PRIMARY KEY (id);

-- or if primary key exists on another column and you want unique only:
ALTER TABLE jobDepartment ADD UNIQUE INDEX uq_id (id);
```

## Index
## Get all tables constraints keys
```mysql
SELECT CONSTRAINT_NAME
FROM information_schema.KEY_COLUMN_USAGE
-- filter 
WHERE TABLE_NAME = 'orders' AND COLUMN_NAME = 'customer_id' AND CONSTRAINT_NAME != 'PRIMARY';
```
### change index of table
```mysql
ALTER TABLE your_table DROP INDEX index_name;
ALTER TABLE your_table ADD INDEX index_name (column_name) USING HASH;
```

> [!NOTE] InnoDB only supports `BTREE` so `HASH` is ignored silently unless he engine is `MEMORY`
```mysql
CREATE TABLE mem_table (
  id INT,
  name VARCHAR(100),
  INDEX name_idx (name) USING HASH
) ENGINE=MEMORY;

```
- `HASH` is only supported by `MEMORY` engine.

```mysql
SHOW INDEX FROM your_table;
```
- check current index type

## Update value on update
```mysql
CREATE TABLE my_table (
	id INT PRIMARY KEY,
	updated_at TIMESTAMP DEFUALT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;
)
```

- remove the constraint from existing table 
```mysql
ALTER TABLE your_table
MODIFY COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
```
- `DEFAULT_GENERATED` -> is a metadata flag shown in `INFORMATION_SCHEMA.COLUMNS` to indicate that a column's default value was automatically generated by the system.

```mysql
SELECT COLUMN_NAME, COLUMN_DEFAULT, EXTRA, GENERATION_EXPRESSION, IS_GENERATED, COLUMN_DEFAULT_GENERATED
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'users';
```

## Add columns to an existing table
```mysql
ALTER TABLE users
ADD (
	age INT
	is_active BOOLEAN DEFAULT TRUE,
	last_login TIMESTAMP
)
```

```mysql
ALTER TABLE table_name RENAME COLUMN old_name TO new_name;
ALTER TABLE table_name CHANGE COLUMN old_name TO new_name data_type;

```

### re-arrange columns
```mysql
ALTER TABLE table_name MODIFY column_name data_type AFTER other_column;
ALTER TABLE table_name MODIFY column_name data_tyep FIRST;
```

### Data insert in table from other table
```mysql
INSERT INTO hkAppNotification (jobType, floorNumber, department, shiftName, level1Mobile, level2Mobile, level3Mobile, hodMobile)
SELECT jobType, floorNumber, department, shiftName, level1Mobile, level2Mobile, level3Mobile, hodMobile
FROM hkAppNotification
WHERE department = 15;
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

### How to define constraints
```mysql
CREATE TABLE orders (
	order_id INT PRIMARY KEY,
	custoemr_id INT
	FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
)

```

## Set foreign key constraints
```mysql
ALTER TABLE table_naem ADD CONSTRAINT FOREIGN KEY 
```

### Altering an existing table
```mysql
ALTER TABLE orders
ADD CONSTRAINT fk_customer
FOREIGN KEY (customer_id) REFERENCES customers(customer_id)

```

```mysql
ALTER TABLE table_name DROP COLUMN column_name;

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

## Partition table