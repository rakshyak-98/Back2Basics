[[MySQL Events]] [[mysql Programmable SQL]]

# mysql events 1

> Supplemental examples for MySQL scheduled events—one-shot events, conditional execution, and privilege requirements alongside [[MySQL Events]].

```txt
        mysql events 1 ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Follow-up to event scheduler: one-time `AT` schedules, `EVENT` privilege, and…

## Sources
- [MySQL Reference Manual — CREATE EVENT](https://dev.mysql.com/doc/refman/en/create-event.html) — deep-dive

## Key Concepts
- **One-shot events:** `ON SCHEDULE AT` for a single run.
- **EVENT privilege:** required to create/manage events.
- **DEFINER security:** event runs as definer — review for privilege escalation.

## Technical Details
```sql
CREATE EVENT archive_2024_q1
ON SCHEDULE AT '2025-01-01 00:00:00'
DO
  INSERT INTO archive.orders SELECT * FROM orders WHERE created_at < '2024-04-01';
```

- Permissions:

```sql
GRANT EVENT ON mydb.* TO 'scheduler'@'%';
```

- `DEFINER` clause runs event as another user—review for privilege escalation.

## Mistakes to Avoid
- **Mistake:** Granting EVENT broadly to application users who only need DML
- **Mistake:** Using powerful DEFINER accounts for trivial housekeeping
- **Mistake:** Forgetting the scheduler must be ON ([[MySQL Events]]) or the ev…

## Pros/Cons or Trade-offs
- **Pro:** Keeps simple timed SQL next to the data without an external scheduler.
- **Con:** Weaker observability than Kubernetes CronJobs; DEFINER mistakes widen privilege blast radius.

## Comparison
- vs [[MySQL Events]]: primary note for enabling/monitoring the scheduler


### Use cases
- Scheduled one-time archival at year boundaries
