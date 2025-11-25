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

```sql
SHOW FULL TABLE WHERE Table_type = "VIEW";
SHOW FULL TABLE WHERE Table_type = "BASE TABLE";
```

# Show details about table
```mysql
SHOW FULL COLUMNS FROM "<table name>";
```

**COALESCE** -> returns first non-Null value from left to right.
- SQL null-safe fallback operator.
- Used for providing default/fallback when column value is `NULL`.