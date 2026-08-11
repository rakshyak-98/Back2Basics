[[Kafka]]

# Zookeeper

> Zookeeper — a distributed coordination service used by kafka to manage metadata, leader election, and synchronization across brokers.

---

## Mental model

**Say it in one breath:** Zookeeper — plain job, how I run it, how I know it’s broken.


is a [[distributed coordination service]] used by kafka to manage metadata, leader election, and synchronization across brokers.
| Function                 | Description                                                     |
| ------------------------ | --------------------------------------------------------------- |
| Broker management        | Keeps track of active Kafka brokers.                            |
| Leader election          | Determines which broker is the leader for a partition.          |
| Topic metadata           | Stores partition details and configurations.                    |
| Consumer offsets         | Tracks the last read message for consumers (in older versions). |
| Distributed coordination | Ensures synchronized updates across kafka brokers.<br>          |
### How does kafka brokers register with Zookeeper when they start?
### How does Zookeeper assigns a controller broker to manage partition leader?

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Zookeeper** | Core idea of this note | “I can explain Zookeeper without jargon.” |
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
