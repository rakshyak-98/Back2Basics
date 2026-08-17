[[mysql query]] [[mysql]] [[variables]] [[mysql lock]]

# show query

> Inspect live and historical MySQL queries — `SHOW PROCESSLIST`, Performance Schema, and the slow query log — to find what blocks production.

```txt
        show query ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** On-call / debugging signal: how do you find the culprit query, kill it safely…

## Sources
- [SHOW PROCESSLIST](https://dev.mysql.com/doc/refman/en/show-processlist.html) — overview
- [Slow Query Log](https://dev.mysql.com/doc/refman/en/slow-query-log.html) — deep-dive
- [Performance Schema](https://dev.mysql.com/doc/refman/en/performance-schema.html) — deep-dive

## Key Concepts
- **Processlist:** What is running now (command, time, state, SQL).
- **KILL QUERY / KILL:** Cancel a statement or full connection.
- **Slow query log:** Thresholded historical offenders (`long_query_time`).
- **Performance Schema:** Statement history and wait instrumentation (MySQL 8+).

## Technical Details
```sql
SHOW FULL PROCESSLIST;
SELECT * FROM information_schema.processlist WHERE command != 'Sleep';

KILL QUERY 12345;

SELECT sql_text, timer_wait/1e12 AS sec
FROM performance_schema.events_statements_history_long
ORDER BY timer_wait DESC LIMIT 10;
```

- Pair findings with `EXPLAIN` on [[mysql query]].

## Mistakes to Avoid
- **Mistake:** `KILL` on the wrong thread ID
- **Mistake:** Enabling slow log with `long_query_time=0` on a hot primary with…
- **Mistake:** Fixating on CPU while the processlist shows lock waits ([[mysql …

## Pros/Cons or Trade-offs
- **Pro:** Immediate visibility without deploying new agents.
- **Con:** Processlist is a point-in-time sample; short queries may never appear.
- **Trade-off:** Always-on Performance Schema overhead vs blind spots.

## Comparison
- vs external APM: DB-native tools are authoritative for SQL text/locks


### Use cases
- Incident response when API latency spikes: find long `Locked`/`Sending data` …
