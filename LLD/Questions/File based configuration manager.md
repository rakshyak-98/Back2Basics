[[Questions]]

# File based configuration manager

> File based configuration manager — you are tasked with creating a system-wide configuration manager for a complex software suite. The configuration manager…

---

## How it works


---


## Configuration and commands

```bash
# sketch
# actors, data stores, failure domains
```

---


## When things break

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


## When not to use

- Don’t over-design a CRUD application into Kafka+K8s on day one.

---


## Related

[[Questions]]

## Sources

- [Wikipedia — File based configuration manager](https://en.wikipedia.org/wiki/File_based_configuration_manager)
