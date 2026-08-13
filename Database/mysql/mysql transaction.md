<!-- note-strategy: operational -->
[[mysql]] [[ACID]] [[mysql lock]] [[write-ahead logging]]

# mysql transaction

> A transaction bundles multiple writes so they all commit or all roll back — one unit of work for correctness.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** `START TRANSACTION` → do related writes → `COMMIT` (durable) or `ROLLBACK` (undo); isolation + locks decide what others see meanwhile.

```txt
BEGIN
  write A
  write B   ── if B fails → ROLLBACK (A undone)
COMMIT      ── both durable (InnoDB redo)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Atomicity** | All or nothing | “Two updates succeed together or neither does.” |
| **Isolation** | How much you see of others | “We pick a level; default REPEATABLE READ on InnoDB.” |
| **COMMIT** | Make changes durable | “After commit, crash recovery still has them.” |
| **ROLLBACK** | Discard uncommitted work | “Error path always rolls back the connection’s txn.” |
| **Autocommit** | Each statement is its own txn | “Multi-step logic needs an explicit transaction.” |
| **Long transaction** | Open too long | “Holds locks + undo; starves others.” |

### When you need one

Use a transaction when **multiple writes must succeed or fail together**. Single-statement DML is already atomic under InnoDB autocommit.

---

## Standard config / commands

```sql
START TRANSACTION;   -- or BEGIN
UPDATE ...;
INSERT ...;
COMMIT;              -- or ROLLBACK;
```

```sql
SELECT @@autocommit, @@transaction_isolation;
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
```

Node-style (one borrowed pool connection):

```js
const conn = await pool.getConnection()
try {
  await conn.beginTransaction()
  await conn.execute('UPDATE ...')
  await conn.execute('INSERT ...')
  await conn.commit()
} catch (e) {
  await conn.rollback()
  throw e
} finally {
  conn.release()
}
```

| Knob | Why it matters |
|------|----------------|
| Isolation level | RR vs RC changes phantoms / gap locks |
| Autocommit OFF | Easy to leave uncommitted work |
| Same connection | Session txn state is per connection |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Partial update visible | Autocommit / missing BEGIN | Wrap related writes in one txn |
| Locks pile up | Long open txn in `PROCESSLIST` | Commit sooner; don’t wait on network inside txn |
| Deadlock | InnoDB status | Retry; consistent ordering |
| “Forgot to commit” | Session still in txn | `COMMIT`/`ROLLBACK`; fix app paths |
| Rollback didn’t undo DDL | MySQL DDL often implicit commit | Don’t mix DDL mid-txn expecting undo |

---

## Gotchas

> [!WARNING]
> **DDL often commits implicitly** — `ALTER`/`CREATE` can end your transaction without an explicit `COMMIT`.

> [!WARNING]
> **Pool + txn** — never return a connection to the pool before commit/rollback.

> [!WARNING]
> **Read-only multi-statement “consistency”** — still may need a txn (or snapshot isolation) if you need a stable view across queries.

---

## When NOT to use

- **Single independent INSERT/UPDATE** — autocommit is enough.
- **Wrapping a long report / ETL in one txn** — huge undo + lock risk; batch with smaller units.
- **Holding a txn open across user confirmation UI** — lock duration becomes user latency.

---

## Related

[[ACID]] [[mysql lock]] [[mysql]] [[mysql connection]] [[write-ahead logging]] [[OLTP]]
