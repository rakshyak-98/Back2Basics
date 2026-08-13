[[Database]] [[connection pooling]] [[Data access patterns]] [[SQL]]

# database application

> The application layer that issues queries—ORMs, repositories, transaction boundaries, and retry logic that turn business operations into [[ACID]]-safe database work.

## Responsibility split

```txt
Controller ──► Service (transaction boundary) ──► Repository/ORM ──► [[SQL]]
```

The database enforces constraints; the application enforces workflows (state machines, idempotency keys).

## Transaction boundaries

Wrap multi-step invariants in one transaction:

```python
with db.begin():
    debit(account_a, amount)
    credit(account_b, amount)
```

## Resilience patterns

- **Retry** serialization failures (`40001` in PostgreSQL)
- **Circuit breaker** when database is unhealthy
- **Timeouts** on statements and connections
- **Idempotency keys** on payment-like operations

## Sources

- Kleppmann, *DDIA*, Ch. 7–9
- PostgreSQL Documentation — [Error Codes](https://www.postgresql.org/docs/current/errcodes-appendix.html)
