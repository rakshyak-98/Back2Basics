[[Python]]

# Python Package Setup

> Python Package Setup — this guide explains how to turn the python/ folder into an installable package for use in other projects.

---

## How it works

This guide explains how to turn the `python/` folder into an installable package for use in other projects.
The sample code under `python/src/` is currently a flat set of scripts. To reuse it as a library, follow the steps below.


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

[[Python]]

## Sources

- [Wikipedia — create python package from source](https://en.wikipedia.org/wiki/create_python_package_from_source)
