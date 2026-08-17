[[Database]] [[connection pooling]] [[Data access patterns]] [[SQL]] [[ACID]] [[mysql]]

# database application

> The application layer that issues queries—ORMs, repositories, transaction boundaries, and retry logic that turn business operations into [[ACID]]-safe database work.





## Interview Relevance
Interviewers probe where transactions begin/end, how you retry serialization failures, and how the app owns workflows the database cannot express. Signal: clear service-layer boundaries, idempotency, and timeouts—not “the ORM handles it.”

## Sources
- Kleppmann, *Designing Data-Intensive Applications*, Ch. 7–9 — deep-dive
- [PostgreSQL Documentation — Error Codes](https://www.postgresql.org/docs/current/errcodes-appendix.html) — overview

## Key Concepts
- **Responsibility split:** database enforces constraints; application enforces workflows (state machines, idempotency keys).
- **Transaction boundary:** multi-step invariants wrap in one transaction at the service layer → not per repository call blindly.
- **Resilience:** retry serialization failures, circuit-break unhealthy DB, timeouts, idempotency keys on payment-like ops.

## Technical Details
```txt
Controller ──► Service (transaction boundary) ──► Repository/ORM ──► [[SQL]]
```

Wrap multi-step invariants in one transaction:

```python
with db.begin():
    debit(account_a, amount)
    credit(account_b, amount)
```

Resilience patterns:

- **Retry** serialization failures (`40001` in PostgreSQL)
- **Circuit breaker** when database is unhealthy
- **Timeouts** on statements and connections
- **Idempotency keys** on payment-like operations

## Real-World Applications
Checkout services that debit inventory and create an order atomically, then publish an outbox event. Example: on `serialization_failure`, the app retries the whole unit of work with the same idempotency key so double-submit does not double-charge.

## Pros/Cons or Trade-offs
- **Pro:** Business invariants stay explicit; retries and timeouts make transient DB failures survivable.
- **Con:** Fat transactions hold locks longer; ORMs can hide N+1 and accidental autocommit if boundaries are unclear.

## Comparison
vs raw [[SQL]] scripts: the application owns session lifecycle, pooling ([[connection pooling]]), and user-facing retries. vs the database alone: constraints catch invalid rows; workflows and idempotency live in app code.

## Mistakes to Avoid
- Opening a transaction in the controller and holding it across HTTP calls to other services.
- Ignoring serialization / deadlock errors instead of retrying the transaction.
- Assuming ORM `save()` is upsert — may INSERT duplicates.
- No statement timeout — one slow query pins the pool and stalls the app.
