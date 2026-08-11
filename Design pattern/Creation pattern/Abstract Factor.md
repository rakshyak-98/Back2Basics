[[Creation pattern]]

# Abstract Factor

> Abstract Factor — → Design pattern/Creation pattern/Abstract Factory

---

## Mental model

**Say it in one breath:** Abstract Factor is a design idea — I trade something off and I can name the failure mode.


→ [[Design pattern/Creation pattern/Abstract Factory]]
Typo stub. Canonical note: [[Design pattern/Creation pattern/Abstract Factory]].


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

- Don’t over-design a CRUD application into Kafka+K8s on day one.

---

## Related

[[Creation pattern]]
