[[mysql Programmable SQL]] [[MySQL Triggers]] [[mysql]] [[MySQL CLI]]

# MySQL Events

> The MySQL Event Scheduler runs SQL jobs inside the server on a cron-like schedule — `CREATE EVENT` defines recurring or one-shot tasks without external cron infrastructure.

---

## Why It Matters

Event Scheduler moves simple housekeeping into the database: purging expired sessions, rotating partitions, refreshing summary tables. It runs with database privileges, close to the data, with no extra infrastructure. The trade-off is observability — a disabled scheduler after restore causes silent no-ops, and long-running event bodies can lock tables and cause replication lag. For complex workflows with retries, alerting, and dependency chains, external schedulers (Kubernetes CronJob, Airflow) are safer.

---

## Sources

- [MySQL Reference Manual — Event Scheduler](https://dev.mysql.com/doc/refman/en/event-scheduler.html) — Enabling the scheduler, privilege requirements, and interaction with replication.
- [MySQL Reference Manual — CREATE EVENT](https://dev.mysql.com/doc/refman/en/create-event.html) — `EVERY`, `STARTS`, `ENDS`, `ON COMPLETION`, and `ENABLE`/`DISABLE` syntax.
- [MySQL Reference Manual — Events in information_schema](https://dev.mysql.com/doc/refman/en/events-table.html) — Querying `information_schema.EVENTS` for auditing scheduled jobs.

---

## Key Concepts

| Concept | Detail |
|---------|--------|
| **In-server cron** | Jobs execute inside `mysqld` — no OS crontab needed. |
| **Must be enabled** | `event_scheduler = ON` globally — OFF by default on some installs. |
| **Recurring** | `ON SCHEDULE EVERY 1 DAY` — cron-like interval. |
| **One-shot** | `ON SCHEDULE AT '2026-12-31 23:59:00'` — runs once. |
| **Definer** | Runs with creator's privileges — security-sensitive on shared hosts. |
| **Replication** | Events replicate to replicas — ensure idempotent logic. |

```txt
event_scheduler = ON
        │
        ▼
Event thread wakes on schedule
        │
        ▼
Execute DO clause (SQL body)
        │
        ▼
Log to performance_schema / error log on failure
```

---

## Technical Details

### Enable the scheduler

```sql
SET GLOBAL event_scheduler = ON;
-- Persist in my.cnf:
-- event_scheduler = ON

SHOW VARIABLES LIKE 'event_scheduler';
```

### Daily purge event

```sql
CREATE EVENT purge_sessions
ON SCHEDULE EVERY 1 DAY
STARTS CURRENT_TIMESTAMP
ON COMPLETION PRESERVE
ENABLE
COMMENT 'Remove expired sessions nightly'
DO
  DELETE FROM sessions WHERE expires_at < NOW() LIMIT 10000;
```

Use `LIMIT` on large DELETEs to avoid long locks — batch across multiple event runs if needed.

### One-shot maintenance

```sql
CREATE EVENT rebuild_stats_once
ON SCHEDULE AT '2026-08-18 02:00:00'
DO
  ANALYZE TABLE orders, order_items;
```

### Inspect events

```sql
SHOW EVENTS;
SHOW CREATE EVENT purge_sessions;

SELECT EVENT_NAME, STATUS, LAST_EXECUTED, STARTS, INTERVAL_VALUE, INTERVAL_FIELD
FROM information_schema.EVENTS
WHERE EVENT_SCHEMA = 'myapp';
```

### Partition maintenance helper

```sql
CREATE EVENT add_monthly_partition
ON SCHEDULE EVERY 1 MONTH
STARTS '2026-09-01 00:00:00'
DO
  CALL add_next_events_partition();  -- stored procedure
```

---

## Mistakes to Avoid

- Creating events while `event_scheduler` is OFF — they exist in metadata but never run.
- Long-running DELETE without batching — lock storms and replication lag.
- Relying on events for business-critical workflows without monitoring `LAST_EXECUTED`.
- Forgetting events after database restore — scheduler state may reset to OFF.
- Non-idempotent event bodies on replicas — double execution after failover.

---

## Pros/Cons or Trade-offs

| Pro | Con |
|-----|-----|
| No extra infrastructure for simple SQL jobs | Limited metrics and alerting vs external runners |
| Runs close to the data | Easy to miss when scheduler is OFF |
| Atomic with other DDL in migrations | Competes with OLTP for connection and lock resources |

---

## Comparison

| vs | Distinction |
|----|-------------|
| [[MySQL Triggers]] | Triggers react to row changes; events run on a schedule |
| OS cron / Kubernetes CronJob | External — better observability, retries, and alerting |
| [[MySQL Events]] vs Airflow | Airflow for DAGs; events for single-statement housekeeping |

---

## Use cases

- Nightly `DELETE FROM sessions WHERE expires_at < NOW()` with batched `LIMIT`.
- Monthly `ALTER TABLE … ADD PARTITION` via stored procedure.
- Weekly `ANALYZE TABLE` on tables with heavy churn.
