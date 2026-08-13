[[Questions]]

# Connection Pool

> Connection Pool — you are tasked with designing a connection pool for a database management module of a complex software application. The connection pool is…

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

- [Wikipedia — Connection Pool](https://en.wikipedia.org/wiki/Connection_Pool)
