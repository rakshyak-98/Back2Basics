[[Database]] [[WAL (Write-Ahead Log)]] [[MVCC]] [[mysql transaction]] [[SQL/postgres]] [[OLTP]] [[BASE]] [[ARIES]]

# ACID

> Four independent guarantees—atomicity, consistency, isolation, durability—that let applications treat multi-step writes as one unit and trust committed data after a crash.





## Interview Relevance
Interviewers use ACID to test whether you can separate the four properties, name isolation anomalies, and pick locking vs optimistic strategies for lost updates. Expect follow-ups on engine defaults (PostgreSQL READ COMMITTED vs InnoDB REPEATABLE READ) and what “consistency” does and does not enforce.

## Sources
- [ISO/IEC 9075 — SQL standard (transaction isolation)](https://www.iso.org/standard/76583.html) — deep-dive
- [PostgreSQL Documentation — 13.2 Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html) — deep-dive
- [MySQL Reference Manual — InnoDB and the ACID Model](https://dev.mysql.com/doc/refman/en/mysql-acid.html) — overview
- Kleppmann, *Designing Data-Intensive Applications*, Ch. 7 — deep-dive

## Core Definition
ACID describes transaction semantics: all-or-nothing apply, declared invariants held at commit, concurrent sessions do not see illegal intermediate states per the chosen isolation level, and committed changes survive crashes via durable logging.

## Key Concepts
- **Atomicity:** crash mid-transaction must not leave half-applied work → undo/rollback; incomplete transactions discarded on recovery.
- **Consistency:** only *declared* rules (`NOT NULL`, `CHECK`, foreign keys, triggers) → business invariants still need app logic or modeled constraints.
- **Isolation:** concurrent transactions should not see each other’s partial work → locks, [[MVCC]], isolation levels.
- **Durability:** committed data survives power loss → [[WAL (Write-Ahead Log)]] flushed before acknowledging commit.

## Technical Details
The four properties are separate knobs:

| Property | Question it answers | Typical mechanism |
|----------|---------------------|-------------------|
| **Atomicity** | If we crash mid-transaction, is work half-applied? | Undo log + rollback |
| **Consistency** | Can invalid states appear? | Schema constraints you declare |
| **Isolation** | Do concurrent txs see partial work? | Locks, [[MVCC]], isolation levels |
| **Durability** | Does commit survive power loss? | WAL flush before ack |

SQL isolation levels trade concurrency for anomaly freedom:

| Anomaly | What goes wrong |
|---------|-----------------|
| Dirty read | See uncommitted data from another transaction |
| Non-repeatable read | Same row reads differently within one transaction |
| Phantom read | New rows appear in a repeated range query |
| Serialization anomaly | Concurrent txs produce an outcome no serial order could |

PostgreSQL implements three distinct behaviors (READ UNCOMMITTED is treated as READ COMMITTED). MySQL InnoDB defaults to **REPEATABLE READ** with next-key locking.

```sql
-- PostgreSQL: stricter isolation when needed
BEGIN;
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
-- ... work ...
COMMIT;  -- may fail with serialization_error; application must retry
```

*What breaks first on READ COMMITTED?* A read-modify-write spread across three autocommit statements — classic inventory oversell.

| Engine | Default isolation | Durability knob |
|--------|-------------------|-----------------|
| PostgreSQL | READ COMMITTED | `synchronous_commit` |
| MySQL InnoDB | REPEATABLE READ | `innodb_flush_log_at_trx_commit=1` |

Preventing lost updates — pick one strategy and use it consistently:

```sql
-- Optimistic: version column
UPDATE accounts SET balance = balance - 100, version = version + 1
WHERE id = 1 AND version = :expected;

-- Pessimistic: row lock
SELECT balance FROM accounts WHERE id = 1 FOR UPDATE;
```

## Real-World Applications
[[OLTP]] ledgers, inventory deduction, and payment capture. Example: transfer funds with debit+credit in one transaction so a crash cannot leave money in limbo; retry on serialization failure under SERIALIZABLE.

## Pros/Cons or Trade-offs
- **Pro:** Applications reason about multi-step writes as one unit; durability + isolation prevent silent corruption after crashes and races.
- **Con:** Stronger isolation reduces concurrency and can force retries; durability settings that skip sync improve throughput but risk committed-but-lost data after power loss.

## Comparison
vs [[BASE]]: ACID prioritizes correctness on a single authoritative store; BASE accepts temporary inconsistency for availability across partitions. vs [[ARIES]]: ACID names the guarantees; ARIES is a concrete WAL recovery algorithm that helps deliver durability and atomicity.

## Mistakes to Avoid
- Treating “consistency” as magic business-rule enforcement — the database only enforces what you declare.
- Spreading read-modify-write across autocommit statements under READ COMMITTED — lost updates and oversell.
- Ignoring engine defaults — assuming MySQL and PostgreSQL share the same isolation behavior.
- Setting `innodb_flush_log_at_trx_commit=0` or `synchronous_commit=off` without understanding durability loss on crash.
