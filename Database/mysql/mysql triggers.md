[[mysql]] [[mysql Programmable SQL]] [[mysql transaction]]

# mysql triggers

> SQL that runs automatically BEFORE/AFTER INSERT, UPDATE, or DELETE on a table — same transaction as the firing statement.

---

## Mental model

**Say it in one breath:** Attach a trigger to a table event; use `NEW`/`OLD` row values; it commits or rolls back with the statement — silent unless you log yourself.

```txt
UPDATE hotels
   │
   ▼
AFTER UPDATE trigger ──► INSERT hotel_audit (OLD.*, NEW.*)
   │
   └── same txn as the UPDATE
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **BEFORE** | Runs before write | “Can change `NEW.col` before store.” |
| **AFTER** | Runs after write | “Good for audit side tables.” |
| **NEW / OLD** | Incoming / previous row | “UPDATE has both; INSERT only NEW.” |
| **FOR EACH ROW** | Per affected row | “Bulk UPDATE = N trigger runs.” |

---

## Standard config / commands

```sql
CREATE TRIGGER log_hotel_update
AFTER UPDATE ON hotels
FOR EACH ROW
INSERT INTO hotel_audit (hotel_id, old_name, new_name, changed_at)
VALUES (OLD.id, OLD.name, NEW.name, NOW());

CREATE TRIGGER set_created
BEFORE INSERT ON tableName
FOR EACH ROW
SET NEW.created_at = NOW();

SELECT TRIGGER_NAME FROM information_schema.TRIGGERS
WHERE TRIGGER_SCHEMA = DATABASE();

DROP TRIGGER IF EXISTS after_hotel_update_create_pages;
```

| Knob | Why it matters |
|------|----------------|
| BEFORE vs AFTER | Mutate NEW only in BEFORE |
| One trigger per event/timing (older limits) | MySQL versions differ; check docs |
| No dedicated trigger log | Instrument yourself |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Side effects missing | Trigger exists? Enabled? | `SHOW TRIGGERS` / information_schema |
| Mysterious constraint errors | Trigger DML failing | Read error; fix trigger body |
| Slow bulk loads | FOR EACH ROW cost | Disable triggers for load (careful) or batch elsewhere |
| Recursive / cascading surprises | Trigger updates same/other tables | Simplify; move logic to app |

---

## Gotchas

> [!WARNING]
> **Silent execution** — MySQL doesn’t keep a trigger audit log by default.

> [!WARNING]
> **Seeds/migrations fire triggers** — bulk import can spam audit tables or send side effects.

---

## When NOT to use

- **Emails, HTTP, PDFs** — don’t hide I/O in triggers; use application/outbox.
- **Complex multi-table workflows** — prefer explicit transactions in the service.

---

## Related

[[mysql Programmable SQL]] [[mysql transaction]] [[MySQL Triggers]] [[mysql table]]
