### Import DB

- before execution create database
```bash
mysql -u <username> -p <db name> < <sql file>;
mysql -u root -p testDB < db.sql;
```

```sql
SHOW databases;
SHOW COLUMNS FROM <table>;
SHOW INDEX FROM <table>;
SHOW tables;
```

## table
```txt
CREATE TABLE table_name (
	column1 datatype constraints,
	column2 datatype constraints,
	...
)
```

```sql
CREATE TABLE users(
	id INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(100) NOT NULL,
	role VARCHAR(50) DEFAULT 'guest'
)
```

## Permission
```sql
GRANT ALL PRIVILEGES ON db_name.* TO 'user'@'host';
```

#### grant specific privileges
```sql
GRANT SELECT, INSERT, UPDATE, DELETE ON db_name.* TO 'user'@'host';

```

```sql
update <tablename> Set <columnname> = <value> <condition>;
update employee Set name = "ram" where emp_id = 1000;
```

### Transaction
```sql
START Transaction;

update user set name = "Alice" where id = 1000;

select * from users where id = 1000;
-- decide if OK
commit;

-- if not ok
rollback;
```

## Query table
```sql
SELECT id, name, role, shift
  CASE
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