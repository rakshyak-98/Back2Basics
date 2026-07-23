[[mysql]] [[mysql triggers]] [[mysql function]] [[OLTP]]

# MySQL Events

> Built-in job scheduler — run SQL on a cron-like schedule inside the server; no external cron required, but visibility and failure handling are weaker than app-level workers.

## Mental model

MySQL Event Scheduler is a background thread that fires **EVENT** objects at `AT` or `EVERY` intervals. Each event runs a single SQL body (often `BEGIN … END` block).

```
event_scheduler thread (ON)
        │
        ▼
  reads mysql.event table
        │
        ▼
  fires DO clause ──► runs as definer (privileges matter)
```

Requires global `event_scheduler = ON`. Events are metadata — survive restart if saved to disk (InnoDB system tables / mysql schema).

## Standard config / commands

### Enable scheduler

```sql
-- Session check
SHOW VARIABLES LIKE 'event_scheduler';

-- Enable globally (my.cnf for persistence)
SET GLOBAL event_scheduler = ON;
```

```ini
# my.cnf
[mysqld]
event_scheduler = ON
```

### Create recurring event

```sql
CREATE EVENT cleanup_sessions
ON SCHEDULE EVERY 1 DAY
STARTS CURRENT_TIMESTAMP + INTERVAL 1 HOUR
ON COMPLETION PRESERVE
ENABLE
COMMENT 'Purge expired sessions nightly'
DO
  DELETE FROM sessions WHERE expired = 1 AND updated_at < NOW() - INTERVAL 30 DAY;
```

### One-shot event

```sql
CREATE EVENT migrate_flag_once
ON SCHEDULE AT '2026-08-01 03:00:00'
DO
  UPDATE schema_migrations SET phase = 2 WHERE phase = 1;
```

### Inspect and manage

```sql
SHOW EVENTS FROM mydb;
SHOW CREATE EVENT mydb.cleanup_sessions\G

ALTER EVENT cleanup_sessions DISABLE;
ALTER EVENT cleanup_sessions ENABLE;
DROP EVENT IF EXISTS cleanup_sessions;
```

### Definer and security

```sql
CREATE DEFINER=`app_admin`@`localhost` EVENT ...
-- Runs with definer's privileges — prefer dedicated least-privilege definer
```

### Error handling in body

```sql
DO
BEGIN
  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    INSERT INTO event_errors (msg, at) VALUES ('cleanup failed', NOW());
  END;
  DELETE FROM sessions WHERE expired = 1;
END
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Event never runs | `event_scheduler` OFF | `SET GLOBAL event_scheduler = ON`; persist in config |
| Event DISABLED after error | `SHOW EVENTS` → Status | `ALTER EVENT … ENABLE`; fix SQL in body |
| Runs but no rows affected | Wrong WHERE; timezone | Verify `time_zone`; test DO clause manually |
| Permission denied | DEFINER lacks rights | Recreate with valid definer or `SQL SECURITY INVOKER` (MySQL 8+) |
| Duplicate work across replicas | Event runs on every replica | Run scheduler only on primary; use app job or orchestrator |
| Lost after upgrade | Event in wrong schema | Backup `mysql.event` / dump routines+events |
| Clock skew / DST surprise | `STARTS` / `EVERY` boundary | Use UTC (`SET time_zone = '+00:00'`) for critical jobs |

## Gotchas

> [!WARNING]
> **No built-in retry or alerting** — silent failure unless you log inside the body or monitor `performance_schema.events_errors`.

> [!WARNING]
> **Replication** — events execute locally on each server unless you restrict; cleanup on replica may be wrong or double-run in failover scenarios.

> [!WARNING]
> **Long-running DO blocks** — blocks event thread; can pile up schedules. Keep jobs idempotent and fast; batch deletes with `LIMIT`.

> [!WARNING]
> **Typo in SQL = disabled event** — `WEHRE` fails at create or first run; always `SHOW CREATE EVENT` after deploy.

## When NOT to use

- **Heavy ETL or cross-system orchestration** — use [[Airflow]], cron + app worker, or CDC pipeline.
- **Exactly-once distributed semantics** — events are single-node; use external queue with acks.
- **User-visible scheduling** — no UI; prefer application scheduler with audit trail.

## Related

[[mysql]] [[mysql triggers]] [[mysql function]] [[OLTP]] [[Airflow]]
