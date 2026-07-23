[[git]] [[git command]] [[git rebase]] [[git branch]]

# Git Merge

> One-line: combine branch histories with a merge commit (or fast-forward) — preview conflicts before touching shared branches.

## Mental model

Merge finds the **merge base** (common ancestor) and integrates two tips into one. Three-way merge compares base → each branch and combines changes.

```
      o---o---o  feature
     /
o---o---o---o  main
         ↑
    merge commit (2 parents) if non-FF
```

**Fast-forward:** main simply moves to feature tip — no merge commit (linear history).
**Merge commit:** `--no-ff` preserves branch topology — preferred for release merges.

---

## Standard config / commands

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

---

## Triage (when things break)

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

---

## Gotchas

> [!WARNING]
> **Merge vs rebase on shared branches:** Rebase rewrites history; merge preserves it. Don't rebase commits others have pulled.

> [!WARNING]
> **`git pull` = fetch + merge** — can create surprise merge commits. Use `git pull --rebase` if team prefers linear history.

> [!WARNING]
> **Octopus merges (3+ branches)** — rare; one conflict aborts entire merge.

> [!WARNING]
> **Renames:** Git detects renames heuristically; `-X patience` helps on big diffs.

---

## When NOT to use

- **Always linear history requirement** — rebase feature onto main, then FF merge (or squash merge via PR).
- **Integrating long-lived divergent forks** — merge is correct, but expect pain; consider subtree or rebase with coordination.

---

## Related

[[git command]] [[git rebase]] [[git diff]] [[git branch]]
