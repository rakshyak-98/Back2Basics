[[System Design]] [[orchestration]] [[backpressure]] [[Eventual consistency]]

# event-driven

> Event-driven architecture — services react to facts (“OrderPlaced”) instead of calling each other for every side effect.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Write to a log/bus; consumers update their own models. Decouples deploy and scale; adds eventual consistency and replay complexity.

```txt
Service A ──event──► Bus/Log ──► Consumers B,C
                         │
                      replay / DLQ
```

| Style | Coupling |
|-------|----------|
| Choreography | Consumers listen; no central brain |
| Orchestration | Workflow engine commands steps |
| CQRS | Writes events; reads projections |

---

## Standard config / commands

```json
{
  "type": "order.placed",
  "id": "evt_123",
  "ts": "2026-08-09T12:00:00Z",
  "data": { "orderId": "o1", "total": 1999 }
}
```

| Rule | Why |
|------|-----|
| Idempotent consumers | At-least-once delivery |
| Schema version | Evolve safely |
| Outbox pattern | DB + event atomicity |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Missing side effect | Consumer lag/error | Fix consumer; replay from offset |
| Duplicates | Retry | Idempotency store |
| Dual-write drift | DB commit without event | Transactional outbox |
| Poison message | Same fail forever | DLQ + alert |
| Ordering surprises | Multi-partition key | Choose partition key wisely |

---

## Gotchas

> [!WARNING]
> **Sync request/response hidden in events** — you’ll invent sagas; maybe just RPC.

> [!WARNING]
> **Fat events vs thin** — PII and huge blobs in the bus hurt.

> [!WARNING]
> **No ownership of schemas** — chaos; use registry.

---

## When NOT to use

- **Simple CRUD app** — direct calls clearer.
- **Need immediate cross-service transaction** — rethink boundaries or use orchestrated saga carefully.
- **Tiny team ops** — bus + schemas + DLQ is real cost.

---

## Related

[[orchestration]] [[stateless offset handling]] [[Eventual consistency]] [[backpressure]]
