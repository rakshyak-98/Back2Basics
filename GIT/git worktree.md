[[git]] [[git command]] [[git branch]]

# Git Worktree

> One-line: multiple checked-out directories sharing one `.git` object store — review PR and hotfix in parallel without stash churn.

## Mental model

One repository, many **working trees**. Each worktree has its own index and working directory but shares objects, refs, and config.

```
repo/.git/          ← bare or main git dir
repo/               ← worktree 1 (main)
../repo-feature/    ← worktree 2 (feature branch)
../repo-hotfix/     ← worktree 3 (detached at tag)
```

Switching branches in a worktree only updates that directory's files — no full checkout dance, no stashing WIP on the other branch.

---

## Standard config / commands

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

Each linked worktree stores a `.git` **file** (not dir) pointing at main repo: `gitdir: /path/to/main/.git/worktrees/feature`.

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

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| "branch already checked out" | `git worktree list` | One branch per worktree max; use detached or different branch |
| Worktree dir deleted manually | `git worktree list` shows prunable | `git worktree prune` |
| Can't remove — dirty tree | `git status` in worktree | Commit, stash, or `--force` remove |
| Submodule confusion | Each worktree needs `submodule update` | Run in each checkout separately |
| Disk looks duplicated | Shared objects | Normal — only working files duplicate |

---

## Gotchas

> [!WARNING]
> **Same branch in two worktrees is forbidden** — Git prevents index corruption. Create a temp branch or use detached HEAD.

> [!WARNING]
> **Shared refs** — commit in one worktree instantly visible to others via `git log`; push from either.

> [!WARNING]
> **IDE lock files** — two worktrees of same repo confuse some tools; use separate IDE windows/paths.

> [!WARNING]
> **CI doesn't know about local worktrees** — pattern is dev-machine only unless CI explicitly uses it.

---

## When NOT to use

- **Long-term second clone needs** — separate clone is simpler if you want different remotes or hooks.
- **Replacing `git stash`** for tiny context switches — stash is lighter for 5-minute detours.

---

## Related

[[git command]] [[git branch]] [[git merge]] [[git submodule]]
