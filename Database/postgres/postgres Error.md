[[SQL error]] [[SQL/postgres]] [[postgres parameter type error]]

# postgres Error

> PostgreSQL error reporting—`SQLSTATE`, `DETAIL`, `HINT`, and `CONTEXT` fields for debugging failed queries and constraint violations.

## Example

```text
ERROR:  null value in column "email" violates not-null constraint
DETAIL:  Failing row contains (1, null, ...).
```

## Client handling (libpq)

```c
PQresultErrorField(res, PG_DIAG_SQLSTATE);
```

## Retry-worthy codes

- `40001` serialization_failure
- `40P01` deadlock_detected

## Sources

- PostgreSQL Documentation — [Error Reporting](https://www.postgresql.org/docs/current/protocol-error-fields.html)
- PostgreSQL Documentation — [Appendix A: Error Codes](https://www.postgresql.org/docs/current/errcodes-appendix.html)
