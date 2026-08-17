[[git]] [[git command]] [[git rebase]] [[git branch]] [[git diff]]

# Git Merge

> combine branch histories with a merge commit (or fast-forward) — preview conflicts before touching shared branches.

```txt
        Git Merge ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Why It Matters
- **Key signal:** Reviewers use `Git Merge` to check real Git fluency under pressure

## Sources
- [Pro Git book](https://git-scm.com/book/en/v2) — deep-dive
- [Git reference documentation](https://git-scm.com/docs) — overview
- [git merge — Wikipedia](https://en.wikipedia.org/wiki/Merge_(version_control)) — overview

## Key Concepts
```
      o---o---o  feature
     /
o---o---o---o  main
         ↑
    merge commit (2 parents) if non-FF
```

- **Note:** **Fast-forward:** main simply moves to feature tip
- **Note:** **Merge commit:** `--no-ff` preserves branch topology

## Technical Details
### Basic merge

```bash
git checkout main
git pull origin main
git merge feature-branch              # FF if possible
git merge --no-ff feature-branch -m "Merge feature X"
git push origin main
```

### Dry-run / conflict preview (no commit)

```bash
git checkout main
git merge feature --no-commit --no-ff
# inspect, run tests
git merge --abort                     # discard

# Off-line conflict prediction (Git 2.38+)
git merge-tree $(git merge-base main feature) main feature
```

### Resolve conflicts

```bash
git merge feature
# CONFLICT in file.js
git diff --name-only --diff-filter=U
# edit files, remove <<<<<< markers
git add file.js
git commit                            # completes merge
# or: git merge --continue
```

### Abort

```bash
git merge --abort
```

### Merge strategies

| Strategy | When |
|----------|------|
| `recursive` (default) | Two branches, one merge base |
| `ours` | Keep our tree entirely — rare, release branch tricks |
| `theirs` | Take their tree (subtree merge contexts) |
| `-X ours` / `-X theirs` | Prefer one side on **conflicting hunks** only |

```bash
git merge -X patience feature        # better on large refactors (slow)
git merge -s ours release-hotfix     # discard their content, keep our history shape
```

### Validate two branches will conflict (without merge)

```bash
git checkout target-branch
git diff target-branch...source-branch
git merge-tree $(git merge-base target-branch source-branch) target-branch source-branch
```

## Mistakes to Avoid
> [!WARNING]
> **Merge vs rebase on shared branches:** Rebase rewrites history; merge preserves it. Don't rebase commits others have pulled.

> [!WARNING]
> **`git pull` = fetch + merge** — can create surprise merge commits. Use `git pull --rebase` if team prefers linear history.

> [!WARNING]
> **Octopus merges (3+ branches)** — rare; one conflict aborts entire merge.

> [!WARNING]
> **Renames:** Git detects renames heuristically; `-X patience` helps on big diffs.

| Symptom | Check | Fix |
|---------|-------|-----|
| Unexpected conflict on "same" file | Both sides edited same lines since base | Manual resolve; consider `git rerere` if repeats |
| Merge commit on simple feature | Default FF disabled or branch diverged | `git merge --ff-only` in CI to enforce linear |
| Lost changes after merge | `git log --merges -p` | `git revert -m 1 <merge-sha>` to revert merge commit |
| Submodule conflict | `git diff --submodule` | Enter submodule, commit there, then parent |
| Binary file conflict | `git checkout --ours\|--theirs file` | Pick one side explicitly |

### Revert a merge commit

```bash
git revert -m 1 <merge-commit-sha>    # -m 1 = keep first parent (main line)
```

## Pros/Cons or Trade-offs
- **Always linear history requirement**
- **Integrating long-lived divergent forks**
