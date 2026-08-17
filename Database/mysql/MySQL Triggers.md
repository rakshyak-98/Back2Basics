[[mysql Programmable SQL]] [[mysql table]] [[ACID]] [[mysql dump]] [[mysql data migrations]] [[MySQL Events]] [[MySQL CLI]]

# MySQL Triggers

> A MySQL trigger is stored program logic that runs automatically when a row is inserted, updated, or deleted — inside the same transaction as the statement that fired it.

---

## Why It Matters

Triggers are invisible to application code. Every INSERT, UPDATE, or DELETE — whether from your API, an admin console, a migration script, or a bulk import — executes the trigger body. That makes triggers powerful for audit trails, automatic timestamp columns, and enforcing invariants at the database layer. It also makes them dangerous: a slow trigger on a hot table can turn a simple bulk load into an hours-long operation, and trigger logic hidden in the database is easy to miss during code review.

---

## Sources

- [MySQL Reference Manual — Triggers](https://dev.mysql.com/doc/refman/en/triggers.html) — Complete reference for trigger semantics, privileges, and metadata tables.
- [MySQL Reference Manual — CREATE TRIGGER](https://dev.mysql.com/doc/refman/en/create-trigger.html) — Syntax, `BEFORE`/`AFTER` timing, and `FOR EACH ROW` rules with examples.
- [MySQL Reference Manual — Trigger Syntax and Examples](https://dev.mysql.com/doc/refman/en/trigger-syntax.html) — Worked examples including `OLD`/`NEW` row access patterns.

---

## Key Concepts

| Concept | Explanation |
|---------|-------------|
| **Timing** | `BEFORE` runs before the row change — can modify `NEW` values or raise errors to abort. `AFTER` sees the final row state. |
| **FOR EACH ROW** | MySQL triggers are row-level only; there is no statement-level trigger model. |
| **OLD / NEW** | `OLD` holds the previous row image (UPDATE/DELETE); `NEW` holds the incoming row (INSERT/UPDATE). |
| **Same transaction** | Trigger work commits or rolls back with the triggering statement — no partial application. |
| **Hidden call site** | Every client path pays the cost; application tests that mock the DB may miss trigger side effects. |
| **Definer vs invoker** | `DEFINER` clause controls whose privileges the trigger body runs under — security-sensitive on shared hosts. |

```txt
INSERT / UPDATE / DELETE on table T
        │
        ▼
  BEFORE trigger (optional) ── can modify NEW or SIGNAL error
        │
        ▼
  Row change applied
        │
        ▼
  AFTER trigger (optional) ── audit, cascade side effects
        │
        ▼
  Commit or rollback (entire statement + all triggers)
```

---

## Technical Details

### Audit trail pattern

Log every change to a shadow table — survives regardless of which application made the change.

```sql
CREATE TRIGGER audit_orders AFTER UPDATE ON orders
FOR EACH ROW
INSERT INTO orders_audit(order_id, old_status, new_status, old_total, new_total, changed_at)
VALUES (OLD.id, OLD.status, NEW.status, OLD.total, NEW.total, NOW());
```

### Automatic timestamp column

```sql
CREATE TRIGGER orders_set_updated BEFORE UPDATE ON orders
FOR EACH ROW
SET NEW.updated_at = CURRENT_TIMESTAMP;
```

Prefer `ON UPDATE CURRENT_TIMESTAMP` on the column definition when that alone satisfies the requirement — triggers add overhead and visibility cost.

### Reject invalid transitions

```sql
CREATE TRIGGER orders_block_cancelled BEFORE UPDATE ON orders
FOR EACH ROW
BEGIN
  IF OLD.status = 'cancelled' AND NEW.status <> 'cancelled' THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cannot reopen cancelled order';
  END IF;
END;
```

### Inspect existing triggers

```sql
SHOW TRIGGERS LIKE 'orders';
SELECT TRIGGER_NAME, EVENT_MANIPULATION, ACTION_TIMING, ACTION_STATEMENT
FROM information_schema.TRIGGERS
WHERE EVENT_OBJECT_TABLE = 'orders';
```

### Operations and migrations

- Rollback of the triggering statement undoes all trigger writes in the same transaction.
- Export definitions with `mysqldump --triggers` during [[mysql dump]] — restores can silently drop triggers if omitted.
- Bulk loads (`LOAD DATA`, large `INSERT … SELECT`) fire triggers per row — estimate runtime before running on production-sized data.
- Recursive trigger chains (trigger A fires trigger B which fires trigger A) need an explicit termination condition or they will loop until `max_sp_recursion_depth` is hit.

### Limits

- Maximum of one trigger per timing per event per table (`BEFORE INSERT`, `AFTER INSERT`, etc.).
- Triggers cannot use prepared statements or return result sets to the client.
- `TRUNCATE` does not fire `DELETE` triggers — use `DELETE` if audit coverage is required.

---

## Mistakes to Avoid

- Putting core business workflows **only** in triggers — application tests and onboarding docs will not mention them.
- Recursive trigger chains without a clear stop condition.
- Ignoring triggers when estimating migration or backfill runtime — a 10M-row import with a per-row audit trigger is not a 10M-row import.
- Using triggers as a substitute for change-data-capture when you need streaming analytics — triggers block the write path.
- Forgetting `DEFINER` security implications on shared MySQL instances.

---

## Pros/Cons or Trade-offs

| Pro | Con |
|-----|-----|
| Enforced for every client including ad-hoc SQL | Invisible in application repositories |
| Runs in the same transaction as the change | Errors abort the entire statement |
| Good for audit and timestamp invariants | Slow on bulk inserts; hard to unit-test |
| Database-layer enforcement when apps are inconsistent | Complicates schema migrations and replication |

---

## Comparison

| Alternative | When to prefer |
|-------------|----------------|
| Application service layer | Logic is complex, needs tests, or varies by tenant |
| `CHECK` constraints / generated columns | Simple invariants without procedural logic |
| [[MySQL Events]] | Time-based housekeeping, not row-level reactions |
| CDC (Debezium, binlog) | Downstream analytics without blocking writes |
| Declarative FK / `ON DELETE CASCADE` | Referential integrity without custom code |

---

## Use cases

- `orders_audit` table populated on every status change regardless of which microservice issued the UPDATE.
- `updated_at` stamping when legacy schemas cannot add `ON UPDATE CURRENT_TIMESTAMP` without a migration window.
- Blocking illegal state transitions (e.g. reopening a cancelled order) at the DB layer when multiple services write the same table.
