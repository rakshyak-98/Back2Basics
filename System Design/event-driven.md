[[orchestration]] [[backpressure]] [[Eventual consistency]] [[stateless offset handling]]

# event-driven

> Event-driven architecture publishes facts ("OrderPlaced", "UserRegistered") to a durable log or bus so downstream services react asynchronously — decoupling deploy and scale at the cost of eventual consistency and operational complexity.

---

## Choreography versus orchestration

```txt
Service A ──event──► Bus / log ──► Consumers B, C
                         │
                    replay / dead-letter queue
```

| Style | Who coordinates |
|-------|-----------------|
| **Choreography** | Each consumer reacts; no central brain |
| **Orchestration** | Workflow engine commands steps ([[orchestration]]) |
| **Command Query Responsibility Segregation** | Writes emit events; reads use projections |

Choose choreography when steps are loosely coupled; orchestration when you need visible workflow state and compensations (sagas).

## Event envelope

```json
{
  "type": "order.placed",
  "id": "evt_123",
  "ts": "2026-08-09T12:00:00Z",
  "data": { "orderId": "o1", "totalCents": 1999 }
}
```

| Rule | Why |
|------|-----|
| Idempotent consumers | Delivery is at-least-once |
| Schema versioning | Evolve without breaking all consumers |
| Transactional outbox | Database commit and event publish atomically |
| Partition key | Per-entity ordering when needed |

## Failure modes

| Symptom | Direction |
|---------|-----------|
| Missing side effect | Consumer lag or error — fix and replay from offset ([[stateless offset handling]]) |
| Duplicates | Idempotency store keyed by event identifier |
| Database updated, no event | Outbox pattern — never dual-write without coordination |
| Poison message | Dead-letter queue and alert |
| Ordering surprises | Wrong partition key — co-locate related events |

## Trade-offs

**Pros:** independent scaling, temporal decoupling, audit trail, replay for new projections.

**Cons:** debugging across async boundaries, schema governance, consumer lag monitoring, [[Eventual consistency]] in read models.

Simple create-read-update-delete with three services may stay synchronous ([[KISS]]). Event buses are not free — budget operators and schema registry.

*When would you still use remote procedure call?* Request-response with immediate answer and strong consistency on one aggregate.

## Sources

- Martin Kleppmann, *Designing Data-Intensive Applications* — logs, streams, and processing.
- Enterprise Integration Patterns (Hohpe & Woolf) — message channel patterns.
- Chris Richardson, microservices.io — saga and event-driven patterns.
