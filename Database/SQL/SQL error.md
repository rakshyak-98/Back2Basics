[[SQL]] [[postgres Error]] [[MySQL Error]] [[postgres parameter type error]] [[ACID]] [[SQL/postgres]] [[mysql]]

# SQL error

> Database servers return structured error codes and messages — reading SQLSTATE, detail fields, and constraint names turns opaque failures into fast fixes.

```txt
        SQL error ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers ask how you map unique violations to HTTP status codes, when to …

## Sources
- [PostgreSQL Documentation — Appendix A. Error Codes](https://www.postgresql.org/docs/current/errcodes-appendix.html) — deep-dive
- [MySQL Reference Manual — Error Message Reference](https://dev.mysql.com/doc/mysql-errors/en/) — deep-dive
- ISO/IEC 9075 SQLSTATE classes — overview
- [PostgreSQL Documentation — Error Reporting and Logging](https://www.postgresql.org/docs/current/runtime-config-logging.html) — overview

## Key Concepts
- **Core:** A SQL error is a structured failure from the server: a five-character SQLSTAT…

## Technical Details
| Code | Meaning | Typical handling |
|------|---------|------------------|
| `23505` | unique_violation | HTTP 409 / user-visible conflict |
| `23503` | foreign_key_violation | 400/422 — missing parent row |
| `40001` | serialization_failure | Retry with backoff |
| `57014` | query_canceled | Timeout — tighten query or raise limit |
| `23502` | not_null_violation | Validation bug |

- PostgreSQL exposes SQLSTATE in `psql` (`\errverbose`) and client libraries (`…
- MySQL clients often surface errno + SQLSTATE

- Reading a message:

1. **Constraint name** — which index or FK failed.
2. **Detail** — key values (PostgreSQL often includes them).
3. **Hint** — missing column, typo, cast.
4. **Position** — character offset in the failing SQL.

```text
ERROR:  duplicate key value violates unique constraint "users_email_key"
DETAIL:  Key (email)=(a@b.com) already exists.
```

- Application handling:

- Map `23505` to HTTP 409 Conflict for APIs.
- Retry `40001` with exponential backoff and jitter; cap attempts.
- Log SQL text and parameters separately — never log passwords or tokens.
- Prefer typed exceptions from the driver over substring matching on `message`.

- See also [[postgres Error]], [[MySQL Error]], and [[postgres parameter type e…

## Mistakes to Avoid
- **Mistake:** Parsing human-readable messages instead of SQLSTATE / errno
- **Mistake:** Retrying unique violations in a tight loop (creates thundering h…
- **Mistake:** Logging bound parameters that contain secrets
- **Mistake:** Returning raw database text to end users (information leak and p…

## Pros/Cons or Trade-offs
- **Pro:** Stable codes enable uniform API and retry policy across services.
- **Con:** Vendor dialects differ; scraping English messages breaks on locale and version.
- **Trade-off:** Verbose DETAIL (great for debug) vs redacting PII in shared logs.

## Comparison
- vs application validation errors: DB errors are the last line when races slip…


### Use cases
- Signup API: unique email → `23505` → “email taken.” Inventory under SERIALIZA…
