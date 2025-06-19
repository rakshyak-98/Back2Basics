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
