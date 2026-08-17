[[psql essential]] [[SQL/postgres]] [[GIN]] [[SQL]]

# psql functions

> PostgreSQL built-in and user-defined functions — scalar, aggregate, window, and procedural languages (PL/pgSQL) callable from [[SQL]].

```txt
        psql functions ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Volatility (`IMMUTABLE`/`STABLE`/`VOLATILE`) and when a function can be used …

## Sources
- [Functions](https://www.postgresql.org/docs/current/functions.html) — overview
- [CREATE FUNCTION](https://www.postgresql.org/docs/current/sql-createfunction.html) — deep-dive

## Key Concepts
- **Built-ins:** Rich JSON, text, date, and aggregate toolkit.
- **Window functions:** Analytics without collapsing groups.
- **UDF languages:** `sql`, `plpgsql`, and others.
- **Volatility:** Drives optimization and index eligibility.

## Technical Details
```sql
SELECT now(), lower('Hello'), jsonb_build_object('a', 1);

SELECT department, AVG(salary) OVER (PARTITION BY department) FROM employees;

CREATE OR REPLACE FUNCTION add_tax(numeric) RETURNS numeric
  LANGUAGE sql IMMUTABLE AS $$ SELECT $1 * 1.08 $$;
```

| Mark | Meaning |
|------|---------|
| IMMUTABLE | Same result for same args always |
| STABLE | Same within one statement |
| VOLATILE | Can change (default) |

## Mistakes to Avoid
- **Mistake:** Marking volatile logic `IMMUTABLE`
- **Mistake:** Heavy PL/pgSQL in hot OLTP paths without measurement
- **Mistake:** Forgetting `SECURITY DEFINER` risks on privileged functions

## Pros/Cons or Trade-offs
- **Pro:** Push compute to the server next to the data; expressive SQL.
- **Con:** Mislabeled volatility causes wrong plans or rejected indexes.
- **Trade-off:** DB functions vs application libraries for shared business rules.

## Comparison
- vs [[mysql function]]: Postgres volatility categories and extension languages…


### Use cases
- Immutable helpers for generated/stored expressions
