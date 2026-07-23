[[git]] [[git merge]] [[git rebase]] [[git branch]] [[git diff]] [[git error]]

# Git Commands — Recovery & Debug

> One-line: when history is wrong, refs are lost, or merges surprise you — reflog, bisect, and dry-run merge before you force-push.

## Mental model

Git stores a DAG of commits; **refs** (branches, tags, HEAD) are movable pointers. `git reflog` records where refs *were* — your safety net after bad reset/rebase. Recovery is almost always possible until garbage collection (`gc`) prunes unreachable objects (~90 days default).

```
Working tree → index (staging) → local commits → remote refs
                     ↑
              reflog remembers HEAD@{n} even after "lost" commits
```

---

## Standard config / commands

### Starter identity

```bash
git config user.name "Your Name"
git config user.email "you@example.com"
git config init.defaultBranch main
git config --global --unset credential.helper   # clear cached creds if switching accounts
```

### Credential helpers (debug auth)

```bash
git config --show-origin credential.helper
git config --global credential.helper
git config --system credential.helper
git config --local credential.helper
```

---

## Recovery playbook

### Reflog — find lost commits

```bash
git reflog                          # HEAD history
git reflog show feature-branch      # branch-specific
git log -g --oneline -10            # same idea, compact

# Recover "lost" commit after bad reset
git reset --hard abc1234            # from reflog entry
git cherry-pick abc1234             # or apply onto current branch
git branch recovered-work abc1234     # save without moving HEAD
```

| When | Command |
|------|---------|
| "I reset --hard and lost work" | `git reflog` → find pre-reset SHA → `git reset --hard HEAD@{1}` |
| "Rebase went wrong" | `git reflog` → `git reset --hard ORIG_HEAD` or specific entry |
| "Deleted branch" | `git reflog` or `git fsck --lost-found` → recreate branch at SHA |

### Undo without rewriting shared history

```bash
git revert <commit-sha>             # new commit that undoes — safe on main
git restore --staged <file>         # unstage
git restore <file>                  # discard working tree changes
git checkout -- <file>              # older syntax, same as restore
```

Avoid `git push --force` on shared branches unless team agrees.

### Stash recovery

```bash
git stash list
git stash show -p stash@{2}
git stash apply stash@{2}           # keep stash
git stash pop                       # apply + drop
git fsck --unreachable | grep commit   # last resort for dropped stash
```

---

## Bisect — find the breaking commit

```bash
git bisect start
git bisect bad                      # current HEAD is broken
git bisect good v1.0.0              # last known good tag/commit

# Git checks out middle commit — test, then:
git bisect good                     # or: git bisect bad
# repeat until culprit commit printed

git bisect reset                    # return to original branch
```

Automate with a test script:

```bash
git bisect start HEAD v1.0.0
git bisect run npm test             # exit 0 = good, 1-125 = bad, 127+ = skip
git bisect reset
```

Use for: regression after release, flaky test introduced between tags, perf cliff.

---

## Merge & conflict debug

### Preview conflicts without merging

```bash
git checkout target-branch
git merge --no-commit --no-ff source-branch   # dry-run merge
git merge --abort                               # clean up

# Or diff the merge base only
git diff target-branch...source-branch
git merge-tree $(git merge-base target-branch source-branch) target-branch source-branch
```

See [[git merge]] for merge strategies.

### Active conflict triage

```bash
git ls-files -u                     # unmerged index entries (stages 1/2/3)
git diff --name-only --diff-filter=U
git diff                            # conflict markers in working tree

# After fixing markers:
git add <resolved-files>
git merge --continue                # or rebase --continue
```

---

## Remote & ref inspection

```bash
git remote -v
git fetch --prune                   # drop stale remote-tracking branches
git remote prune origin
git branch -vv                      # upstream tracking status
git branch --set-upstream-to=origin/main my-feature
git branch --unset-upstream

git show-ref                        # all refs → SHAs (integrity check)
git show-ref --verify refs/heads/main
```

| Tool | Purpose | Scope |
|------|---------|-------|
| `git show-ref` | Where refs point now | All branches/tags |
| `git reflog` | History of ref movements | Local (HEAD, branches) |

Example `show-ref`: `abc1234 refs/heads/main`
Example `reflog`: `abc1234 HEAD@{0}: reset: moving to HEAD~1`

---

## Tags (release pointers)

```bash
git tag -l "v1.*"
git tag -a v1.0.0 -m "Release notes"
git show v1.0.0
git push origin v1.0.0
git push origin --tags

# Move tag to different commit (coordinate with team)
git tag -d v1.0.0
git tag -a v1.0.0 <new-sha> -m "Retagged"
git push origin :refs/tags/v1.0.0   # delete remote old tag
git push origin v1.0.0

git branch --contains v1.0.0
git rev-list -n 1 v1.0.0
```

Prefer **annotated tags** (`-a`) for releases — store author, date, message.

---

## Inspection & forensics

### What is tracked / deleted?

```bash
git ls-files                       # tracked in index
git status --short
git ls-tree -r HEAD --name-only    # files in last commit
git ls-tree -r <branch> --name-only

git ls-files --deleted
git diff --cached --name-only --diff-filter=D
git log --diff-filter=D --summary  # commits that deleted files
git diff --diff-filter=D main..feature
```

### Diff deep cuts

```bash
git diff main...feature             # changes on feature since diverge (triple-dot)
git diff main..feature              # symmetric diff (double-dot)
man git-diff
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| "Detached HEAD" after checkout | `git status` | `git switch -c new-branch` to keep work |
| Push rejected (non-fast-forward) | `git fetch`; `git log origin/main..HEAD` | Rebase onto remote or merge; don't force unless intentional |
| Wrong commit on main | `git reflog` | Revert commit or reset + force (if unpushed only) |
| Submodule shows modified | `git submodule status` | See [[git submodule]] |
| Auth fails mid-push | `git config credential.helper` | Clear helper; re-auth with PAT/SSH |
| Can't find when bug introduced | `git bisect run ./test.sh` | Bisect between good tag and HEAD |

---

## Gotchas

> [!WARNING]
> **`git clean -fd` is irreversible** — removes untracked files. Preview with `git clean -fdn`.

> [!WARNING]
> **Reflog is local** — not on remote. Cloned repo won't have your laptop's reflog.

> [!WARNING]
> **`git merge-tree` output is informational** — doesn't modify working tree; use for CI conflict prediction.

> [!WARNING]
> **Triple-dot vs double-dot diff** — `A...B` = changes on B since common ancestor; `A..B` = all diff between tips. Code review and merge preview usually want `...`.

---

## When NOT to use

- **`git push --force` on shared main** — use revert or a coordinated reset window.
- **Bisect on flaky tests** — script must be deterministic or bisect lies.
- **Reflog on someone else's machine** — recover from your clone or remote tags.

---

## Related

[[git merge]] [[git rebase]] [[git worktree]] [[git hook]] [[git submodule]] [[git logs]] [[git blame]]
