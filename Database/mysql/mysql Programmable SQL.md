[[mysql function]] [[mysql triggers]] [[MySQL Events]] [[SQL]] [[mysql]]

# mysql Programmable SQL

> Server-side logic in MySQL — stored procedures, functions, triggers, and scheduled events that run inside `mysqld` with the server’s privileges and connection context.

```txt
        mysql Programmable ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Expect “when would you put logic in the database versus the app?” Signal: you…

## Sources
- [MySQL Stored Objects](https://dev.mysql.com/doc/refman/en/stored-objects.html) — overview
- [MySQL Stored Programs](https://dev.mysql.com/doc/refman/en/stored-programs-security.html) — deep-dive

## Key Concepts
- **Stored procedure:** Invoked with `CALL`; can run multi-statement workflows.
- **Function:** Used in expressions
- **[[mysql triggers]]:** Fire `BEFORE`/`AFTER` DML per row (or statement, depending on definition).
- **[[MySQL Events]]:** Scheduler-driven jobs inside the server (cron-like).

## Technical Details
| Object | How it runs |
|--------|-------------|
| Stored procedure | `CALL proc()` |
| Function | Inside `SELECT` / expressions |
| Trigger | DML on a table |
| Event | Event scheduler timeline |

- Definer vs invoker security matters: `DEFINER` runs as the owner

## Mistakes to Avoid
- **Mistake:** Hiding business-critical branching only in triggers (invisible t…
- **Mistake:** Overusing events instead of an observable job runner with retrie…
- **Mistake:** Ignoring `DEFINER` privileges on shared production accounts

## Pros/Cons or Trade-offs
- **Pro:** Centralized invariants, fewer round trips, works for every client language.
- **Con:** Harder to test, version, and code-review; couples deploys to DDL; opaque to most app stacks.
- **Trade-off:** Prefer application code for complex workflows unless DBAs require database-enforced rules.

## Comparison
- vs app services: programmable SQL shares the transaction with the triggering …


### Use cases
- Enforce audit columns or soft invariants that every client must obey
