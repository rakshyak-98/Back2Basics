[[git command]] [[git diff]] [[git merge]] [[git rebase]]

# Git patch files

> Git patch files — feature branch commits ──format-patch──► 0001-fix.patch, 0002-feat.patch

```txt
        Git patch files ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Why It Matters
- **Key signal:** Reviewers use `Git patch files` to check real Git fluency under pressure

## Sources
- [Pro Git book](https://git-scm.com/book/en/v2) — deep-dive
- [Git reference documentation](https://git-scm.com/docs) — overview

## Key Concepts
```
- **Note:** feature branch commits ──format-patch──► 0001-fix.patch, 0002-feat.patch
                                                    │
                                           git am *.patch
                                                    ▼
                                            replayed commits on target branch
```

- **Note:** Use for: mailing lists, exporting PR to air-gapped environment, carrying patc…

## Technical Details
### Export range

```bash
# All commits on branch since main
git format-patch main..feature

# Last N commits
git format-patch -3 HEAD

# Single commit
git format-patch -1 abc1234

# Include merge commits flattened (-m parent)
git format-patch -1 -m merge_commit_sha
```

### Output options

```bash
git format-patch main..HEAD -o ./patches/
git format-patch --cover-letter -n main..HEAD   # series intro
git format-patch --stdout main..HEAD > series.mbox
```

### Apply patches

```bash
git am ./patches/*.patch
git am --3way ./patches/0001-*.patch   # merge conflicts with 3-way
```

### Conflict resolution

```bash
# fix conflicts in files
git add .
git am --continue

git am --abort    # back out entire am session
git am --skip     # skip current patch
```

### Alternative: apply without committing

```bash
git apply --check patch.file
git apply patch.file
git commit -C HEAD  # after manual apply
```

## Mistakes to Avoid
> [!WARNING]
> **`git apply` vs `git am`** — apply doesn't create commit metadata; easy to lose authorship.

> [!WARNING]
> **Binary files** — patches handle small binaries; large assets need Git LFS or direct fetch.

> [!WARNING]
> **Renames** — patches can be fragile across refactors; prefer merge/cherry-pick for big moves.

| Symptom | Check | Fix |
|---------|-------|-----|
| `patch does not apply` | Base branch drift | Regenerate from common ancestor; `git am --3way` |
| Empty patch series | Wrong range `A..B` | `A..B` excludes A; use `A^..B` or verify log |
| Wrong author on applied | Used `apply` not `am` | `git am` preserves From: line |
| `corrupt patch at line` | Line endings CRLF | `git config core.autocrlf`; regenerate patch |
| Duplicate commits after am | Patches already applied | `git log`; skip or rebase --onto |
| Merge commit patch huge | Need `-m` parent | `format-patch -m -1 merge_sha` |

## Pros/Cons or Trade-offs
- **Same repository, same remote** — push branch + PR.
- **Interactive conflict-prone long series** — one merge or rebase onto target.
