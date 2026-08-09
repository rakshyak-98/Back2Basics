[[helm]]

# helm

> helm — the kind field is not part of the basic required fields, but it can be added to specify the type of chart. The kind field should

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** helm is infra/security tooling — least privilege, clear config, observable failures.


```bash
helm list
helm get values
```
- The `kind` field is not part of the basic required fields, but it can be added to specify the type of chart. The `kind` field should be used for custom resources, as it helps Helm understand how to process the resource during installation and upgrade

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **helm** | Core idea of this note | “I can explain helm without jargon.” |
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

[[helm]]
