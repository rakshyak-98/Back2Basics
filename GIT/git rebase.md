[[git error]] [[git worktree]] [[git ssh configuration]] [[INDEX]] [[git blame]] [[Terraform workflow]]

# git rebase

> Replay your commits on top of a moving base — linear history without merge commits — **Pro Git (Chacon)**; dangerous on shared branches without agreement.

```txt
        git rebase ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Why It Matters
- **Key signal:** Rebase reviews check the golden rule (do not rewrite shared history), ours…

## Sources
- [Pro Git — Rewriting History](https://git-scm.com/book/en/v2/Git-Tools-Rewriting-History) — deep-dive
- [git-rebase documentation](https://git-scm.com/docs/git-rebase) — overview

## Key Concepts
```txt
              └──x──y  (your branch)

After rebase onto main:
         main ──A──B──C──x'──y'
```

- **Note:** **Rebase** copies each commit as a new hash (`x'`, `y'`) with updated parent

- **Note:** **versus merge:** merge preserves branch topology + merge commit

- **Note:** **Golden rule:** never rebase commits **already pushed** that others may have…

## Technical Details
### Daily update (feature branch)

```bash
git fetch origin
git rebase origin/main
# or: git pull --rebase origin main   # fetch + rebase current branch
```

### Interactive rebase (squash, reorder, edit)

```bash
git rebase -i origin/main
# pick / squash / fixup / edit / drop commits in editor
```

### After conflict

```bash
# Fix files, then:
git add path/to/fixed
git rebase --continue

# Abort and return to pre-rebase state
git rebase --abort

# Skip one commit (rare — know why)
git rebase --skip
```

### Conflict: keep upstream vs yours

```bash
git checkout --ours path/file    # keep version from branch you rebased ONTO (upstream)
git checkout --theirs path/file  # keep YOUR branch's version during rebase (counterintuitive!)
git add path/file
git rebase --continue
```

> During rebase, **"ours" = upstream base**, **"theirs" = your replayed commit** — opposite of merge.

### Push rebased branch

```bash
git push --force-with-lease origin feature/my-branch
# --force-with-lease refuses if remote moved unexpectedly (safer than --force)
```

### Autosquash fixups

```bash
git commit --fixup abc1234
git rebase -i --autosquash origin/main
```

## Mistakes to Avoid
> [!WARNING]
> **Rebase rewrites SHAs** — open PRs with review comments on old commits become confusing; notify reviewers after force-push.

> [!WARNING]
> **`--force-with-lease` is not magic** — stale lease if you fetch without updating tracking ref; fetch immediately before push.

> [!WARNING]
> **Merge commits in feature branch** — default rebase may flatten oddly; use `-r` (rebase merges) or avoid merge commits on feature branches.

> [!WARNING]
> **Signed commits** — replay may need re-signing depending on GPG hook config.

| Symptom | Check | Fix |
|---------|-------|-----|
| Same conflict every commit | Repeated touch of file | `git rebase -i` → squash; or merge once instead |
| "Cannot rebase: unstaged changes" | `git status` | Stash (`git stash -u`) or commit WIP |
| Lost commits after abort | `git reflog` | `git reset --hard HEAD@{n}` to pre-rebase entry |
| Force push rejected | Teammate pushed | Fetch; coordinate; never `--force` main |
| Empty commit skipped | Already applied patch | `git rebase --skip` or `--keep-empty` |
| Wrong file kept in conflict | ours/theirs confusion | Re-read labels; re-run conflict resolution |
| CI fails only after rebase | Hidden dependency on old base | Run tests locally on rebased branch before push |

## Pros/Cons or Trade-offs
- **Shared long-lived branch** multiple people commit to
- **Integrating released tags** — don't rewrite history consumers depend on.
- **You need true merge context**
