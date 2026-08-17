[[SQL error]] [[SQL/postgres]] [[postgres parameter type error]] [[psql essential]]

# postgres Error

> PostgreSQL error reporting — `SQLSTATE`, `DETAIL`, `HINT`, and `CONTEXT` fields that turn failed queries into actionable fixes.

```txt
        postgres Error ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Reliability interviews care which errors are retryable (`40001`, `40P01`) ver…

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

- Retry-worthy examples:

- `40001` serialization_failure
- `40P01` deadlock_detected

- Related: [[postgres parameter type error]] for `42P18` / bind issues

## Mistakes to Avoid
- **Mistake:** Retrying constraint violations forever
- **Mistake:** Logging secrets embedded in failed SQL text
- **Mistake:** Ignoring CONTEXT on PL/pgSQL failures

## Pros/Cons or Trade-offs
- **Pro:** Rich, structured errors beat opaque “query failed.”
- **Con:** Drivers sometimes swallow fields unless configured.
- **Trade-off:** Logging full DETAIL (may contain PII) vs redaction.

## Comparison
- vs MySQL: MySQL leans on numeric vendor codes (e.g. 1062)


### Use cases
- API maps unique violations to HTTP 409
