- check if JSON type if Array
```mysql
SELECT *
FROM your_table
WHERE JSON_TYPE(your_column) = 'ARRAY';
```
- `JSON_TYPE(column)` returns one of: `OBJECT` `ARRAY` `STRING` `INTEGER` `DECIMAL` `BOOLEAN` `NULL`.