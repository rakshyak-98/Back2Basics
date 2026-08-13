[[mysql query]] [[mysql]] [[variables]]

# show query

> MySQL statements to inspect live and historical queries—`SHOW PROCESSLIST`, Performance Schema, and slow query log—for finding what blocks production.

## Live sessions

```sql
SHOW FULL PROCESSLIST;
-- or
SELECT * FROM information_schema.processlist WHERE command != 'Sleep';
```

## Kill runaway query

```sql
KILL QUERY 12345;
```

## Performance Schema (MySQL 8+)

```sql
SELECT sql_text, timer_wait/1e12 AS sec
FROM performance_schema.events_statements_history_long
ORDER BY timer_wait DESC LIMIT 10;
```

Enable **slow query log** with `long_query_time` for offline analysis.

## Sources

- MySQL Reference Manual — [SHOW PROCESSLIST](https://dev.mysql.com/doc/refman/en/show-processlist.html)
- MySQL Reference Manual — [The Slow Query Log](https://dev.mysql.com/doc/refman/en/slow-query-log.html)
