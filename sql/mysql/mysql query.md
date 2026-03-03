`\G` -> in MySQL CLI the `\G` is not the same as semicolon. It's a command terminator that changes the output format.
- outputs results in standard tabular format (columns as headers, rows as lines)
- use `\G` when, the table has many columns, you want vertical readability instead of horizontal table.

- check if JSON type if Array
```mysql
SELECT *
FROM your_table
WHERE JSON_TYPE(your_column) = 'ARRAY';
``` - `JSON_TYPE(column)` returns one of: `OBJECT` `ARRAY` `STRING` `INTEGER` `DECIMAL` `BOOLEAN` `NULL`.

```sql
SHOW FULL TABLE WHERE Table_type = "VIEW";
SHOW FULL TABLE WHERE Table_type = "BASE TABLE";
```

## Format dates

```sql
 SELECT 
     DATE_FORMAT(MAX(trxnDate), '%d %b %Y, %W') AS last_revenue_date_formatted,
     MAX(trxnDate) AS last_revenue_date_raw,
     COUNT(*) AS number_of_bills_on_that_date,
     ROUND(SUM(roomRevenue), 2) AS total_room_revenue_on_last_date,
     ROUND(SUM(amount), 2) AS total_amount_on_last_date
 FROM transactions
 WHERE transactionType = 'Bill'
   AND (roomRevenue > 0 OR amount > 0)
 GROUP BY trxnDate
 ORDER BY trxnDate DESC
 LIMIT 1;

```

# Show details about table

```mysql
SHOW FULL COLUMNS FROM "<table name>";
```

**COALESCE** -> returns first non-Null value from left to right.
- SQL null-safe fallback operator.
- Used for providing default/fallback when column value is `NULL`.

### user specific query

```sql
SELECT CURRENT_USER();
```

## Extract database metadata

```sql
SELECT 
  table_name, 
  column_name, 
  data_type 
FROM information_schema.columns 
WHERE table_schema = 'your_db';
```