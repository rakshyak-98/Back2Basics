[[Nginx]]

# nginx URL rewrite

> nginx URL rewrite — what happens when user goes to /about

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** nginx URL rewrite is infra/security tooling — least privilege, clear config, observable failures.


|Nginx directive|What it actually does|When your browser URL becomes|Real folder on disk|
|---|---|---|---|
|`root /var/www/html;`|Physical folder|unchanged|`/var/www/html/blog/post1.html`|
|`alias`|Replace entire path|unchanged|something else|
|`try_files`|“Look here, then here, then fallback”|unchanged|multiple places|
|`rewrite`|**Changes the URL inside Nginx before it looks for files**|can change|depends|
|`return` / `proxy_pass`|Final answer|can change|doesn’t matter|

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **nginx URL rewrite** | Core idea of this note | “I can explain nginx URL rewrite without jargon.” |
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
