[[git]] [[git merge]] [[git rebase]] [[git branch]] [[git diff]] [[git error]] [[git worktree]] [[git hook]] [[git submodule]] [[git logs]] [[git blame]]

# Git Commands — Recovery & Debug

> When history is wrong — reflog, bisect, and dry-run merge before you force-push.

```txt
        Git Commands — Rec ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Interview Relevance
- **Interview probes:** Interviewers use `Git Commands

## Sources
- [Pro Git book](https://git-scm.com/book/en/v2) — deep-dive
- [Git reference documentation](https://git-scm.com/docs) — overview

## Key Concepts
```txt
Working tree → index → commits → remote refs
                 ↑
           reflog = local undo log
```

## Technical Details
```bash
git reflog                          # find lost SHA
git reset --hard HEAD@{1}           # or: git branch recover <sha>
git revert <sha>                    # safe undo on shared main

git bisect start HEAD v1.0.0
git bisect run ./test.sh            # 0=good, 1-125=bad
git bisect reset

git merge --no-commit --no-ff other # dry-run merge
git merge --abort
git diff main...feature             # triple-dot: since diverge

git fetch --prune
git stash list && git stash apply stash@{0}
```

| Knob | Why it matters |
|------|----------------|
| Annotated tag `-a` | Release metadata |
| `ORIG_HEAD` | Quick undo after rebase/merge |
| Triple-dot `A...B` | Review / PR shape |

| Flag | Effect | When to use |
|------|--------|-------------|
| … | … | … |

```bash
# …
```

| Task | Command |
|------|---------|
| … | `…` |

## Mistakes to Avoid
> [!WARNING]
> **`git clean -fd` is irreversible** — preview with `-n`.

> [!WARNING]
> **Reflog is local** — not on the remote clone.

> [!WARNING]
> **`A...B` ≠ `A..B`** — code review usually wants triple-dot.

| Symptom | Check | Fix |
|---------|-------|-----|
| Lost after reset | `git reflog` | Reset/branch to old SHA |
| Detached HEAD | `git status` | `git switch -c keep-work` |
| Push rejected | Non-fast-forward | Rebase/merge; force only if agreed |
| When did bug land? | Bisect | `git bisect run` between good/bad |
| Conflict mess | `git ls-files -u` | Fix markers; `--continue` / `--abort` |
| Auth mid-push | credential helper | Clear helper; SSH/PAT |

## Pros/Cons or Trade-offs
- **Force-push shared main** — prefer revert.
- **Bisect on flaky tests** — script must be deterministic.
