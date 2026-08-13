[[GIT]]

# git error

> git error — drwxr-xr-x 2 root root 4096 Jul 3 18:35 test/

---

## Index

- [[#Triage (when things break)]]
- [[#Preconditions]]
- [[#Steps]]
- [[#Verification]]
- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Rollback]]
- [[#Escalation]]
- [[#Related]]

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Permission denied (publickey) | SSH key loaded; remote URL | `ssh -T git@github.com`; fix `~/.ssh/config` |
| Repository not found | Remote URL; access token scope | Verify org/repo name and credentials |
| Failed to push (non-fast-forward) | Remote has new commits | `git pull --rebase` then push |
| Unable to index file | File permissions; line endings | `chmod`; check `core.autocrlf` |

---

## Preconditions

…

## Steps

1. …

## Verification

```bash
# …
```

## Mental model

**Say it in one breath:** git error — drwxr-xr-x 2 root root 4096 Jul 3 18:35 test/

## Standard config / commands

```bash
git status
git remote -v
GIT_TRACE=1 git fetch
git config --list --show-origin
```

---

## Gotchas

> [!WARNING]
> Read the **first error line** in the message — later lines are often cascading noise.

---

## When NOT to use

- Do not force-push to shared branches to silence errors — coordinate with the team.


---

## Rollback

1. …

## Escalation

…

## Related

[[GIT]]
