[[Messaging/RabbitMQ]] [[Messaging/Kafka/kafka]] [[Messaging/webhook]] [[Messaging/SSE (Server-Sent Events)]] [[Idempotent-key]]

# Message Broker

> Message broker — middleware that accepts messages from producers and delivers them to consumers via queues or streams.

## Interview Relevance
Interviewers want delivery guarantees (at-most/at-least/exactly-once *effects*), ordering, backpressure, and when to pick a queue broker vs a log (Kafka). Name failure modes: poison messages, consumer lag, duplicate processing.

## Sources
- [Wikipedia — Message broker](https://en.wikipedia.org/wiki/Message_broker) — overview
- [Apache Kafka Documentation](https://kafka.apache.org/documentation/) — deep-dive (log-oriented broker)
- [RabbitMQ Docs — Messaging Concepts](https://www.rabbitmq.com/docs/messaging-concepts) — deep-dive (AMQP broker)

## Core Definition
A message broker decouples senders from receivers in time and space: producers publish; the broker stores/routes; consumers pull or are pushed messages without sharing a process or synchronous HTTP call.

## Key Concepts
- **Queue vs stream/log:** Queues (e.g. [[Messaging/RabbitMQ]]) compete consumers; logs (e.g. [[Messaging/Kafka/kafka]]) retain ordered partitions for many consumer groups.
- **Delivery semantics:** Network reality is at-least-once; “exactly-once” is usually idempotent consumers + [[Idempotent-key]] / transactions.
- **Routing:** Exchanges/topics, headers, partitions — where the message goes.
- **Ack / offset:** Progress markers; lose them and you redeliver or skip.

## Technical Details
```txt
Producer ──► Broker (queue / topic partitions)
                 │
                 ├── Consumer group A
                 └── Consumer group B (fan-out / independent lag)
```

Ops signals: queue depth or consumer lag, publish rate, error/DLQ rate, broker disk and ISR health (Kafka).

## Real-World Applications
Order service publishes `order.created`; email, inventory, and analytics consume independently. Live apps may prefer [[Messaging/SSE (Server-Sent Events)]] or [[Messaging/webhook]] for simpler one-way push when you do not need a durable broker.

## Pros/Cons or Trade-offs
- **Pro:** Decoupling, buffering spikes, fan-out, retry isolation.
- **Con:** Operational complexity; duplicates; harder end-to-end tracing; wrong broker type locks the architecture.

## Comparison
vs direct HTTP: sync coupling and no durable buffer. vs [[Messaging/webhook]]: webhooks are point-to-point callbacks; brokers are shared infrastructure. vs DB as queue: works until locking and polling collapse under load.

## Mistakes to Avoid
- Assuming the broker gives exactly-once without consumer design.
- Using Kafka like a job queue without understanding retention and consumer groups.
- Ignoring poison messages / DLQ strategy.
- Letting unbounded queues hide a dead consumer until disk fills.
