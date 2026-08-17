[[Messaging/RabbitMQ]] [[Messaging/Kafka/kafka]] [[Messaging/webhook]] [[Messaging/SSE (Server-Sent Events)]] [[Idempotent-key]]

# Message Broker

> Message broker — middleware that accepts messages from producers and delivers them to consumers via queues or streams.

```txt
        Message Broker ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers want delivery guarantees (at-most/at-least/exactly-once *effects…

## Sources
- [Wikipedia — Message broker](https://en.wikipedia.org/wiki/Message_broker) — overview
- [Apache Kafka Documentation](https://kafka.apache.org/documentation/) — deep-dive (log-oriented broker)
- [RabbitMQ Docs — Messaging Concepts](https://www.rabbitmq.com/docs/messaging-concepts) — deep-dive (AMQP broker)

## Key Concepts
- **Queue vs stream/log:** Queues (e.g. [[Messaging/RabbitMQ]]) compete consumers
- **Delivery semantics:** Network reality is at-least-once
- **Routing:** Exchanges/topics, headers, partitions — where the message goes.
- **Ack / offset:** Progress markers; lose them and you redeliver or skip.


- **Core:** A message broker decouples senders from receivers in time and space: producer…

## Technical Details
```txt
Producer ──► Broker (queue / topic partitions)
                 │
                 ├── Consumer group A
                 └── Consumer group B (fan-out / independent lag)
```

- Ops signals: queue depth or consumer lag, publish rate, error/DLQ rate, broke…

## Mistakes to Avoid
- **Mistake:** Assuming the broker gives exactly-once without consumer design
- **Mistake:** Using Kafka like a job queue without understanding retention and…
- **Mistake:** Ignoring poison messages / DLQ strategy
- **Mistake:** Letting unbounded queues hide a dead consumer until disk fills

## Pros/Cons or Trade-offs
- **Pro:** Decoupling, buffering spikes, fan-out, retry isolation.
- **Con:** Operational complexity; duplicates; harder end-to-end tracing; wrong broker type locks the architecture.

## Comparison
- vs direct HTTP: sync coupling and no durable buffer. vs [[Messaging/webhook]]…


### Use cases
- Order service publishes `order.created`
