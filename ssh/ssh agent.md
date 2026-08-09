[[ssh]]

# and define "github-personal" in ~/.ssh/config with the right IdentityFile

> and define "github-personal" in ~/.ssh/config with the right IdentityFile — use ssh-agent to hold your keys in memory. This prevents the need to type the…

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** and define "github-personal" in ~/.ssh/config with the right IdentityFile is infra/security tooling — least privilege, clear config, observable failures.


use `ssh-agent` to hold your keys in memory. This prevents the need to type the passphrase repeatedly while keeping the key encrypted on the disk.

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **and define "github-personal" in ~/.ssh/config with the right IdentityFile** | Core idea of this note | “I can explain and define "github-personal" in ~/.ssh/config with the right IdentityFile without jargon.” |
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

[[ssh]]
