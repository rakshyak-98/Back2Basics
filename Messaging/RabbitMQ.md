[[Messaging]]

# RabbitMQ

> RabbitMQ — they will be loaded in alphabetical order. A common naming practice uses numerical prefixes in filenames to make it easier to reason about the…

---

## How it works

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

[[Messaging]]

## Sources

- [Wikipedia — RabbitMQ](https://en.wikipedia.org/wiki/RabbitMQ)
