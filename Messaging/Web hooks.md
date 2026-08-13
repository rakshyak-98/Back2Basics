[[webhook]] [[HTTP module]] [[JWT authentication]]

# Web hooks

> Web hooks — → See webhook (canonical note).

---

## How it works

→ See **[[webhook]]** (canonical note).
This page is a redirect alias for plural search / legacy links.


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

[[webhook]]] [[[HTTP module]]] [[[JWT authentication]]

## Sources

- [Wikipedia — Web hooks](https://en.wikipedia.org/wiki/Web_hooks)
