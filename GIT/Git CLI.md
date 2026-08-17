[[Git CLI]] [[INDEX]]

# GIT CLI

> Git CLI — recovery, bisect, merge dry-runs, and everyday workflow commands.

---

## Git CLI

From [[Git CLI]].

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

```bash
# …
```
