[[mysql]] [[ACID]] [[mysql lock]] [[write-ahead logging]] [[database application]]

# mysql transaction

> InnoDB transactions group SQL statements under [[ACID]] rules — autocommit wraps each statement unless `START TRANSACTION` opens an explicit unit of work.





## Interview Relevance
Expect isolation default (REPEATABLE READ), durability knobs, and why distributed XA is rare versus outbox/saga patterns.

## Sources
- [START TRANSACTION / COMMIT](https://dev.mysql.com/doc/refman/en/commit.html) — overview
- [InnoDB Transaction Model](https://dev.mysql.com/doc/refman/en/innodb-transaction-model.html) — deep-dive

## Key Concepts
- **Explicit vs autocommit:** Multi-statement atomicity needs `START TRANSACTION` … `COMMIT`.
- **Isolation:** InnoDB default **REPEATABLE READ** with next-key locking ([[mysql lock]]).
- **Durability:** `innodb_flush_log_at_trx_commit=1` waits for redo flush ([[write-ahead logging]]).
- **Distributed:** XA exists; microservices usually prefer outbox/saga ([[database application]]).

## Technical Details
```sql
START TRANSACTION;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
-- ROLLBACK; on error
```

Keep transactions short; do not hold locks across remote calls.

## Real-World Applications
Money movement, inventory reservation, and any multi-row invariant that must not partially apply.

## Pros/Cons or Trade-offs
- **Pro:** Correctness under concurrency and crash recovery.
- **Con:** Long transactions amplify lock contention and undo pressure.
- **Trade-off:** Full durability (`=1`) vs batched fsync (`=2`) for non-critical data.

## Comparison
vs PostgreSQL: default isolation is READ COMMITTED there; do not assume identical anomaly behavior.

## Mistakes to Avoid
- Relying on autocommit for multi-step business operations.
- Catching errors without `ROLLBACK` and continuing on a doomed session.
- Using XA as the default microservice coordination tool.
