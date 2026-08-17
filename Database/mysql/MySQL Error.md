[[mysql]] [[SQL error]] [[mysql query]] [[connection pooling]]

# MySQL Error

> MySQL server error numbers and messages—duplicate key `1062`, deadlock `1213`, lock wait timeout `1205`—mapped to fixes and retry policies.





## Interview Relevance
Error-code fluency shows production readiness: which errors to retry (deadlock), which are client bugs (duplicate key), and which are capacity issues (too many connections). Pairs with [[SQL error]] for broader SQLSTATE thinking.

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

MySQL also returns SQLSTATE for portable handling—check driver docs for mapping.

```sql
SHOW WARNINGS;
SHOW ERRORS;
```

## Real-World Applications
API layer maps 1062 → HTTP 409, retries 1213 with jitter, and alerts on 1040 spikes. Example: payment service retries deadlocks up to 3 times, then fails the request with a safe idempotent replay path.

## Pros/Cons or Trade-offs
- **Pro:** Stable numeric codes enable automated handling and dashboards.
- **Con:** Blind retries on non-idempotent operations can double-apply side effects; message text alone is brittle across versions/locales.

## Comparison
vs [[SQL error]]: SQLSTATE/portable framing; this note is MySQL errno-centric. vs application exceptions: always preserve the MySQL code in logs—string matching “Duplicate” is fragile.

## Mistakes to Avoid
- Not retrying deadlocks (1213) — they are normal under concurrency.
- Retrying duplicate-key inserts without idempotency — infinite loops or silent doubles.
- Ignoring 1040 until the site is down — treat as capacity/leak incident.
