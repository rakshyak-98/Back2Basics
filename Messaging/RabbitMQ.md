[[Messaging]]

# RabbitMQ

> RabbitMQ — they will be loaded in alphabetical order. A common naming practice uses numerical prefixes in filenames to make it easier to reason about the…

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** RabbitMQ — plain job, how I run it, how I know it’s broken.


### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **RabbitMQ** | Core idea of this note | “I can explain RabbitMQ without jargon.” |
| **idempotent** | Safe to retry | “Retries must not double-charge.” |
| **config** | Knobs outside code | “Env-specific values stay out of source.” |

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

[[Messaging]]
