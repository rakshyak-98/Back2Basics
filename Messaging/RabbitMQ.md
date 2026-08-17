[[kafka]] [[MQTT]] [[webhook]] [[event-driven]] [[distributed system]]

# RabbitMQ

> Message broker that speaks AMQP — producers publish to exchanges, which route messages into queues for consumers to process asynchronously.





## Interview Relevance
Interviewers use RabbitMQ to check exchange/queue/binding mental models, acknowledgement and dead-letter behavior, and when you would pick it versus [[kafka]]’s log-oriented stream.

## Sources
- [RabbitMQ documentation — AMQP 0-9-1 model](https://www.rabbitmq.com/tutorials/amqp-concepts.html) — deep-dive
- [RabbitMQ — Reliability](https://www.rabbitmq.com/docs/reliability) — deep-dive
- [Wikipedia — RabbitMQ](https://en.wikipedia.org/wiki/RabbitMQ) — overview

## Core Definition
RabbitMQ is an open-source broker. Publishers send messages to an *exchange*; bindings decide which *queue* receives a copy; consumers pull or get pushed messages and *ack* when work is done.

## Key Concepts
- **Exchange types:** `direct`, `topic`, `fanout`, `headers` → routing key / pattern decides fan-out.
- **Queue:** durable buffer of messages waiting for consumers → scale consumers for parallelism.
- **Acknowledgements:** manual ack after successful processing → crash before ack redelivers (at-least-once).
- **Dead-letter exchange (DLX):** poison messages move aside after N failures → inspect without blocking the main queue.
- **Prefetch:** limits unacked messages per consumer → prevents one fast connection from hoarding work.

## Technical Details
```
Producer → Exchange --binding--> Queue → Consumer
                 \--binding--> Queue → Consumer
```

```bash
# Management plugin / CLI examples (broker must be running)
rabbitmqctl list_queues name messages consumers
rabbitmqctl list_exchanges
rabbitmq-diagnostics status
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Queue depth grows | Consumer lag / errors | Scale consumers; fix handler; add DLX |
| Duplicate processing | Redelivery after crash | Make handlers idempotent |
| Connection flaps | Heartbeats / load balancer idle | Tune heartbeat; sticky timeouts |
| “Lost” messages | Non-durable queue + restart | Durable queue + persistent messages + publisher confirms |

## Real-World Applications
Background jobs, email/SMS dispatch, work queues between microservices, and fan-out notifications where each consumer needs its own copy of a task.

**Example:** An order service publishes `order.created` to a topic exchange; inventory and billing queues each get a copy via bindings.

## Pros/Cons or Trade-offs
- **Pro:** Flexible routing, mature operational tooling, strong fit for task queues and request/reply.
- **Con:** Not designed as a long retention event log — replay history is weaker than [[kafka]].
- **Con:** At-least-once delivery demands idempotent consumers.

## Comparison
- vs [[kafka]]: RabbitMQ routes messages through queues (often deleted after consume); Kafka retains a partitioned log for replay and high throughput streams.
- vs [[MQTT]]: MQTT is a lightweight pub/sub protocol (IoT-friendly); RabbitMQ can speak MQTT via plugins but AMQP is its core model.
- vs [[webhook]]: Webhooks are HTTP callbacks to external systems; RabbitMQ is an internal broker.

## Mistakes to Avoid
- Acknowledging before the side effect is durable — crashes lose work without redelivery.
- Using a single queue for unrelated workloads without TTL/DLX — poison messages block everyone.
- Expecting global strict ordering across many consumers without designing for it.
