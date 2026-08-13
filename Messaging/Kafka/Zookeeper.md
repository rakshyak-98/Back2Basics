[[Kafka]]

# Zookeeper

> Zookeeper — a distributed coordination service used by kafka to manage metadata, leader election, and synchronization across brokers.

---

## How it works

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


---


## Configuration and commands

```bash
# version + config path
# dry-run when available
```

---


## When things break

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


## When not to use

- Avoid the tool if a simpler built-in covers the job.

---


## Related

[[Kafka]]

## Sources

- [Wikipedia — Zookeeper](https://en.wikipedia.org/wiki/Zookeeper)
