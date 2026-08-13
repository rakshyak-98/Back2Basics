[[mysql]] [[mysql index]] [[show query]] [[SQL]]

# mysql query

> Executing [[SQL]] against MySQL—`EXPLAIN` plans, optimizer hints, and patterns that use indexes instead of full table scans.

## Plan inspection

```sql
EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = 42 AND status = 'open';
```

Look for `type: ALL` (full scan) on large tables and `Using filesort` on big result sets.

## Parameterized queries

```sql
PREPARE stmt FROM 'SELECT id FROM users WHERE email = ?';
SET @email = 'a@b.com';
EXECUTE stmt USING @email;
```

Drivers handle preparation automatically—prefer driver APIs over string building.

## Hot-path checklist

- Filter columns indexed and selective
- Avoid functions on indexed columns (`WHERE YEAR(created_at)=2024`)
- Limit selected columns — enables [[covering index]] scans

## Sources

- MySQL Reference Manual — [EXPLAIN Output](https://dev.mysql.com/doc/refman/en/explain-output.html)
- MySQL Reference Manual — [Optimization](https://dev.mysql.com/doc/refman/en/optimization.html)
