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
fsdjmc

s`