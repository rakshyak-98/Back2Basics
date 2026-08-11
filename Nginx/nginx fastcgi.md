[[Nginx]]

# nginx fastcgi

> nginx fastcgi — if you want nginx to handle other languages, you have two main routes.

---

## Mental model

**Say it in one breath:** nginx fastcgi is infra/security tooling — least privilege, clear config, observable failures.


[fastcgi_module](https://nginx.org/en/docs/http/ngx_http_fastcgi_module.html#fastcgi_split_path_info)
if you want nginx to handle other languages, you have two main routes.

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **nginx fastcgi** | Core idea of this note | “I can explain nginx fastcgi without jargon.” |
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
