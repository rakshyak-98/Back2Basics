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


# Index usage

```mysql
SELECT
  OBJECT_SCHEMA,
  OBJECT_NAME,
  INDEX_NAME,
  COUNT_STAR
FROM performance_schema.table_io_waits_summary_by_index_usage
WHERE INDEX_NAME IS NOT NULL
ORDER BY COUNT_STAR DESC;
```
- unused indexes (drop them - index maintenance isn't free)
- hot indexes to optimize further 

## Why indexes matter

> [!NOTE]
> MySQL (InnoDB default engine) stores data in two main structures

**Clustered Index**
- the actual table data (PRIMARY KEY or first unique key)
- Rows are physically ordered by the key
- Looking up by PK is very fast

**Secondary Indexes**
- Separate B+ tree structures that point back to the clustered index
- Every secondary index stores the indexed columns + PK value
- Covering index = when all needed columns are in the secondary index -> no extra lookup to clustered table (fastest)

- Forgetting composite indexes for multi-column WHERE/JOIN/ORDER BY
	- Bad `WHERE city = "Bengaluru" AND status = "active" ORDER BY created_at DESC`
	-> only index on `city` ? MySQL scans all Bengaluru rows + sorts
	- Good `CREATE INDEX idx_city_status_created ON hotels(city, status, created_at)`

> [!INFO]
> Index columns in left-to-right order as they appear in WHERE/JOIN/ORDER/GROUP.

- **Using functions on indexed columns → index ignored**
	- Bad: `WHERE YEAR(created_at) = 2025 or WHERE LOWER(email) = 'rakshyak@example.com'` → Full scan, index useless
	- Good: `WHERE created_at >= '2025-01-01' AND created_at < '2026-01-01'` or store normalized data if needed
	
- **SELECT * kills covering indexes**
	- If you `SELECT` columns not in the index → MySQL has to go back to clustered table for every row (bookmark lookup)
	- In high-traffic APIs → this adds 2–10× latency easily
	- Fix: Select only needed columns, or make index [[covering index]] by including extras via INCLUDE (MySQL 8.0+) or just add them to index.

- **Too many indexes = write penalty**
	- Every INSERT/UPDATE/DELETE must update **all** indexes → slows writes
	- Rule: Aim for 3–6 indexes per table max in most cases
	- Monitor with SHOW INDEX FROM table; and drop unused ones (use EXPLAIN + slow query log)