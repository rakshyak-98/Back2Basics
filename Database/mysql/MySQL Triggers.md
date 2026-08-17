[[mysql triggers]] [[mysql Programmable SQL]] [[mysql table]] [[ACID]] [[mysql dump]] [[mysql data migrations]] [[mysql Events]]

# MySQL Triggers

> Automatic stored logic fired on INSERT/UPDATE/DELETE — audit rows, stamp columns, or reject bad transitions in the same transaction as the triggering statement.

```txt
        MySQL Triggers ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers want awareness of hidden side effects: triggers complicate migra…

## Sources
- [MySQL Reference Manual — Triggers](https://dev.mysql.com/doc/refman/en/triggers.html) — deep-dive
- [MySQL Reference Manual — CREATE TRIGGER](https://dev.mysql.com/doc/refman/en/create-trigger.html) — deep-dive
- [MySQL Reference Manual — Trigger Syntax](https://dev.mysql.com/doc/refman/en/trigger-syntax.html) — overview
- [[mysql triggers]] — overview

## Key Concepts
- **Timing:** `BEFORE` can change `NEW` or signal errors; `AFTER` sees the row as stored.
- **FOR EACH ROW:** row-level access to `OLD` / `NEW` images.
- **Same transaction:** trigger work commits or rolls back with the statement
- **Hidden call site:** every client path (app, admin SQL, migration) pays the cost.
- **Complement to [[mysql triggers]]:** that leaf is the concise concept note; this note holds operational patterns.


- **Core:** A MySQL trigger is a named program associated with a table event (`BEFORE`/`A…

## Technical Details
- Audit pattern:

```sql
CREATE TRIGGER audit_orders AFTER UPDATE ON orders
FOR EACH ROW
INSERT INTO orders_audit(order_id, old_total, new_total, changed_at)
VALUES (OLD.id, OLD.total, NEW.total, NOW());
```

- Stamp columns:

```sql
CREATE TRIGGER orders_set_updated BEFORE UPDATE ON orders
FOR EACH ROW
SET NEW.updated_at = CURRENT_TIMESTAMP;
```

- Testing and operations:

- Rollback of the triggering statement undoes trigger writes.
- Export definitions with `mysqldump --triggers` during [[mysql dump]].
- Bulk loads and [[mysql data migrations]] must account for per-row trigger cost
- Recursive or cascading trigger chains need an explicit termination story.

- Limits worth remembering: statement-level triggers are not the MySQL model (r…

## Mistakes to Avoid
- **Mistake:** Putting core business workflows only in triggers so app tests ne…
- **Mistake:** Recursive trigger chains without a clear stop condition
- **Mistake:** Ignoring triggers when estimating migration or backfill runtime
- **Mistake:** Using triggers as a substitute for a proper change-data-capture …

## Pros/Cons or Trade-offs
- **Pro:** Enforced for every client, including ad-hoc SQL and forgotten code paths.
- **Con:** Invisible in application repos; errors abort statements; slow on bulk inserts.
- **Trade-off:** Trigger invariants vs application service layer + declarative constraints.

## Comparison
- vs [[mysql triggers]]: shared topic


### Use cases
- Write `orders_audit` on every status change regardless of which microservice …
