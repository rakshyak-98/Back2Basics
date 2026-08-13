[[mysql Programmable SQL]] [[mysql events 1]] [[mysql]]

# MySQL Events

> MySQL Event Scheduler—cron-like jobs executing SQL inside the server (`CREATE EVENT`) for housekeeping, rollups, and partition maintenance.

## Enable scheduler

```sql
SET GLOBAL event_scheduler = ON;
```

## Create event

```sql
CREATE EVENT purge_sessions
ON SCHEDULE EVERY 1 DAY
STARTS CURRENT_TIMESTAMP
DO
  DELETE FROM sessions WHERE expires_at < NOW();
```

## Monitoring

```sql
SHOW EVENTS;
SELECT * FROM information_schema.EVENTS;
```

Prefer external schedulers (Kubernetes CronJob) for complex workflows needing observability.

## Sources

- MySQL Reference Manual — [Event Scheduler](https://dev.mysql.com/doc/refman/en/event-scheduler.html)
- MySQL Reference Manual — [CREATE EVENT](https://dev.mysql.com/doc/refman/en/create-event.html)
