[[Kafka]]

# Kafka broker

> Kafka broker — a broker in Apache Kafka is server that acts as an intermediary between producers (who send messages) and consumers (who receive messages).

---

## Mental model

**Say it in one breath:** Kafka broker — plain job, how I run it, how I know it’s broken.


A broker in Apache Kafka is server that acts as an intermediary between producers (who send messages) and consumers (who receive messages).
| feature              | Description                                                       |
| -------------------- | ----------------------------------------------------------------- |
| Message storage      | Stores messages in topics and partitions.                         |
| Message routing      | Distributes messages from producers to consuers.                  |
| partition Management | handles partition assignments and replications.                   |
| Load balancing       | Spreads workload across multiple brokers in a kafka cluster.      |
| Replication          | Ensures fault tolerance by duplicating partitions across brokers. |
### Why is it called a Topic in Kafka?
The term _topic_ in kafka is inspired by publish-subscribe messaging systems.
- it represents a logical channel where messages are categorized, similar to how topics work in forums or newsletters.

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Kafka broker** | Core idea of this note | “I can explain Kafka broker without jargon.” |
| **idempotent** | Safe to retry | “Retries must not double-charge.” |
| **config** | Knobs outside code | “Env-specific values stay out of source.” |

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
