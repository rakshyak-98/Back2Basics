<!-- note-strategy: operational -->
[[mysql]] [[mysql Programmable SQL]] [[Configuration]]

# mysql events 1

> MySQL Event Scheduler — cron inside the database for one-shot or recurring SQL.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Create an EVENT that runs SQL on a schedule; nothing fires unless `event_scheduler=ON` (persist it in `my.cnf` or it dies after restart).

```txt
event_scheduler=ON
      │
      ▼
CREATE EVENT … ON SCHEDULE EVERY / AT …
      │
      ▼
DO INSERT/DELETE/CALL …
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Event** | Scheduled SQL job | “DB-side cron.” |
| **event_scheduler** | Global on/off | “OFF ⇒ events exist but never run.” |
| **AT / EVERY** | Once vs recurring | “AT for one cleanup; EVERY for stats.” |
| **ENABLE/DISABLE** | Pause without DROP | `ALTER EVENT … DISABLE` |

---

## Standard config / commands

```sql
SET GLOBAL event_scheduler = ON;
SHOW VARIABLES LIKE 'event_scheduler';

CREATE EVENT my_event
ON SCHEDULE EVERY 1 DAY STARTS CURRENT_TIMESTAMP
DO INSERT INTO logs(message, created_at) VALUES ('Daily log entry', NOW());

CREATE EVENT cleanup_old_data
ON SCHEDULE AT TIMESTAMP '2025-08-21 00:00:00'
DO DELETE FROM sessions WHERE created_at < NOW() - INTERVAL 30 DAY;

SHOW EVENTS;
SHOW CREATE EVENT my_event\G
ALTER EVENT my_event DISABLE;
DROP EVENT my_event;
```

```ini
# /etc/mysql/my.cnf
[mysqld]
event_scheduler=ON
```

| Knob | Why it matters |
|------|----------------|
| GLOBAL scheduler | Must survive restart via config |
| EVENT privilege | Who can create/alter events |
| DO body | Keep short; heavy jobs → external worker |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Event never runs | `event_scheduler` | SET GLOBAL ON; persist in my.cnf |
| Works until reboot | Only runtime SET | Add `event_scheduler=ON` to config |
| Permission denied | Missing EVENT priv | GRANT EVENT ON db.* |
| Overlap / pile-up | Long DO body | Shorten job or move to queue worker |

---

## Gotchas

> [!WARNING]
> **Restart clears non-persisted scheduler** — runtime `SET GLOBAL` alone is a classic footgun.

> [!WARNING]
> **No rich observability** — check `SHOW EVENTS` / logs; don’t assume success without monitoring the side effects.

---

## When NOT to use

- **application-level jobs with retries/backoff** — use a real worker/queue.
- **Multi-primary / unclear ownership** — events can double-fire; prefer one scheduler outside the DB.

---

## Related

[[MySQL Events]] [[Configuration]] [[mysql Programmable SQL]] [[mysql]]
