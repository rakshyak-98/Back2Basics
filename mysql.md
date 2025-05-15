```bash
mysql --auto-rehash -u user -p db_name; # enable auto complete
```
### Import DB

- before execution create database
```bash
mymysql -u <username> -p <db name> < <sql file>;
mymysql -u root -p testDB < db.sql;
```

```mysql
SHOW databases;
SHOW COLUMNS FROM <table>;
SHOW INDEX FROM <table>;
SHOW tables;
```

```mysql
DROP VIEW <viewname>;
```

## table
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

## Permission
```mysql
GRANT ALL PRIVILEGES ON db_name.* TO 'user'@'host';
```

#### grant specific privileges
```mysql
GRANT SELECT, INSERT, UPDATE, DELETE ON db_name.* TO 'user'@'host';

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

## Query table
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

``

## Index
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

- check current index type
```mysql
SHOW INDEX FROM your_table;
```

### how to define constraints
```mysql
CREATE TABLE orders (
	order_id INT PRIMARY KEY,
	custoemr_id INT
	FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
)

```

#### Altering an existing table
```mysql
ALTER TABLE orders
ADD CONSTRAINT fk_customer
FOREIGN KEY (customer_id) REFERENCES customers(customer_id)

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
