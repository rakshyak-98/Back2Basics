[[GIT]]

# git commit

> git commit — snapshot of the index; the unit of Git history.

```txt
        git commit ──┬── Why it matters
               ├── Sources
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Why It Matters
- **Key signal:** Commit reviews probe atomic commits, message quality, and amend/fixup safe…

## Sources
- [Pro Git book](https://git-scm.com/book/en/v2) — deep-dive
- [Git reference documentation](https://git-scm.com/docs) — overview

## Technical Details
```bash
git add file.txt
git commit -m "describe the change"
git commit --amend --no-edit          # add to last commit, keep message
git commit --amend -m "new message"
git status
git diff --cached                   # what will be committed
```

## Mistakes to Avoid
> [!WARNING]
> **Commit only stages what you added** — `git commit` does not pick up unstaged edits.

| Symptom | Check | Fix |
|---------|-------|-----|
| Nothing to commit | `git status`; unstaged changes | `git add` first |
| Commit rejected (hook) | `.git/hooks/pre-commit` output | Fix hook failure or `--no-verify` only if policy allows |
| Wrong files committed | `git show --stat HEAD` | `git reset --soft HEAD~1` then re-stage |
| Author/email wrong | `git config user.name`; `git config user.email` | Set locally or globally before commit |

## Pros/Cons or Trade-offs
- Do not commit secrets, build artifacts, or `.env` files — use `.gitignore`.
