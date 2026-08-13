[[postgres Error]] [[psql essential]] [[SQL/postgres]]

# postgres parameter type error

> `ERROR: could not determine data type of parameter $N` and related bind mismatches—usually fixed by explicit casts or typed placeholders in prepared statements.

## Common cause

```sql
-- Ambiguous parameter in prepared statement
PREPARE p AS SELECT * FROM t WHERE col = $1 AND other = $1;
-- Fix: cast
PREPARE p AS SELECT * FROM t WHERE col = $1::text AND other = $2::int;
```

## ORM / driver fixes

- Pass JavaScript `null` with type context
- Use `::timestamptz` for date parameters in raw SQL
- Enable `prepare: true` only when parameter types are stable

## Related errors

- `42804` datatype_mismatch
- `42P18` indeterminate_datatype

## Sources

- PostgreSQL Documentation — [PREPARE](https://www.postgresql.org/docs/current/sql-prepare.html)
- PostgreSQL Documentation — [Error Code 42P18](https://www.postgresql.org/docs/current/errcodes-appendix.html)
