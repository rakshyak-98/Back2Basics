[[Kafka]]

# kafka

> kafka — event streaming platform designed to handle real-time data feeds.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** kafka — plain job, how I run it, how I know it’s broken.


- event streaming platform designed to handle real-time data feeds.
- used for building data pipelines, stream analytics, and integration across systems.
- Scale horizontally by distributing data across multiple brokers.
- producer and consumers are independent, allowing system flexibility.
**Producers**: Send data (message) to Kafka topics.
**Consumers**: Read data from topics.
**Topics**: Logical storage units to organize message. Each topic can have multiple partitions for parallelism.
**Brokers**: Kafka servers managing storage and distribution of topics.
**ZooKeeper (or Kafka Raft)**: Coordinates brokers and maintains cluster metadata.
### kafka docker contianer

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **kafka** | Core idea of this note | “I can explain kafka without jargon.” |
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
