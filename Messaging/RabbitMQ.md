[[kafka]] [[MQTT]] [[webhook]] [[event-driven]] [[distributed system]]

# RabbitMQ

> Message broker that speaks AMQP — producers publish to exchanges, which route messages into queues for consumers to process asynchronously.

```txt
        RabbitMQ ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers use RabbitMQ to check exchange/queue/binding mental models, ackn…

## Sources
- [RabbitMQ documentation — AMQP 0-9-1 model](https://www.rabbitmq.com/tutorials/amqp-concepts.html) — deep-dive
- [RabbitMQ — Reliability](https://www.rabbitmq.com/docs/reliability) — deep-dive
- [Wikipedia — RabbitMQ](https://en.wikipedia.org/wiki/RabbitMQ) — overview

## Key Concepts
- **Exchange types:** `direct`, `topic`, `fanout`, `headers` → routing key / pattern decides fan-ou…
- **Queue:** durable buffer of messages waiting for consumers → scale consumers for parall…
- **Acknowledgements:** manual ack after successful processing → crash before ack redelivers (at-leas…
- **Dead-letter exchange (DLX):** poison messages move aside after N failures → inspect without blocking the ma…
- **Prefetch:** limits unacked messages per consumer → prevents one fast connection from hoar…


- **Core:** RabbitMQ is an open-source broker. Publishers send messages to an *exchange*

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

## Mistakes to Avoid
- **Mistake:** Acknowledging before the side effect is durable
- **Mistake:** Using a single queue for unrelated workloads without TTL/DLX
- **Mistake:** Expecting global strict ordering across many consumers without d…

## Pros/Cons or Trade-offs
- **Pro:** Flexible routing, mature operational tooling, strong fit for task queues and request/reply.
- **Con:** Not designed as a long retention event log — replay history is weaker than [[kafka]].
- **Con:** At-least-once delivery demands idempotent consumers.

## Comparison
- vs [[kafka]]: RabbitMQ routes messages through queues (often deleted after consume)
- vs [[MQTT]]: MQTT is a lightweight pub/sub protocol (IoT-friendly)
- vs [[webhook]]: Webhooks are HTTP callbacks to external systems; RabbitMQ is an internal broker.


### Use cases
- Background jobs, email/SMS dispatch, work queues between microservices, and f…

- **Example:** An order service publishes `order.created` to a topic exchange
