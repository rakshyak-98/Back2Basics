[[psql essential]] [[SQL/postgres]] [[GIN]]

# psql functions

> PostgreSQL built-in and user-defined functions—scalar, aggregate, window, and procedural languages (PL/pgSQL)—callable from [[SQL]].

## Examples

```sql
SELECT now(), lower('Hello'), jsonb_build_object('a', 1);

SELECT department, AVG(salary) OVER (PARTITION BY department) FROM employees;

CREATE OR REPLACE FUNCTION add_tax(numeric) RETURNS numeric
  LANGUAGE sql IMMUTABLE AS $$ SELECT $1 * 1.08 $$;
```

## Volatility categories

| Mark | Meaning |
|------|---------|
| IMMUTABLE | Same result for same args always |
| STABLE | Same within one statement |
| VOLATILE | Can change (default) |

Affects index expression eligibility and optimization.

## Sources

- PostgreSQL Documentation — [Functions](https://www.postgresql.org/docs/current/functions.html)
- PostgreSQL Documentation — [CREATE FUNCTION](https://www.postgresql.org/docs/current/sql-createfunction.html)
