`\G` -> in MySQL CLI the `\G` is not the same as semicolon. It's a command terminator that changes the output format.
- outputs results in standard tabular format (columns as headers, rows as lines)
- use `\G` when, the table has many columns, you want vertical readability instead of horizontal table.

- check if JSON type if Array
```mysql
SELECT *
FROM your_table
WHERE JSON_TYPE(your_column) = 'ARRAY';
```
- `JSON_TYPE(column)` returns one of: `OBJECT` `ARRAY` `STRING` `INTEGER` `DECIMAL` `BOOLEAN` `NULL`.