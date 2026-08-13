[[mysql transaction]] [[ACID]] [[mysql query]]

# mysql lock

> InnoDB row-level locks, gap locks, and next-key locks that implement isolation—deadlocks are normal and one transaction is rolled back.

## Lock types

| Lock | Scenario |
|------|----------|
| Record lock | Exact row match |
| Gap lock | Blocks inserts in index gap (RR isolation) |
| Next-key | Record + gap |
| Intention locks | Table-level intent for row locks |

## Explicit locking

```sql
SELECT * FROM accounts WHERE id = 1 FOR UPDATE;
SELECT * FROM accounts WHERE id = 1 LOCK IN SHARE MODE;  -- FOR SHARE in 8.0
```

## Deadlocks

```sql
SHOW ENGINE INNODB STATUS\G
-- LATEST DETECTED DEADLOCK section
```

Application should retry deadlocked transactions.

## Sources

- MySQL Reference Manual — [InnoDB Locking](https://dev.mysql.com/doc/refman/en/innodb-locking.html)
- MySQL Reference Manual — [Deadlocks](https://dev.mysql.com/doc/refman/en/innodb-deadlocks.html)
