[[mysql]] [[ACID]] [[mysql lock]] [[write-ahead logging]] [[database application]]

# mysql transaction

> InnoDB transactions group SQL statements under [[ACID]] rules — autocommit wraps each statement unless `START TRANSACTION` opens an explicit unit of work.

```txt
        mysql transaction ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Expect isolation default (REPEATABLE READ), durability knobs, and why distrib…

## Sources
- [START TRANSACTION / COMMIT](https://dev.mysql.com/doc/refman/en/commit.html) — overview
- [InnoDB Transaction Model](https://dev.mysql.com/doc/refman/en/innodb-transaction-model.html) — deep-dive

## Key Concepts
- **Explicit vs autocommit:** Multi-statement atomicity needs `START TRANSACTION` … `COMMIT`.
- **Isolation:** InnoDB default **REPEATABLE READ** with next-key locking ([[mysql lock]]).
- **Durability:** `innodb_flush_log_at_trx_commit=1` waits for redo flush ([[write-ahead loggin…
- **Distributed:** XA exists; microservices usually prefer outbox/saga ([[database application]]…

## Technical Details
```sql
START TRANSACTION;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
-- ROLLBACK; on error
```

- Keep transactions short; do not hold locks across remote calls.

## Mistakes to Avoid
- **Mistake:** Relying on autocommit for multi-step business operations
- **Mistake:** Catching errors without `ROLLBACK` and continuing on a doomed se…
- **Mistake:** Using XA as the default microservice coordination tool

## Pros/Cons or Trade-offs
- **Pro:** Correctness under concurrency and crash recovery.
- **Con:** Long transactions amplify lock contention and undo pressure.
- **Trade-off:** Full durability (`=1`) vs batched fsync (`=2`) for non-critical data.

## Comparison
- vs PostgreSQL: default isolation is READ COMMITTED there


### Use cases
- Money movement, inventory reservation, and any multi-row invariant that must …
