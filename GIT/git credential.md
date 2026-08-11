[[GIT]]

# 1. When git runs a command like `git push` it internally calls.

> 1. When git runs a command like `git push` it internally calls. — create auth token from GitHub personal access token

---

## Mental model

**Say it in one breath:** 1. When git runs a command like `git push` it internally calls. is infra/security tooling — least privilege, clear config, observable failures.


### reset the credential manager
```bash
git config --global --unset credentila.*; # remove the set credential helper
git clone <https remote repo url>;
git pull; # git will ask the username and auth token.
```
- create auth token from [GitHub personal access token](https://github.com/settings/tokens)
- paste the auth token password.
```bash
git config --global credential.helper cache;
```
- the `cache` helper stores credentials in memory only, not on disk.
- Git spawn the credentials cache daemon in the background.
- it keeps the credentials in RAM for 15 minutes by default.
- no file is written.
- once expired or system restarts -> the data is gone.
```bash
printf "protocol=https\nhost=github.com\n\n" | git credential fill;
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **1. When git runs a command like `git push` it internally calls.** | Core idea of this note | “I can explain 1. When git runs a command like `git push` it internally calls. without jargon.” |
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
