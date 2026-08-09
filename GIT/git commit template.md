[[GIT]]

# git commit template

> git commit template — git config to use custom commit template

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** git commit template is infra/security tooling — least privilege, clear config, observable failures.


**Git config to use custom commit template**
```bash
git config --global commit.template ~/.config/git/commit-template
```
```text
<type>(<scope>): <short summary 50-72 chars>
<body - optional>
Explain **why** this change + **context** if needed (especially for tricky parts)
BREAKING CHANGE: <description if any>   ← only when really breaking
Resolves: #123
See also: #456
```
- feat        → new feature
- fix         → bug fix
- docs        → documentation only
- style       → formatting, missing semicolons, etc (no code change)
- refactor    → code change that neither fixes bug nor adds feature
- perf        → performance improvement
- test        → adding or correcting tests
- build       → build system, CI, external dependencies
- chore       → maintenance (gitignore, scripts, rename...)
- revert      → revert previous commit

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **git commit template** | Core idea of this note | “I can explain git commit template without jargon.” |
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
