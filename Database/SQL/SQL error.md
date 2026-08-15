[[SQL]] [[postgres Error]] [[MySQL Error]] [[postgres parameter type error]] [[ACID]] [[SQL/postgres]] [[mysql]]

# SQL error

> Database servers return structured error codes and messages — reading SQLSTATE, detail fields, and constraint names turns opaque failures into fast fixes.

## Interview Relevance

Interviewers ask how you map unique violations to HTTP status codes, when to retry serialization failures, and how you log failures without leaking secrets. Signal: you treat SQLSTATE as a contract, not a string to scrape ad hoc.

## Sources

- [PostgreSQL Documentation — Appendix A. Error Codes](https://www.postgresql.org/docs/current/errcodes-appendix.html) — deep-dive
- [MySQL Reference Manual — Error Message Reference](https://dev.mysql.com/doc/mysql-errors/en/) — deep-dive
- ISO/IEC 9075 SQLSTATE classes — overview
- [PostgreSQL Documentation — Error Reporting and Logging](https://www.postgresql.org/docs/current/runtime-config-logging.html) — overview

## Core Definition

A SQL error is a structured failure from the server: a five-character SQLSTATE (ISO) and/or a vendor number, plus message, detail, hint, and often a constraint or position — enough to decide retry, conflict, or fix-the-query.

## Key Concepts

- **SQLSTATE:** portable five-character code (`class` + `subclass`).
- **Vendor number:** MySQL-style integers (e.g. `1062` duplicate entry) alongside or instead of SQLSTATE in clients.
- **Constraint name:** which unique index or foreign key failed.
- **Detail / Hint / Position:** values involved, suggested fix, character offset in the SQL text.
- **Retryable vs terminal:** `40001` serialization_failure often retries; `23505` unique_violation usually maps to conflict for the client.

## Technical Details

| Code | Meaning | Typical handling |
|------|---------|------------------|
| `23505` | unique_violation | HTTP 409 / user-visible conflict |
| `23503` | foreign_key_violation | 400/422 — missing parent row |
| `40001` | serialization_failure | Retry with backoff |
| `57014` | query_canceled | Timeout — tighten query or raise limit |
| `23502` | not_null_violation | Validation bug |

PostgreSQL exposes SQLSTATE in `psql` (`\errverbose`) and client libraries (`SQLSTATE` / `sqlstate`). MySQL clients often surface errno + SQLSTATE; duplicate key is `1062` / `23000`.

Reading a message:

1. **Constraint name** — which index or FK failed.
2. **Detail** — key values (PostgreSQL often includes them).
3. **Hint** — missing column, typo, cast.
4. **Position** — character offset in the failing SQL.

```text
ERROR:  duplicate key value violates unique constraint "users_email_key"
DETAIL:  Key (email)=(a@b.com) already exists.
```

Application handling:

- Map `23505` to HTTP 409 Conflict for APIs.
- Retry `40001` with exponential backoff and jitter; cap attempts.
- Log SQL text and parameters separately — never log passwords or tokens.
- Prefer typed exceptions from the driver over substring matching on `message`.

See also [[postgres Error]], [[MySQL Error]], and [[postgres parameter type error]] for engine-specific traps.

## Real-World Applications

Signup API: unique email → `23505` → “email taken.” Inventory under SERIALIZABLE: `40001` → automatic retry. Ops dashboards alert on rising `57014` as a sign of missing indexes or runaway reports.

## Pros/Cons or Trade-offs

- **Pro:** Stable codes enable uniform API and retry policy across services.
- **Con:** Vendor dialects differ; scraping English messages breaks on locale and version.
- **Trade-off:** Verbose DETAIL (great for debug) vs redacting PII in shared logs.

## Comparison

vs application validation errors: DB errors are the last line when races slip past checks. vs [[ACID]] isolation failures: `40001` is the engine saying concurrent schedules conflict — retry, do not treat as a schema bug. vs HTTP 500: most constraint violations are client/conflict issues, not server crashes.

## Mistakes to Avoid

- Parsing human-readable messages instead of SQLSTATE / errno.
- Retrying unique violations in a tight loop (creates thundering herds on hot keys).
- Logging bound parameters that contain secrets.
- Returning raw database text to end users (information leak and poor UX).
