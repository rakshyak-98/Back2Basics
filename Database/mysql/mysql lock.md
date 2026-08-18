[[mysql]] [[mysql transaction]] [[ACID]] [[mysql engine]]

# mysql lock

> Locks stop two sessions from stepping on the same data — prefer row locks in transactions; table locks are a blunt tool.

## Mental model

**Say it in one breath:** InnoDB grabs row locks as you read `FOR UPDATE` / write; `LOCK TABLES` freezes whole tables outside that finer model.

```txt
Session A                         Session B
  BEGIN                             BEGIN
  SELECT ... FOR UPDATE  ──wait──►  same rows
  UPDATE / COMMIT                   proceeds
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **Row lock** | Lock matching rows (InnoDB) | “We lock only inventory rows we intend to change.” |
| --- | --- | --- |
| **FOR UPDATE** | Exclusive row lock on read | “Read-modify-write without lost updates.” |
| **FOR SHARE** | Shared lock; blocks writers | “Readers can share; writers wait.” |
| **LOCK TABLES READ** | Table shared; no writers (incl. you) | “Consistent snapshot of whole tables — rare now.” |
| **LOCK TABLES WRITE** | Exclusive table | “Blocks everyone else — last resort.” |
| **Deadlock** | Cycle of waits | “InnoDB aborts one txn; retry the loser.” |

### Table vs row

| Tool | Scope | Typical use |

| InnoDB row locks | Rows (gap/next-key too) | Normal OLTP inside transactions |
| --- | --- | --- |
| `LOCK TABLES` | Whole table(s) | Legacy / MyISAM-era; avoid on InnoDB apps |

## Standard config / commands

```sql
START TRANSACTION;

SELECT * FROM inventory
WHERE room_type_id = 101 AND date = '2026-04-25'
FOR UPDATE;          -- exclusive

UPDATE inventory SET available = available - 1
WHERE room_type_id = 101 AND date = '2026-04-25';

COMMIT;
```

```sql
START TRANSACTION;
SELECT * FROM inventory WHERE room_type_id = 101 FOR SHARE;  -- shared
COMMIT;
```

```sql
LOCK TABLES t READ;    -- or WRITE
-- ... work ...
UNLOCK TABLES;
```

| Knob | Why it matters |

| Index on lock predicate | Without index, InnoDB may lock many more rows / gaps |
| --- | --- |
| Short transactions | Long `FOR UPDATE` holds block others |
| `innodb_lock_wait_timeout` | How long waiters block before error |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Query waits forever | `SHOW ENGINE INNODB STATUS\G` / `performance_schema` | Kill blocker; shorten txn; add index |
| Deadlock error | InnoDB status deadlock section | Retry; consistent lock order |
| Whole app stalls | `LOCK TABLES` held | Unlock; migrate to row locks |
| Lost updates without error | No `FOR UPDATE` on RMW | Wrap read+write in txn with `FOR UPDATE` |
| Lock wait timeout | `SHOW PROCESSLIST` | Reduce contention; fix hot rows |

## Gotchas

> [!WARNING]
> **No useful index on WHERE** — InnoDB may lock a wide range (next-key/gap), not “just one row.”

> [!WARNING]
> **`LOCK TABLES` commits the current transaction** — don’t mix casually with InnoDB txns.

> [!WARNING]
> **Deadlocks are normal under contention** — design for retry, not “never deadlock.”

## When NOT to use

- **`LOCK TABLES` for modern InnoDB OLTP** — use transactions + row locks.
- **Holding locks across user think-time / HTTP round-trips** — lock in DB, decide in application quickly, or use optimistic patterns.
- **Table WRITE locks for “safety” on every write path** — kills concurrency.

## Related

[[mysql transaction]] [[mysql]] [[ACID]] [[mysql engine]] [[mysql index]] [[OLTP]]
