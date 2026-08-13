[[Design pattern]]

# Abstraction

> Abstraction — it allows interaction with an object through a defined interface, ensuring that only the specified behaviors are accessible, even if…

---

## Index

- [[#Mental model]]
- [[#Core idea]]
- [[#Variations / implementations]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#Trade-offs]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Abstraction is a design idea — I trade something off and I can name the failure mode.


It allows interaction with an object through a defined interface, ensuring that only the specified behaviors are accessible, even if additional functionalities exist in the concrete implementation.
- it allows users to interact with an object through a wall defined interface, ensuring that they only access the necessary behaviors while keeping the underlying complexity hidden.


---

## Core idea

…

## Variations / implementations

…

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

## Trade-offs

| Gain | Cost |
|------|------|
| … | … |

## When NOT to use

- Don’t over-design a CRUD application into Kafka+K8s on day one.

---

## Related

[[Design pattern]]
