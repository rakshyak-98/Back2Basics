[[mysql]] [[mysql Programmable SQL]] [[SQL]]

# mysql function

> Built-in and user-defined SQL functions in MySQL—scalar functions in expressions, aggregate functions in `GROUP BY`, window functions in 8.0+.

## Built-in examples

```sql
SELECT UPPER(email), COUNT(*) FROM users GROUP BY domain(email);
SELECT id, ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) AS rn FROM employees;
```

## User-defined functions

```sql
CREATE FUNCTION add_tax(amount DECIMAL(10,2)) RETURNS DECIMAL(10,2)
DETERMINISTIC
RETURN amount * 1.08;
```

Stored functions differ from [[mysql triggers]] and stored procedures in call syntax and use cases.

## Sources

- MySQL Reference Manual — [Built-In Function Reference](https://dev.mysql.com/doc/refman/en/built-in-function-reference.html)
- MySQL Reference Manual — [CREATE FUNCTION](https://dev.mysql.com/doc/refman/en/create-function.html)
