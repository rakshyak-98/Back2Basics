[[Questions]]

# Connection Pool

> Connection Pool — you are tasked with designing a connection pool for a database management module of a complex software application. The connection pool is…

---

## Mental model

**Say it in one breath:** Connection Pool is a design idea — I trade something off and I can name the failure mode.


### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Connection Pool** | Core idea of this note | “I can explain Connection Pool without jargon.” |
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
