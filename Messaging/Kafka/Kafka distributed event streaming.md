[[kafka]] [[kafka producer and consumer]] [[Kafka broker]] [[event-driven]] [[RabbitMQ]]

# Kafka distributed event streaming

> Architectural pattern Kafka enables — many services publish and subscribe to durable event streams instead of calling each other synchronously.

## Interview Relevance

Interviewers ask you to contrast event streaming with request/response: decoupling, replay, eventual consistency, and how partitions give parallelism without a shared database for every integration.

## Sources

- [Apache Kafka — Introduction](https://kafka.apache.org/intro) — overview
- [Confluent — Event streaming](https://www.confluent.io/learn/event-streaming/) — overview
- [Kleppmann — Designing Data-Intensive Applications (event logs)](https://dataintensive.net/) — deep-dive

## Core Definition

Distributed event streaming means recording state changes as an ordered sequence of events in a shared log (Kafka topics). Producers append; many consumer groups process independently on their own schedule.

## Key Concepts

- **Event as fact:** `cart.item.added` is an immutable record of something that happened → consumers derive their own views.
- **Decoupling:** producers do not know consumers → new subscribers can join without changing publishers.
- **Replay:** retention lets you rebuild read models or fix bugs by reprocessing from an old offset.
- **Parallelism:** scale by partitions and consumer group members → throughput grows until partition count caps it.
- **Eventual consistency:** downstream stores lag the log → design UX and idempotency accordingly.

## Technical Details

| Component | Role in the pattern |
|-----------|---------------------|
| Producer | Emits domain events to topics |
| Topic | Durable stream (e.g. `cart.item.added`) |
| Broker | Stores and replicates partitions |
| Consumer | Projects events into DB, cache, email, etc. |

```
Checkout service --produce--> topic:order.placed
                                ├─ consumer group:inventory
                                ├─ consumer group:fraud
                                └─ consumer group:analytics
```

Back-pressure shows up as *consumer lag*, not as blocked HTTP threads in the producer (unless you chose synchronous send with tight timeouts).

## Real-World Applications

Microservice integration, clickstream pipelines, CDC from databases into search/analytics, and activity feeds.

**Example:** After placing an order, the API writes to its DB and produces `order.placed`; inventory and email services catch up asynchronously from the topic.

## Pros/Cons or Trade-offs

- **Pro:** Independent deploy/scale of consumers; auditability and replay.
- **Con:** Harder end-to-end reasoning than a single ACID transaction across services.
- **Con:** Requires idempotent consumers and clear event contracts (schema evolution).

## Comparison

- vs [[kafka]]: platform/mechanics versus this note’s *pattern* focus — link both in interviews.
- vs synchronous REST: streaming favors throughput and isolation; REST favors immediate consistency and simpler debugging.
- vs [[RabbitMQ]] work queues: streaming keeps history for many subscriber groups; classic queues optimize task delivery.

## Mistakes to Avoid

- Emitting events *before* the local transaction commits (listeners see phantoms).
- Designing huge “god events” that break when one field changes — prefer versioned, focused payloads.
- Expecting every consumer to see events at the same instant.
