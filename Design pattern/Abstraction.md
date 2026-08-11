[[Design pattern]]

# Abstraction

> Abstraction — it allows interaction with an object through a defined interface, ensuring that only the specified behaviors are accessible, even if…

---

## Mental model

**Say it in one breath:** Abstraction is a design idea — I trade something off and I can name the failure mode.


It allows interaction with an object through a defined interface, ensuring that only the specified behaviors are accessible, even if additional functionalities exist in the concrete implementation.
- it allows users to interact with an object through a wall defined interface, ensuring that they only access the necessary behaviors while keeping the underlying complexity hidden.

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Abstraction** | Core idea of this note | “I can explain Abstraction without jargon.” |
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

[[Design pattern]]
