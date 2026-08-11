[[Nginx]]

# URL Rewriting

> URL Rewriting — a technique used by web servers (like Apache, Nginx, IIS, etc.) or web frameworks to transform a "pretty" or user-friendly URL into a…

---

## Mental model

**Say it in one breath:** URL Rewriting is infra/security tooling — least privilege, clear config, observable failures.


URL rewriting is a technique used by web servers (like Apache, Nginx, IIS, etc.) or web frameworks to **transform a "pretty" or user-friendly URL into a different internal URL** that the server actually uses to locate and serve the correct file, script, or content.
### Why is it used?
Most modern web applications (especially single-page applications or framework-based sites like React, Angular, Vue, Laravel, Next.js, etc.)
- do **not** have real physical files or folders for every URL path. Instead, they use **client-side routing** or **server-side routing** that points many (or all) URLs to a single entry point (e.g., index.html or app.php).
To make this work without breaking when users refresh the page or visit a deep link directly, the server uses **URL rewriting** to redirect all requests (or specific patterns) to that single entry point.

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **URL Rewriting** | Core idea of this note | “I can explain URL Rewriting without jargon.” |
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
