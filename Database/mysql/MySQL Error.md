[[mysql]] [[SQL error]] [[mysql query]] [[connection pooling]]

# MySQL Error

> MySQL server error numbers and messages—duplicate key `1062`, deadlock `1213`, lock wait timeout `1205`—mapped to fixes and retry policies.

```txt
        MySQL Error ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Error-code fluency shows production readiness: which errors to retry (deadloc…

## Sources
- [MySQL Reference Manual — Server Error Message Reference](https://dev.mysql.com/doc/mysql-errors/en/server-error-reference.html) — deep-dive
- [MySQL Reference Manual — Client Error Codes](https://dev.mysql.com/doc/mysql-errors/en/client-error-reference.html) — overview

## Key Concepts
- **Numeric codes + messages:** drivers expose errno and SQLSTATE.
- **Retryable vs fatal:** deadlocks retry; duplicate keys usually need app logic.
- **Capacity signals:** 1040 → pooling and connection leaks.
- **Diagnostics:** `SHOW WARNINGS` / `SHOW ERRORS` in session.

## Technical Details
| Code | Message pattern | Action |
|------|-----------------|--------|
| 1062 | Duplicate entry | Upsert or return 409 |
| 1213 | Deadlock found | Retry transaction |
| 1205 | Lock wait timeout | Shorter txs; index tuning |
| 1040 | Too many connections | [[connection pooling]] |
| 1146 | Table doesn't exist | Migration drift |

- MySQL also returns SQLSTATE for portable handling—check driver docs for mappi…

```sql
SHOW WARNINGS;
SHOW ERRORS;
```

## Mistakes to Avoid
- **Mistake:** Not retrying deadlocks (1213) — they are normal under concurrency
- **Mistake:** Retrying duplicate-key inserts without idempotency
- **Mistake:** Ignoring 1040 until the site is down

## Pros/Cons or Trade-offs
- **Pro:** Stable numeric codes enable automated handling and dashboards.
- **Con:** Blind retries on non-idempotent operations can double-apply side effects; message text alone is brittle across versions/locales.

## Comparison
- vs [[SQL error]]: SQLSTATE/portable framing


### Use cases
- API layer maps 1062 → HTTP 409, retries 1213 with jitter, and alerts on 1040 …
