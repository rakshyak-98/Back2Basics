[[git command]] [[git merge]] [[git rebase]] [[git diff]] [[git logs]] [[git worktree]]

# Git branches

> movable refs pointing at commits — track upstream, know tracking config, and debug "wrong branch" deploys with `-vv` and reflog.





## Interview Relevance
Interviewers use `Git branches` to check real Git fluency under pressure — history rewriting safety, conflict recovery, and what not to do on shared branches.

## Sources
- [Pro Git book](https://git-scm.com/book/en/v2) — deep-dive
- [Git reference documentation](https://git-scm.com/docs) — overview

## Key Concepts
```
origin/main ──► commit C
     ▲
     │ fetch
local main ───► commit C (tracking origin/main)
feature ──────► commit D (ahead 2)
```

Creating a branch is instant (new reference). **Merging/rebasing** moves history; deleting branch removes reference only, not commits until GC.

## Technical Details
### List and inspect

```bash
git branch              # local
git branch -r           # remote-tracking
git branch -a           # all
git branch -vv          # upstream + ahead/behind
```

Example `-vv`:

```txt
* main    abc1234 [origin/main] Latest commit message
  feat    def5678 [origin/feat: ahead 2, behind 1] WIP
```

### Tracking upstream

```bash
git branch -u origin/main           # set upstream current branch
git push -u origin feature          # push and set upstream
git config --get branch.$(git branch --show-current).remote
git config --get branch.$(git branch --show-current).merge
```

### Create / switch

```bash
git switch -c feature origin/main   # create from remote
git switch feature
git checkout -b hotfix main           # legacy equivalent
```

### Sync with remote

```bash
git fetch origin
git pull --rebase origin main         # preferred linear history
git status -sb                      # ## main...origin/main [ahead 1, behind 2]
```

### Delete

```bash
git branch -d feature                 # merged only
git branch -D feature                 # force
git push origin --delete feature      # remote
```

### Rename

```bash
git branch -m old-name new-name
```

## Pros/Cons or Trade-offs
- **Immutable release tags** — use annotated tags for releases, not moving branch pointers.
- **Storing unmerged WIP forever** — delete merged branches; rely on reflog short term.

## Mistakes to Avoid
> [!WARNING]
> **Local branch name ≠ remote name** — tracking config maps them; verify with `-vv`.

> [!WARNING]
> **Stale remote-tracking refs** — `git fetch --prune` after remote deletes.

> [!WARNING]
> **Long-lived branch drift** — rebase/merge main regularly to reduce conflict bomb.

| Symptom | Check | Fix |
|---------|-------|-----|
| `ahead/behind` confusion | `git fetch`; `git status -sb` | Pull/rebase; push if ahead |
| Push rejected non-ff | Remote has new commits | `git pull --rebase` then push |
| Wrong branch deployed | CI branch filter | Protect main; tag releases |
| No upstream on push | `-u` not set | `git push -u origin branch` |
| Detached HEAD | `git status` | `git switch main` or create branch at SHA |
| Branch gone after clone | Default branch only | `git fetch --all`; checkout remote branch |
