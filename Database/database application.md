[[Database]] [[connection pooling]] [[Data access patterns]] [[SQL]] [[ACID]] [[mysql]]

# database application

> The application layer that issues queries—ORMs, repositories, transaction boundaries, and retry logic that turn business operations into [[ACID]]-safe database work.

```txt
        database applicati ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers probe where transactions begin/end, how you retry serialization …

## Sources
- Kleppmann, *Designing Data-Intensive Applications*, Ch. 7–9 — deep-dive
- [PostgreSQL Documentation — Error Codes](https://www.postgresql.org/docs/current/errcodes-appendix.html) — overview

## Key Concepts
- **Responsibility split:** database enforces constraints
- **Transaction boundary:** multi-step invariants wrap in one transaction at the service layer → not per …
- **Resilience:** retry serialization failures, circuit-break unhealthy DB, timeouts, idempoten…

## Technical Details
```txt
Controller ──► Service (transaction boundary) ──► Repository/ORM ──► [[SQL]]
```

- Wrap multi-step invariants in one transaction:

```python
with db.begin():
    debit(account_a, amount)
    credit(account_b, amount)
```

- Resilience patterns:

- **Retry:** serialization failures (`40001` in PostgreSQL)
- **Circuit breaker:** when database is unhealthy
- **Timeouts:** on statements and connections
- **Idempotency keys:** on payment-like operations

## Mistakes to Avoid
- **Mistake:** Opening a transaction in the controller and holding it across HT…
- **Mistake:** Ignoring serialization / deadlock errors instead of retrying the…
- **Mistake:** Assuming ORM `save()` is upsert — may INSERT duplicates
- **Mistake:** No statement timeout

## Pros/Cons or Trade-offs
- **Pro:** Business invariants stay explicit; retries and timeouts make transient DB failures survivable.
- **Con:** Fat transactions hold locks longer; ORMs can hide N+1 and accidental autocommit if boundaries are unclear.

## Comparison
- vs raw [[SQL]] scripts: the application owns session lifecycle, pooling ([[co…


### Use cases
- Checkout services that debit inventory and create an order atomically, then p…
