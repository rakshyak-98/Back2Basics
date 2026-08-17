[[git]] [[git command]] [[git branch]] [[git merge]] [[git submodule]]

# Git Worktree

> multiple checked-out directories sharing one `.git` object store — review PR and hotfix in parallel without stash churn.

```txt
        Git Worktree ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Interview Relevance
- **Interview probes:** Interviewers use `Git Worktree` to check real Git fluency under pressure

## Sources
- [Pro Git book](https://git-scm.com/book/en/v2) — deep-dive
- [Git reference documentation](https://git-scm.com/docs) — overview

## Key Concepts
```
repo/.git/          ← bare or main git dir
repo/               ← worktree 1 (main)
../repo-feature/    ← worktree 2 (feature branch)
../repo-hotfix/     ← worktree 3 (detached at tag)
```

- **Note:** Switching branches in a worktree only updates that directory's files

## Technical Details
```bash
# Create worktree for existing branch
git worktree add ../project-feature feature-branch

# Create branch + worktree in one step
git worktree add -b fix/login-bug ../project-hotfix main

# Detached HEAD at specific commit (code review)
git worktree add --detach ../project-review abc1234

# List worktrees
git worktree list

# Remove worktree (must be clean or forced)
git worktree remove ../project-feature
git worktree remove --force ../project-dirty

# Prune stale registration
git worktree prune
```

- Each linked worktree stores a `.git` **file** (not dir) pointing at main repo…

### Typical workflow

```bash
# Terminal 1 — main development
cd ~/project && git switch main

# Terminal 2 — urgent hotfix
git worktree add -b hotfix/ CVE-2024 ../project-hotfix main
cd ../project-hotfix
# fix, commit, push
git worktree remove ../project-hotfix
```

## Mistakes to Avoid
> [!WARNING]
> **Same branch in two worktrees is forbidden** — Git prevents index corruption. Create a temp branch or use detached HEAD.

> [!WARNING]
> **Shared refs** — commit in one worktree instantly visible to others via `git log`; push from either.

> [!WARNING]
> **IDE lock files** — two worktrees of same repo confuse some tools; use separate IDE windows/paths.

> [!WARNING]
> **CI doesn't know about local worktrees** — pattern is dev-machine only unless CI explicitly uses it.

| Symptom | Check | Fix |
|---------|-------|-----|
| "branch already checked out" | `git worktree list` | One branch per worktree max; use detached or different branch |
| Worktree dir deleted manually | `git worktree list` shows prunable | `git worktree prune` |
| Can't remove — dirty tree | `git status` in worktree | Commit, stash, or `--force` remove |
| Submodule confusion | Each worktree needs `submodule update` | Run in each checkout separately |
| Disk looks duplicated | Shared objects | Normal — only working files duplicate |

## Pros/Cons or Trade-offs
- **Long-term second clone needs**
- **Replacing `git stash`** for tiny context switches
