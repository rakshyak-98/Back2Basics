[[Python]]

# User web server gateway interface

> User web server gateway interface — uWSGI acts as a bridge between your web application and the web server (like Nginx or Apache). It takes care of…

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** User web server gateway interface — plain job, how I run it, how I know it’s broken.


```bash
uwsgi --ini uwsgi.ini
```
uWSGI acts as a bridge between your web application and the web server (like Nginx or Apache). It takes care of communication, request handling, and process management.
- You configure uWSGI using a configuration file (often named `uwsgi.ini`). This file contains settings like the application entry point, the number of worker processes, and more.
- uWSGI operates using a master-worker model. The master process manages the worker processes that actually handle incoming requests. Each worker is essentially an instance of your application.

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **User web server gateway interface** | Core idea of this note | “I can explain User web server gateway interface without jargon.” |
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

[[Python]]
