[[mysql]] [[mysql table]] [[mysql triggers]]

# MySQL triggers

> One-line: automatic SQL on INSERT/UPDATE/DELETE — audit, denormalization, validation; hidden logic that breaks migrations and surprises ORMs.

## Mental model

Triggers run **inside the same transaction** as the triggering statement (InnoDB). **BEFORE** triggers can modify `NEW` row; **AFTER** triggers see committed change context but can't modify triggering row.

```
INSERT INTO orders ...
        │
        ▼
BEFORE INSERT trigger (validate, set defaults)
        │
        ▼
row written
        │
        ▼
AFTER INSERT trigger (audit log, counter update)
```

MySQL allows **one trigger per timing/event/table** (before 5.7 had limits; 8.0+ multiple with different names). Logic in triggers is **invisible to app code** — hard to test and version.

## Standard config / commands

### List triggers

```sql
SELECT TRIGGER_NAME, EVENT_MANIPULATION, EVENT_OBJECT_TABLE,
       ACTION_TIMING, ACTION_STATEMENT
FROM INFORMATION_SCHEMA.TRIGGERS
WHERE TRIGGER_SCHEMA = DATABASE();
```

```sql
SHOW TRIGGERS LIKE 'orders%';
```

### Create BEFORE INSERT

```sql
DELIMITER //
CREATE TRIGGER before_employee_insert
BEFORE INSERT ON employees
FOR EACH ROW
BEGIN
  IF NEW.created_at IS NULL THEN
    SET NEW.created_at = NOW();
  END IF;
END//
DELIMITER ;
```

### AFTER UPDATE audit

```sql
CREATE TRIGGER orders_audit_update
AFTER UPDATE ON orders
FOR EACH ROW
INSERT INTO orders_audit (order_id, old_status, new_status, changed_at)
VALUES (OLD.id, OLD.status, NEW.status, NOW());
```

### Drop

```sql
DROP TRIGGER IF EXISTS before_employee_insert;
```

### Dump with triggers (schema only)

```bash
mysqldump -u root -p --no-data --triggers mydb > schema.sql
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| INSERT fails mysteriously | Trigger SIGNAL/validation | `SHOW TRIGGERS`; test trigger body |
| Double audit rows | App + trigger both write | Remove duplicate path |
| Migration fails on trigger | Invalid def after ALTER | Drop/recreate trigger in migration |
| Replication error on replica | Definer / SQL mode mismatch | `SHOW CREATE TRIGGER`; align sql_mode |
| Slow bulk load | Per-row trigger fire | Disable trigger session (privilege) or batch ETL |
| ORM row count wrong | Hidden side effects | Move logic to app service layer |

## Gotchas

> [!WARNING]
> **Cascade triggers** — UPDATE trigger causing UPDATE on same table → recursion limits / loops.

> [!WARNING]
> **DEFINER=root@localhost** — breaks on restore to different host; use invoker or explicit definer.

> [!WARNING]
> **Not in all backup tools by default** — include `--triggers` in mysqldump.

## When NOT to use

- **Core business rules** — enforce in application with tests; triggers for DBA audit only.
- **Cross-database actions** — unsupported/unreliable; use job queue.
- **Heavy computation per row** — blocks transaction; use async worker.

## Related

[[mysql triggers]] [[mysql table]] [[Alter table]] [[mysql dump]] [[database migration]]
