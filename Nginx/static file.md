[[Nginx]]

# static file

> static file — try_files — checks the filesystem for one or more paths in order.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** static file is infra/security tooling — least privilege, clear config, observable failures.


### Nginx static file serving rule for a location
```nginx
location / {
    try_files $uri $uri/ =404;
}
```
`try_files` -> checks the filesystem for one or more paths in order.
`$uri` -> the exact file path from the request e.g. `/index.html` -> `/var/www/global/index.html`
`$uri/` -> the same but as a directory path e.g. `/docs/` if this exists, nginx can serve `index.html` from inside it (depending on your `index` directive).
`=404` -> if neither a matching file nor a matching directory exists, return HTTP 404 immediately (instead of falling back to a PHP handler).
**What it means in practice**
- If `/style.css` exists in your `root` → serve it.
- If `/blog/` exists as a directory and contains an `index.html` → serve that.
- If neither exists → return `404 Not Found`.
- It **avoids unnecessary backend calls** — Nginx won’t forward these requests to PHP/Python/etc. unless they match a different location.

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **static file** | Core idea of this note | “I can explain static file without jargon.” |
| **least privilege** | Only needed access | “Grant the smallest role that works.” |
| **secret** | Password/key/token | “Secrets out of git; rotate them.” |
| **observability** | metrics/logs/traces | “You can’t fix what you can’t see.” |

---

## Standard config / commands

```bash
# status
# check version, auth, and recent changes
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Auth fail | clock / creds / IAM | Sync time; fix policy |
| TLS error | cert chain / SNI | Fix certs and CA bundle |
| Deploy down | rollback / health | Roll back; check probes |

---

## Gotchas

> [!WARNING]
> Never commit long-lived secrets.

---

## When NOT to use

- Don’t build custom infra when managed services meet the SLO.

---

## Related

[[Nginx]]
