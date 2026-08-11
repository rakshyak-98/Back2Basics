[[Questions]]

# File based configuration manager

> File based configuration manager — you are tasked with creating a system-wide configuration manager for a complex software suite. The configuration manager…

---

## Mental model

**Say it in one breath:** File based configuration manager is a design idea — I trade something off and I can name the failure mode.


### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **File based configuration manager** | Core idea of this note | “I can explain File based configuration manager without jargon.” |
| **scalability** | Handle more load | “Scale reads and writes differently.” |
| **availability** | Stay up on failure | “Redundancy plus health checks.” |
| **consistency** | Same data everywhere | “Pick C or A under partition.” |

---

## Standard config / commands

```bash
# sketch
# actors, data stores, failure domains
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Hot key / hotspot | metrics by key | Shard or cache |
| Cascading failure | timeouts/bulkheads | Add limits and backoff |
| Split brain | fencing / quorum | Use consensus or single writer |

---

## Gotchas

> [!WARNING]
> Draw the failure mode before the happy path.

---

## When NOT to use

- Don’t over-design a CRUD app into Kafka+K8s on day one.

---

## Related

[[Questions]]
