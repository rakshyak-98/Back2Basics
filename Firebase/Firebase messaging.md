[[Firebase]]

# Firebase messaging

> Firebase messaging — the current code has a logic flaw: it limits the token list to 500 (slice(0, 500)) but does not handle tokens beyond 500 or split

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Firebase messaging — plain job, how I run it, how I know it’s broken.


[Firebase Multicast Message](https://firebase.google.com/docs/reference/admin/java/reference/com/google/firebase/messaging/MulticastMessage)

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Firebase messaging** | Core idea of this note | “I can explain Firebase messaging without jargon.” |
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

[[Firebase]]
