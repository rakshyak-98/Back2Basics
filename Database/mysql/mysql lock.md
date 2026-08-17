[[mysql transaction]] [[ACID]] [[mysql query]] [[MySQL Error]]

# mysql lock

> InnoDB row-level locks, gap locks, and next-key locks that implement isolation—deadlocks are normal and one transaction is rolled back.





## Interview Relevance
Locking interviews cover record/gap/next-key locks under REPEATABLE READ, `FOR UPDATE`, and deadlock retry. Expect to read `SHOW ENGINE INNODB STATUS` deadlock section conceptually.

## Sources
- [MySQL Reference Manual — InnoDB Locking](https://dev.mysql.com/doc/refman/en/innodb-locking.html) — deep-dive
- [MySQL Reference Manual — Deadlocks](https://dev.mysql.com/doc/refman/en/innodb-deadlocks.html) — deep-dive

## Key Concepts
- **Record / gap / next-key:** exact row, index gap, and combination (RR default).
- **Intention locks:** table-level intent coordinating with row locks.
- **Explicit locking:** `FOR UPDATE` / `FOR SHARE` (8.0) for read-modify-write.
- **Deadlocks:** normal; one tx rolls back (error 1213) — application retries.

## Technical Details
| Lock | Scenario |
|------|----------|
| Record lock | Exact row match |
| Gap lock | Blocks inserts in index gap (RR isolation) |
| Next-key | Record + gap |
| Intention locks | Table-level intent for row locks |

```sql
SELECT * FROM accounts WHERE id = 1 FOR UPDATE;
SELECT * FROM accounts WHERE id = 1 LOCK IN SHARE MODE;  -- FOR SHARE in 8.0
```

```sql
SHOW ENGINE INNODB STATUS\G
-- LATEST DETECTED DEADLOCK section
```

Application should retry deadlocked transactions ([[MySQL Error]] 1213).

## Real-World Applications
Inventory decrement and seat booking under concurrency. Example: `SELECT … FOR UPDATE` then update quantity; on deadlock, retry the whole transaction rather than surfacing 1213 to the user as a hard failure.

## Pros/Cons or Trade-offs
- **Pro:** Row-level locking allows high concurrency vs table locks; gap locks prevent phantoms under RR.
- **Con:** Gap locks increase contention on hot index ranges; long transactions amplify deadlocks and wait timeouts (1205).

## Comparison
vs [[ACID]] isolation levels: locks (and MVCC) are mechanisms that implement isolation. vs [[mysql transaction]]: transactions define boundaries; locks are what InnoDB takes inside those boundaries.

## Mistakes to Avoid
- Treating deadlocks as server bugs instead of expected concurrency outcomes.
- Holding locks across user think-time or external HTTP calls.
- Scanning huge ranges under RR without indexes — gap lock storms.
