[[GIT]]

# git commit

> git commit — snapshot of the index; the unit of Git history.

---

## How it works


## Configuration and commands

```bash
git add file.txt
git commit -m "describe the change"
git commit --amend --no-edit          # add to last commit, keep message
git commit --amend -m "new message"
git status
git diff --cached                   # what will be committed
```

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| Nothing to commit | `git status`; unstaged changes | `git add` first |
| Commit rejected (hook) | `.git/hooks/pre-commit` output | Fix hook failure or `--no-verify` only if policy allows |
| Wrong files committed | `git show --stat HEAD` | `git reset --soft HEAD~1` then re-stage |
| Author/email wrong | `git config user.name`; `git config user.email` | Set locally or globally before commit |

---


## Gotchas

> [!WARNING]
> **Commit only stages what you added** — `git commit` does not pick up unstaged edits.

---


## When not to use

- Do not commit secrets, build artifacts, or `.env` files — use `.gitignore`.


---


## Related

[[GIT]]

## Sources

- [Wikipedia — git commit](https://en.wikipedia.org/wiki/git_commit)
