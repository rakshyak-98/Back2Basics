[[Database]] [[WAL (Write-Ahead Log)]] [[MVCC]] [[mysql transaction]] [[SQL/postgres]] [[OLTP]] [[BASE]]

# ACID

> Four independent guarantees—atomicity, consistency, isolation, durability—that let applications treat multi-step writes as one unit and trust committed data after a crash.

## The four properties are separate knobs

| Property | Question it answers | Typical mechanism |
|----------|---------------------|-------------------|
| **Atomicity** | If we crash mid-transaction, is work half-applied? | Undo log + rollback; incomplete transactions discarded on recovery |
| **Consistency** | Can invalid states appear? | `NOT NULL`, `CHECK`, foreign keys, triggers — only *declared* rules |
| **Isolation** | Do concurrent transactions see each other's partial work? | Locks, [[MVCC]], isolation levels |
| **Durability** | Does committed data survive power loss? | [[WAL (Write-Ahead Log)]] flushed before acknowledging commit |

**Consistency is not magic.** The database enforces schema constraints you declare. Business invariants such as "account balance never negative" still need application logic or database triggers unless modeled as constraints.

## Isolation levels and anomalies

The SQL standard defines isolation levels that trade concurrency for anomaly freedom. PostgreSQL implements three distinct behaviors (READ UNCOMMITTED is treated as READ COMMITTED). MySQL InnoDB defaults to **REPEATABLE READ** with next-key locking.

| Anomaly | What goes wrong |
|---------|-----------------|
| Dirty read | See uncommitted data from another transaction |
| Non-repeatable read | Same row reads differently within one transaction |
| Phantom read | New rows appear in a repeated range query |
| Serialization anomaly | Concurrent txs produce an outcome no serial order could |

```sql
-- PostgreSQL: stricter isolation when needed
BEGIN;
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
-- ... work ...
COMMIT;  -- may fail with serialization_error; application must retry
```

*What breaks first on READ COMMITTED?* A read-modify-write spread across three autocommit statements — classic inventory oversell.

## Engine defaults matter

| Engine | Default isolation | Durability knob |
|--------|-------------------|-----------------|
| PostgreSQL | READ COMMITTED | `synchronous_commit` |
| MySQL InnoDB | REPEATABLE READ | `innodb_flush_log_at_trx_commit=1` |

## Preventing lost updates

Pick one strategy and use it consistently:

```sql
-- Optimistic: version column
UPDATE accounts SET balance = balance - 100, version = version + 1
WHERE id = 1 AND version = :expected;

-- Pessimistic: row lock
SELECT balance FROM accounts WHERE id = 1 FOR UPDATE;
```

## Sources

- ISO/IEC 9075 (SQL standard) — transaction isolation definitions
- PostgreSQL Documentation — [13.2 Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html)
- MySQL Reference Manual — [15.2 InnoDB and the ACID Model](https://dev.mysql.com/doc/refman/en/mysql-acid.html)
- Kleppmann, *DDIA*, Ch. 7
