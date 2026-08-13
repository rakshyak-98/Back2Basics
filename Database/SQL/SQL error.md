[[SQL]] [[postgres Error]] [[MySQL Error]] [[postgres parameter type error]]

# SQL error

> Database servers return structured error codes and messages—learning to read SQLSTATE, detail fields, and constraint names turns opaque failures into fast fixes.

## Standard SQLSTATE

Five-character codes (ISO SQL). Examples:

| Code | Meaning |
|------|---------|
| `23505` | unique_violation |
| `23503` | foreign_key_violation |
| `40001` | serialization_failure (retry) |
| `57014` | query_canceled (timeout) |

PostgreSQL exposes `SQLSTATE` in `psql` and client libraries. MySQL uses vendor error numbers (e.g. `1062` duplicate entry).

## Reading an error message

1. **Constraint name** — which index or FK failed
2. **Detail** — key values involved (PostgreSQL often includes)
3. **Hint** — suggested fix (missing column, typo)
4. **Position** — character offset in failing SQL

```text
ERROR:  duplicate key value violates unique constraint "users_email_key"
DETAIL:  Key (email)=(a@b.com) already exists.
```

## Application handling

- Map `23505` to HTTP 409 Conflict for APIs
- Retry `40001` with exponential backoff
- Log `query` and `parameters` separately — never log secrets

## Sources

- PostgreSQL Documentation — [Appendix A. PostgreSQL Error Codes](https://www.postgresql.org/docs/current/errcodes-appendix.html)
- MySQL Reference Manual — [Error Message Reference](https://dev.mysql.com/doc/mysql-errors/en/)
