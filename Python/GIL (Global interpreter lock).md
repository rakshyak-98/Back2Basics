<!-- note-strategy: operational -->
[[Python]]

# GIL (Global interpreter lock)

> GIL (Global interpreter lock) — global interpreter lock : A global interpreter lock is a mechanism used in computer-language interpreters to synchronise the…

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** GIL (Global interpreter lock) — global interpreter lock : A global interpreter lock is a mechanism used in computer-language interpreters to synchronise the…

[GIL](https://en.wikipedia.org/wiki/Global_interpreter_lock](https://en.wikipedia.org/wiki/Global_interpreter_lock)
**Global interpreter lock** : A global interpreter lock is a mechanism used in computer-language interpreters to synchronise the execution of threads so that only one native thread (pre process) can execute one thread to execute at a time, even if run on a multi-core processor.
- application running on implementations with a GIL can be designed to use separate processes to achieve full parallelism, as each process has its own interpreter and in turn has its own GIL.
- otherwise the GIL can be a significant barrier to parallelism.


---

## Standard config / commands

```bash
# version + config path
# dry-run when available
```

---

## Triage (when things break)

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

## When NOT to use

- Avoid the tool if a simpler built-in covers the job.

---

## Related

[[Python]]
