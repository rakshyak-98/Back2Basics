[[mysql Programmable SQL]] [[mysql events 1]] [[mysql]]

# MySQL Events

> MySQL Event Scheduler—cron-like jobs executing SQL inside the server (`CREATE EVENT`) for housekeeping, rollups, and partition maintenance.

```txt
        MySQL Events ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Event scheduler questions cover enabling `event_scheduler`, `CREATE EVENT` sy…

## Sources
- [MySQL Reference Manual — Event Scheduler](https://dev.mysql.com/doc/refman/en/event-scheduler.html) — deep-dive
- [MySQL Reference Manual — CREATE EVENT](https://dev.mysql.com/doc/refman/en/create-event.html) — deep-dive

## Key Concepts
- **In-server cron:** SQL jobs scheduled inside mysqld.
- **Must be enabled:** `event_scheduler = ON`.
- **Recurring or one-shot:** `EVERY` vs `AT` (see [[mysql events 1]]).
- **Observability limit:** prefer external schedulers for complex workflows.

## Technical Details
```sql
SET GLOBAL event_scheduler = ON;
```

```sql
CREATE EVENT purge_sessions
ON SCHEDULE EVERY 1 DAY
STARTS CURRENT_TIMESTAMP
DO
  DELETE FROM sessions WHERE expires_at < NOW();
```

```sql
SHOW EVENTS;
SELECT * FROM information_schema.EVENTS;
```

- Prefer external schedulers (Kubernetes CronJob) for complex workflows needing…

## Mistakes to Avoid
- **Mistake:** Creating events while `event_scheduler` is OFF — silent no-ops
- **Mistake:** Long-running event DELETEs without batching — lock and lag storms
- **Mistake:** Relying on events for business-critical workflows without monito…

## Pros/Cons or Trade-offs
- **Pro:** No extra infrastructure for simple SQL housekeeping; runs close to the data.
- **Con:** Easy to miss when scheduler is OFF after restore; limited metrics/alerting vs external job runners.

## Comparison
- vs [[mysql events 1]]: core scheduler vs supplemental one-shot/privilege exam…


### Use cases
- Daily session purge, partition rotation helpers, simple rollups. Example: `pu…
