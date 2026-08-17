[[GIT]]

# git error

> git error — drwxr-xr-x 2 root root 4096 Jul 3 18:35 test/





## Interview Relevance
Git error interviews check whether you can diagnose from messages — detached HEAD, rejected non-fast-forward, index locks.

## Sources
- [Pro Git book](https://git-scm.com/book/en/v2) — deep-dive
- [Git reference documentation](https://git-scm.com/docs) — overview

## Technical Details
```bash
git status
git remote -v
GIT_TRACE=1 git fetch
git config --list --show-origin
```

1. …

## Pros/Cons or Trade-offs
- Do not force-push to shared branches to silence errors — coordinate with the team.

## Mistakes to Avoid
> [!WARNING]
> Read the **first error line** in the message — later lines are often cascading noise.

| Symptom | Check | Fix |
|---------|-------|-----|
| Permission denied (publickey) | SSH key loaded; remote URL | `ssh -T git@github.com`; fix `~/.ssh/config` |
| Repository not found | Remote URL; access token scope | Verify org/repo name and credentials |
| Failed to push (non-fast-forward) | Remote has new commits | `git pull --rebase` then push |
| Unable to index file | File permissions; line endings | `chmod`; check `core.autocrlf` |

1. …

```bash
# …
```
