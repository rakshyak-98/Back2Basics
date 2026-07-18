
[PREPARE statement](https://dev.mysql.com/doc/refman/8.0/en/sql-prepared-statements.html)
```mysql
PREPARE stmt FROM 'UPDATE table_name set column_name = ? where id = 1';
SET @json = '[]';
EXECUTE stmt USING @json;
DEALLOCATE PROCEDURE stmt;
```

```mysql
SHOW STATUS LIKE "Prepared%";
```

## View all the prepared statement
```sql
SELECT STATEMENT_ID, STATEMENT_NAME, SQL_TEXT FROM performance_schema.prepared_statements_instances;

SELECT STATEMENT_NAME, SQL_TEXT FROM
performance_schema.prepared_statements_instances;
```

> [!NOTE]
> - **No**, you **cannot** use literals directly in the `EXECUTE ... USING` statement like this
```mysql
EXECUTE stmt USING 10, 2, Home; -- this is invalid.
```
- have to assign literals to variables.
```mysql
SET @a = 10;
SET @b = 2;
SET @c = 'Home';
EXECUTE stmt USING @a, @b, @c;

```

| Name                        | MySQL Term / Category        | Description                                     |
| --------------------------- | ---------------------------- | ----------------------------------------------- |
| `PREPARE`, `EXECUTE`        | **Prepared Statements**      | Runtime dynamic SQL with placeholders           |
| `Stored Procedure`          | **Stored Routine**           | Reusable block of SQL with input/output params  |
| `Function`                  | **Stored Function**          | Returns a single value; used in SQL expressions |
| `Trigger`                   | **Trigger**                  | Auto-run SQL on table events (`INSERT`, etc.)   |
| `Event`                     | **Event Scheduler / Event**  | Scheduled SQL tasks                             |
| `View`                      | **View (Virtual Table)**     | Query abstraction; read-only or updatable       |
| `User-defined Variable`     | **Session Variable**         | Temporary scoped variable prefixed with `@`     |
| `Control Flow` (`IF`, etc.) | **Flow Control Constructs**  | Logic inside procedures/functions               |
| `EXECUTE IMMEDIATE`         | Not in SQL; MySQL Shell only | Used in `mysqlsh`, not standard MySQL SQL       |
