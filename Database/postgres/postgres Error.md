[[SQL error]] [[SQL/postgres]] [[postgres parameter type error]] [[psql essential]]

# postgres Error

> PostgreSQL error reporting — `SQLSTATE`, `DETAIL`, `HINT`, and `CONTEXT` fields that turn failed queries into actionable fixes.





## Interview Relevance
Reliability interviews care which errors are retryable (`40001`, `40P01`) versus permanent constraint failures.

## Sources
- [Protocol error fields](https://www.postgresql.org/docs/current/protocol-error-fields.html) — deep-dive
- [Error Codes](https://www.postgresql.org/docs/current/errcodes-appendix.html) — overview

## Key Concepts
- **SQLSTATE:** Five-character standard/vendor code for programmatic handling.
- **DETAIL / HINT / CONTEXT:** Human debugging layers (values, suggestions, call stack).
- **Client APIs:** libpq `PQresultErrorField`; drivers expose equivalents.
- **Retry class:** Serialization and deadlock failures should be retried transactionally.

## Technical Details
```text
ERROR:  null value in column "email" violates not-null constraint
DETAIL:  Failing row contains (1, null, ...).
```

```c
PQresultErrorField(res, PG_DIAG_SQLSTATE);
```

Retry-worthy examples:
- `40001` serialization_failure
- `40P01` deadlock_detected

Related: [[postgres parameter type error]] for `42P18` / bind issues; [[SQL error]] for cross-engine mapping.

## Real-World Applications
API maps unique violations to HTTP 409; workers retry serialization failures with backoff; on-call reads HINT/CONTEXT before guessing.

## Pros/Cons or Trade-offs
- **Pro:** Rich, structured errors beat opaque “query failed.”
- **Con:** Drivers sometimes swallow fields unless configured.
- **Trade-off:** Logging full DETAIL (may contain PII) vs redaction.

## Comparison
vs MySQL: MySQL leans on numeric vendor codes (e.g. 1062); PostgreSQL centers SQLSTATE + DETAIL. See [[SQL error]].

## Mistakes to Avoid
- Retrying constraint violations forever.
- Logging secrets embedded in failed SQL text.
- Ignoring CONTEXT on PL/pgSQL failures.
