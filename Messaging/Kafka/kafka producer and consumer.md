[[kafka]] [[Kafka broker]] [[Kafka configuration]] [[event-driven]] [[RabbitMQ]]

# kafka producer and consumer

> Writers and readers of Kafka topics — producers append records; consumers track offsets and process events, usually inside a consumer group.

```txt
        kafka producer and ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers probe acks/`enable.idempotence`, key→partition mapping, consumer…

## Sources
- [Kafka docs — Producer configs](https://kafka.apache.org/documentation/#producerconfigs) — deep-dive
- [Kafka docs — Consumer configs](https://kafka.apache.org/documentation/#consumerconfigs) — deep-dive
- [Confluent — Kafka consumers](https://docs.confluent.io/platform/current/clients/consumer.html) — overview

## Key Concepts
- **Keyed partitioning:** same key → same partition → per-key order
- **Acks:** `acks=all` waits for in-sync replicas → durability over latency.
- **Idempotent producer:** broker dedupes producer retries → avoids duplicates on network retry (still n…
- **Consumer group:** partitions split across members → add consumers until you hit partition count.
- **Commit after success:** at-least-once when you commit post-processing


- **Core:** A *producer* publishes records `(key, value, headers)` to a topic partition

## Technical Details
- Reuse a long-lived producer

```js
const { Kafka } = require("kafkajs");

const kafka = new Kafka({
  clientId: "cart-service",
  brokers: ["localhost:9092"],
});

const producer = kafka.producer();
await producer.connect(); // once at process start

await producer.send({
  topic: "cart.item.added",
  messages: [{ key: cartId, value: JSON.stringify(payload) }],
});

const consumer = kafka.consumer({ groupId: "inventory" });
await consumer.connect();
await consumer.subscribe({ topic: "cart.item.added", fromBeginning: false });

await consumer.run({
  eachMessage: async ({ topic, partition, message }) => {
    await handle(message);
    // commit strategy depends on client autoCommit settings
  },
});
```

| Symptom | Check | Fix |
|---------|-------|-----|
| High produce latency | `acks`, batching | Tune linger/batch; review ISR health |
| Frequent rebalances | Processing time | Raise `max.poll.interval.ms`; shorten work |
| Duplicates after crash | Commit timing | Idempotent handlers; transactional patterns |
| Short-lived producer thrash | New client per request | Share one producer per process |

## Mistakes to Avoid
- **Mistake:** Instantiating a producer inside each request handler and disconn…
- **Mistake:** Committing offsets before the database write succeeds
- **Mistake:** Assuming global order across partitions

## Pros/Cons or Trade-offs
- **Pro:** Independent scale of producers and consumers; replay by resetting offsets.
- **Con:** At-least-once is the default mental model — exactly-once needs careful transactional design.
- **Con:** Rebalances pause processing; unstable membership hurts SLAs.

## Comparison
- vs [[RabbitMQ]] consumers: Rabbit acks remove messages from a queue
- vs HTTP fan-out: producers do not wait on every downstream


### Use cases
- Notify inventory/order/discount services when a cart changes without synchron…

- **Example:** Cart service produces `cart.item.added` with `cartId` as key so …
