[[Kafka]]

# kafka producer and consumer

> kafka producer and consumer — a kafka producer is a component responsible for sending messages (events) to Kafka topics.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** kafka producer and consumer — a kafka producer is a component responsible for sending messages (events) to Kafka topics.

A kafka producer is a component responsible for sending messages (events) to Kafka topics.
- used to notify other microservices (e.g., Inventory, Order, and Discount services).
Decouples services -> ensure [[event-driven]] architecture, reducing direct dependencies between services.
Asynchronous processing -> improves performance by processing cart updates in the background.
### Why disconnect is called each time?
In, Kafka, the `disconnect` is called each time a producer is instantiated and sends a message if a new connection is created and closed immediately rather than being
#### Short lived producer
- if the kafka producer is instantiated inside a function and not reused, it will create a new connection each time a message is sent.
```js
const {Kafka} = require("kafkajs");
const kafka = new Kafka({
	clientId: 'cart-service',
	brokers: ["localhost:9092"], // Actual Kafka brokers
})
const producer = kafka.producer();


---

## Standard config / commands

```bash
# version + config path
# dry-run when available
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Retry storm | backoff / jitter | Cap retries; circuit break |
| Config drift | plan/apply or lockfile | Single source of truth |
| Poison message | DLQ | Quarantine and alert |

---

## Gotchas

> [!WARNING]
> Make retries safe or you will duplicate side effects.

---

## When NOT to use

- Avoid the tool if a simpler built-in covers the job.

---

## Related

[[Kafka]]
