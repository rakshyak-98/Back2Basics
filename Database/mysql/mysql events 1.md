```mysql
SHOW EVENTS;                           -- list events
SHOW CREATE EVENT my_event\G;          -- view definition
ALTER EVENT my_event DISABLE;          -- disable
ALTER EVENT my_event ENABLE;           -- enable
DROP EVENT my_event;                   -- delete

```

> [!NOTE]
> if server restarts, `event_scheduler` must be re-enabled unless set in `my.cnf`.

- lightweight cron inside the DB.

```sql
SET GLOBAL event_scheduler = ON;
```

```sql
SHOW VARIABLEs LIKE 'event_scheduler';
```

```sql
CREATE EVENT my_event
ON SCHEDULE EVERY 1 DAY
STARTS CURRENT_TIMESTAMP
DO
	INSERT INTO logs(message, created_at)
	VALUES ('Daily log entry', NOW());
```

### Run once at a specific time
```sql
CREATE EVENT cleanup_old_data
ON SCHEDULE AT TIMESTAMP '2025-08-21 00:00:00'
DO
  DELETE FROM sessions WHERE created_at < NOW() - INTERVAL 30 DAY;
```

### Repeat every hour
```sql
CREATE EVENT hourly_stats
ON SCHEDULE EVERY 1 HOUR
DO
  CALL update_stats();
```

### Persist the mysql events scheduler
`/etc/mysql/my.cnf`  `/etc/my.cnf`

```ini
[mysqld]
event_scheduler=ON
```

```bash
sudo systemctl restart mysql;
```