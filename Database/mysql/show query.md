[[mysql query]] [[mysql]] [[variables]] [[mysql lock]]

# show query

> Inspect live and historical MySQL queries — `SHOW PROCESSLIST`, Performance Schema, and the slow query log — to find what blocks production.

## Interview Relevance
On-call / debugging signal: how do you find the culprit query, kill it safely, and prevent repeats with the slow log.

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

Pair findings with `EXPLAIN` on [[mysql query]].

## Real-World Applications
Incident response when API latency spikes: find long `Locked`/`Sending data` threads, kill runaways, then add indexes or limit fan-out.

## Pros/Cons or Trade-offs
- **Pro:** Immediate visibility without deploying new agents.
- **Con:** Processlist is a point-in-time sample; short queries may never appear.
- **Trade-off:** Always-on Performance Schema overhead vs blind spots.

## Comparison
vs external APM: DB-native tools are authoritative for SQL text/locks; APM shows user-facing impact.

## Mistakes to Avoid
- `KILL` on the wrong thread ID.
- Enabling slow log with `long_query_time=0` on a hot primary without disk plan.
- Fixating on CPU while the processlist shows lock waits ([[mysql lock]]).
