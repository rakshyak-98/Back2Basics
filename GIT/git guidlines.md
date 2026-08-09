[[GIT]]

# git guidlines

> git guidlines — feat: add new inventory endpoint

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** git guidlines is infra/security tooling — least privilege, clear config, observable failures.


```vbnet
feat: add new inventory endpoint
fix: correct inventory route response
docs: update inventory API documentation
refactor: improve inventory route structure
test: add inventory route tests
```
```vbnet
feat: add GET /inventory pagination support
feat: implement inventory search endpoint
fix: handle empty inventory response
perf: optimize inventory query performance
security: add authentication to inventory routes
```
```vbnet
<type>: <subject>
[optional body]
[optional footer]
Example:
feat: add inventory filtering endpoint
- Implements filtering by asset type
- Adds validation for filter parameters
- Includes error handling for invalid filters
Ticket: AT-123
```
- keep first line under 50 characters
- use imperative mood (add not added)
- include relevant ticket/issues numbers
- separate subject from body with blank line
- describe what and why, not how

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **git guidlines** | Core idea of this note | “I can explain git guidlines without jargon.” |
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

[[GIT]]
