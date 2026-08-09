[[GIT]]

# git diff

> git diff — show unstaged, staged, or commit-to-commit file changes.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** git diff is infra/security tooling — least privilege, clear config, observable failures.


```bash
git diff --name-only;
git diff --cached --name-only;
git diff main.. --name-only;
git diff --name-status;
```
- compare file in different brach
```bash
git diff branch1 branch2 -- <file path>;
```
```bash
git diff --stat
git diff --shortstat
```
```bash
git diff --cached;
git diff --staged;
git diff HEAD;
git diff HEAD~1 HEAD;
git diff main...HEAD;
git diff main..feature;
```
```bash
git diff v1.2.3 v1.3.0 --name-only;
git diff abc123..def456;
git diff --since="2 days ago" --name-only;
```
### Filter by path/pattern
```bash
git diff -- src/;
git diff -- '*.js' '*.ts' '*.tsx';
git diff -- . ':!node_modules';
git diff --diff-filter=R --name-only;
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **git diff** | Core idea of this note | “I can explain git diff without jargon.” |
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
