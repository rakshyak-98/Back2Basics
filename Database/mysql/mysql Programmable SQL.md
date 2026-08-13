[[mysql function]] [[mysql triggers]] [[MySQL Events]] [[SQL]]

# mysql Programmable SQL

> Server-side logic in MySQL—stored procedures, functions, triggers, and scheduled events—that runs inside `mysqld` with shared privileges and connection context.

## Components

| Object | Fires |
|--------|-------|
| Stored procedure | `CALL proc()` |
| Function | Expression in SQL |
| [[mysql triggers]] | `BEFORE`/`AFTER` DML on table |
| [[MySQL Events]] | Scheduler cron |

## Tradeoffs

- **Pros:** Centralized invariants, fewer round trips
- **Cons:** Hidden logic, harder to test/version, deployment coupling

Prefer application code for complex workflows unless DBAs require database-enforced rules.

## Sources

- MySQL Reference Manual — [Stored Objects](https://dev.mysql.com/doc/refman/en/stored-objects.html)
