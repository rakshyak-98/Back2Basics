```sql
\c database_name -- connect to database;
\l -- list all databases
\conninfo -- show current connection info
```

### Tables

```sql
\dt -- list all tables;
\d table_name -- Describe table structure
\d+ table_name -- Detailed table info (with storage)
```

```sql
CREATE TABLE table_name (); -- create table;
DROP TABLE table_name; -- delete table;
ALTER TABLE table_name ADD COLUMN col_name TYPE;
ALTER TABLE table_name DROP COLUMN col_name;
TRUNCATE table_name; -- delete all rows (faster than delete)

```

```sql
SELECT * FROM table_name; 
SELECT col1, col2 FROM table_name WHERE condition;
INSERT INTO table_name (col1, col2) VALUES (val1, val2);
UPDATE table_name SET col1=val1 WHERE id = 1;

```


### Create user

```sql
CREATE USER wateradmin WITH PASSWORD 'secure_password';

-- Connect permission
GRANT CONNECT ON DATABASE your_database TO wateradmin;

-- Usage on public schema
GRANT USAGE ON SCHEMA public TO wateradmin;

-- Create tables in schema
GRANT CREATE ON SCHEMA public TO wateradmin;

-- Use all objects in schema
GRANT USAGE ON SCHEMA public TO wateradmin;
```

```sql
ALTER USER <user> WITH PASSWORD <new password>;
ALTER USER wateradmin WITH PASSWORD 'new_password' VALID UNTIL '2025-12-31';
ALTER USER wateradmin WITH VALID UNTIL 'infinity';
```

### Drop user

```sql
-- Kill active connections
SELECT pg_terminate_backend(pid) 
FROM pg_stat_activity 
WHERE usename = 'wateradmin' AND pid <> pg_backend_pid();

-- Reassign owned objects
REASSIGN OWNED BY wateradmin TO postgres;

-- Drop owned objects
DROP OWNED BY wateradmin;

-- Delete user
DROP USER IF EXISTS wateradmin;

```