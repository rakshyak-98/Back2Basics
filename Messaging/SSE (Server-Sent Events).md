[[Messaging]]

# SSE (Server-Sent Events)

> SSE (Server-Sent Events) — uni directional push from server to browser over HTTP.

---

## How it works

- uni directional push from server to browser over HTTP.
- server pushes events -> client auto-receives over single long-lived connection.


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

- [Wikipedia — SSE](https://en.wikipedia.org/wiki/SSE)
