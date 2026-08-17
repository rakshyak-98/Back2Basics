[[Database]] [[WAL (Write-Ahead Log)]] [[MVCC]] [[mysql transaction]] [[SQL/postgres]] [[OLTP]] [[BASE]] [[ARIES]]

# ACID

> Four independent guarantees—atomicity, consistency, isolation, durability—that let applications treat multi-step writes as one unit and trust committed data after a crash.

```txt
        ACID ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers use ACID to test whether you can separate the four properties, n…

## Sources
- [ISO/IEC 9075 — SQL standard (transaction isolation)](https://www.iso.org/standard/76583.html) — deep-dive
- [PostgreSQL Documentation — 13.2 Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html) — deep-dive
- [MySQL Reference Manual — InnoDB and the ACID Model](https://dev.mysql.com/doc/refman/en/mysql-acid.html) — overview
- Kleppmann, *Designing Data-Intensive Applications*, Ch. 7 — deep-dive

## Key Concepts
- **Atomicity:** crash mid-transaction must not leave half-applied work → undo/rollback
- **Consistency:** only *declared* rules (`NOT NULL`, `CHECK`, foreign keys, triggers) → busines…
- **Isolation:** concurrent transactions should not see each other’s partial work → locks, [[M…
- **Durability:** committed data survives power loss → [[WAL (Write-Ahead Log)]] flushed before…


- **Core:** ACID describes transaction semantics: all-or-nothing apply, declared invarian…

## Technical Details
- The four properties are separate knobs:

| Property | Question it answers | Typical mechanism |
|----------|---------------------|-------------------|
| **Atomicity** | If we crash mid-transaction, is work half-applied? | Undo log + rollback |
| **Consistency** | Can invalid states appear? | Schema constraints you declare |
| **Isolation** | Do concurrent txs see partial work? | Locks, [[MVCC]], isolation levels |
| **Durability** | Does commit survive power loss? | WAL flush before ack |

- SQL isolation levels trade concurrency for anomaly freedom:

| Anomaly | What goes wrong |
|---------|-----------------|
| Dirty read | See uncommitted data from another transaction |
| Non-repeatable read | Same row reads differently within one transaction |
| Phantom read | New rows appear in a repeated range query |
| Serialization anomaly | Concurrent txs produce an outcome no serial order could |

- PostgreSQL implements three distinct behaviors (READ UNCOMMITTED is treated a…
- MySQL InnoDB defaults to **REPEATABLE READ** with next-key locking.

```sql
-- PostgreSQL: stricter isolation when needed
BEGIN;
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
-- ... work ...
COMMIT;  -- may fail with serialization_error; application must retry
```

- *What breaks first on READ COMMITTED?* A read-modify-write spread across thre…

| Engine | Default isolation | Durability knob |
|--------|-------------------|-----------------|
| PostgreSQL | READ COMMITTED | `synchronous_commit` |
| MySQL InnoDB | REPEATABLE READ | `innodb_flush_log_at_trx_commit=1` |

- Preventing lost updates — pick one strategy and use it consistently:

```sql
-- Optimistic: version column
UPDATE accounts SET balance = balance - 100, version = version + 1
WHERE id = 1 AND version = :expected;

-- Pessimistic: row lock
SELECT balance FROM accounts WHERE id = 1 FOR UPDATE;
```

## Mistakes to Avoid
- **Mistake:** Treating “consistency” as magic business-rule enforcement
- **Mistake:** Spreading read-modify-write across autocommit statements under R…
- **Mistake:** Ignoring engine defaults
- **Mistake:** Setting `innodb_flush_log_at_trx_commit=0` or `synchronous_commi…

## Pros/Cons or Trade-offs
- **Pro:** Applications reason about multi-step writes as one unit; durability + isolation prevent silent corruption after crashes and races.
- **Con:** Stronger isolation reduces concurrency and can force retries; durability settings that skip sync improve throughput but risk committed-but-lost data after power loss.

## Comparison
- vs [[BASE]]: ACID prioritizes correctness on a single authoritative store


### Use cases
- [[OLTP]] ledgers, inventory deduction, and payment capture. Example: transfer…
