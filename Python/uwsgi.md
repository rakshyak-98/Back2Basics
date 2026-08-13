[[Python]]

# User web server gateway interface

> User web server gateway interface — uWSGI acts as a bridge between your web application and the web server (like Nginx or Apache). It takes care of…

---

## How it works

```bash
uwsgi --ini uwsgi.ini
```
uWSGI acts as a bridge between your web application and the web server (like Nginx or Apache). It takes care of communication, request handling, and process management.
- You configure uWSGI using a configuration file (often named `uwsgi.ini`). This file contains settings like the application entry point, the number of worker processes, and more.
- uWSGI operates using a master-worker model. The master process manages the worker processes that actually handle incoming requests. Each worker is essentially an instance of your application.


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

- [Wikipedia — uwsgi](https://en.wikipedia.org/wiki/uwsgi)
