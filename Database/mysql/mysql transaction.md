[[mysql]] [[ACID]] [[mysql lock]] [[write-ahead logging]]

# mysql transaction

> InnoDB transactions group SQL statements with [[ACID]] guarantees—default autocommit wraps each statement unless `START TRANSACTION` opens an explicit unit of work.

## Basic usage

```sql
START TRANSACTION;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
-- ROLLBACK; on error
```

## Isolation default

InnoDB default **REPEATABLE READ** with next-key locking prevents phantoms in many cases (gap locks).

## Durability

Commit waits for redo log flush when `innodb_flush_log_at_trx_commit=1`.

## Distributed transactions

XA transactions exist but microservices rarely use them—prefer outbox/saga patterns ([[database application]]).

## Sources

- MySQL Reference Manual — [START TRANSACTION](https://dev.mysql.com/doc/refman/en/commit.html)
- MySQL Reference Manual — [InnoDB Transaction Model](https://dev.mysql.com/doc/refman/en/innodb-transaction-model.html)
