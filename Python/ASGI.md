[[Python]]

# ASGI

> ASGI — web servers to forward request to asynchronous-capable python programming language frameworks, and applications.

---

## Mental model

**Say it in one breath:** ASGI — web servers to forward request to asynchronous-capable python programming language frameworks, and applications.

Asynchronous Server Gateway Interface (ASGI)
web servers to forward request to asynchronous-capable python programming language frameworks, and applications.
- built as a successor to the Web Server Gateway Interface ([[WSGI]]). Superset of WSGI.
- WSGI provide a standard for synchronous Python application, ASGI porvides one for both asynchronous and synchronous applications, with a WSGI backwards-compatibility implementation and multiple servers and application frameworks.
- allowing WSGI applications to be run inside ASGI servers through a translation wrapper (provided in the asgiref library).
>[!NOTE] WSGI
>A thread pool can be used to run the synchronous WSGI applications away from the async event loop
>


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
