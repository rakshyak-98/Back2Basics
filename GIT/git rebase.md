[[git error]] [[git worktree]] [[git ssh config]] [[INDEX]]

# git rebase

> Replay your commits on top of a moving base — linear history without merge commits — **Pro Git (Chacon)**; dangerous on shared branches without agreement.

---

## Mental model

```txt
Before:  main ──A──B──C
              └──x──y  (your branch)

After rebase onto main:
         main ──A──B──C──x'──y'
```

**Rebase** copies each commit as a new hash (`x'`, `y'`) with updated parent. Old commits become unreachable (until reflog expires).

**vs merge:** merge preserves branch topology + merge commit; rebase rewrites your local work to look like it was built on latest main.

**Golden rule:** never rebase commits **already pushed** that others may have pulled — unless team explicitly uses `git pull --rebase` culture and coordinates force-push.

---

## Standard config / commands

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

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Same conflict every commit | Repeated touch of file | `git rebase -i` → squash; or merge once instead |
| "Cannot rebase: unstaged changes" | `git status` | Stash (`git stash -u`) or commit WIP |
| Lost commits after abort | `git reflog` | `git reset --hard HEAD@{n}` to pre-rebase entry |
| Force push rejected | Teammate pushed | Fetch; coordinate; never `--force` main |
| Empty commit skipped | Already applied patch | `git rebase --skip` or `--keep-empty` |
| Wrong file kept in conflict | ours/theirs confusion | Re-read labels; re-run conflict resolution |
| CI fails only after rebase | Hidden dependency on old base | Run tests locally on rebased branch before push |

---

## Gotchas

> [!WARNING]
> **Rebase rewrites SHAs** — open PRs with review comments on old commits become confusing; notify reviewers after force-push.

> [!WARNING]
> **`--force-with-lease` is not magic** — stale lease if you fetch without updating tracking ref; fetch immediately before push.

> [!WARNING]
> **Merge commits in feature branch** — default rebase may flatten oddly; use `-r` (rebase merges) or avoid merge commits on feature branches.

> [!WARNING]
> **Signed commits** — replay may need re-signing depending on GPG hook config.

---

## When NOT to use

- **Shared long-lived branch** multiple people commit to — merge or trunk-based with short branches.
- **Integrating released tags** — don't rewrite history consumers depend on.
- **You need true merge context** — complex binary conflicts sometimes easier with one merge commit.

---

## Related

[[git error]] · [[git blame]] · [[git worktree]] · [[git ssh config]] · [[Terraform workflow]]
