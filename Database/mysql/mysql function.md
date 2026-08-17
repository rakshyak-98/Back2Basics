[[mysql]] [[mysql Programmable SQL]] [[SQL]] [[mysql triggers]]

# mysql function

> Built-in and user-defined SQL functions in MySQL—scalar functions in expressions, aggregate functions in `GROUP BY`, window functions in 8.0+.





## Interview Relevance
Function questions span built-ins vs UDFs, DETERMINISTIC marking, and window functions (`ROW_NUMBER`). Distinguish functions from triggers and stored procedures.

## Sources
- [MySQL Reference Manual — Built-In Function Reference](https://dev.mysql.com/doc/refman/en/built-in-function-reference.html) — overview
- [MySQL Reference Manual — CREATE FUNCTION](https://dev.mysql.com/doc/refman/en/create-function.html) — deep-dive

## Key Concepts
- **Scalar / aggregate / window:** different call contexts in SELECT.
- **User-defined functions:** `CREATE FUNCTION` with return type and DETERMINISTIC hint.
- **Not triggers/procedures:** different call syntax and use cases ([[mysql triggers]]).

## Technical Details
Built-in examples:

```sql
SELECT UPPER(email), COUNT(*) FROM users GROUP BY domain(email);
SELECT id, ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) AS rn FROM employees;
```

User-defined functions:

```sql
CREATE FUNCTION add_tax(amount DECIMAL(10,2)) RETURNS DECIMAL(10,2)
DETERMINISTIC
RETURN amount * 1.08;
```

Stored functions differ from [[mysql triggers]] and stored procedures in call syntax and use cases.

## Real-World Applications
Reporting queries with window functions and small UDFs for shared business formulas. Example: rank employees per department with `ROW_NUMBER()` instead of self-joins.

## Pros/Cons or Trade-offs
- **Pro:** Expressive SQL; UDFs centralize simple calculations next to data.
- **Con:** Heavy UDFs in hot queries hurt optimizer choices; binary UDFs raise security/ops burden.

## Comparison
vs [[mysql triggers]]: triggers fire on DML events; functions are invoked in expressions. vs application code: keep complex domain logic in the app unless there is a clear pushdown reason.

## Mistakes to Avoid
- Marking non-deterministic functions as DETERMINISTIC — wrong replication/optimizer assumptions.
- Using UDFs for what should be a join or generated column.
- Forgetting window functions need MySQL 8.0+.
