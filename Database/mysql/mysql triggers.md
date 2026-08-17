[[mysql Programmable SQL]] [[mysql table]] [[ACID]] [[mysql data migrations]] [[MySQL Triggers]]

# mysql triggers

> Row-level actions fired automatically on INSERT/UPDATE/DELETE — set audit columns, cascade logic, or guard invalid transitions inside the same statement transaction.

```txt
        mysql triggers ──┬── Why it matters
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
- [CREATE TRIGGER](https://dev.mysql.com/doc/refman/en/create-trigger.html) — deep-dive
- [Trigger Syntax](https://dev.mysql.com/doc/refman/en/trigger-syntax.html) — overview

## Key Concepts
- **Timing:** `BEFORE` / `AFTER` × `INSERT` / `UPDATE` / `DELETE`.
- **FOR EACH ROW:** Access `OLD` / `NEW` row images.
- **Same transaction:** Trigger work commits or rolls back with the triggering statement.
- **Visibility:** Easy to forget during app reviews and bulk loads.

## Technical Details
```sql
CREATE TRIGGER orders_set_updated BEFORE UPDATE ON orders
FOR EACH ROW SET NEW.updated_at = CURRENT_TIMESTAMP;
```

- Also see [[MySQL Triggers]] for audit patterns and dump flags.
- Bulk loads and [[mysql data migrations]] must account for trigger cost.

## Mistakes to Avoid
- **Mistake:** Business workflows that only exist in triggers
- **Mistake:** Recursive trigger chains without a clear termination story
- **Mistake:** Ignoring triggers when estimating migration runtime

## Pros/Cons or Trade-offs
- **Pro:** Enforced for every client, including ad-hoc SQL.
- **Con:** Hidden logic; errors abort statements; slow on bulk inserts.
- **Trade-off:** Trigger invariants vs application service layer + DB constraints.

## Comparison
- vs [[mysql function]] / procedures: triggers are implicit; functions/procedur…


### Use cases
- Maintain `updated_at`, write audit rows, or reject illegal status transitions…
