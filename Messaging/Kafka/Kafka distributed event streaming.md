<!-- note-strategy: operational -->
[[Kafka]]

# Kafka distributed event streaming

> Kafka distributed event streaming — kafka is a distributed event streaming platform used for real-time data processing.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Kafka distributed event streaming — kafka is a distributed event streaming platform used for real-time data processing.

Kafka is a distributed event streaming platform used for real-time data processing.
- it helps microservices communicate asynchronously by sending and receiving messages efficiently.
### How kafka works
kafka consist of four main components
| Component | Description                                                    |
| --------- | -------------------------------------------------------------- |
| Producer  | sends message (events) to kafka topics.                        |
| Topic     | A category where message are stored. Example `cart.item.added` |
| Broker    | Kafka servers that manage topics and messages.                 |
| Consumer  | Listens to topics and process messages.                        |


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
