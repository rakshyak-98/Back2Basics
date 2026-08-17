[[GIT]]

# git diff

> git diff — show unstaged, staged, or commit-to-commit file changes.

```txt
        git diff ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Why It Matters
- **Key signal:** Diff questions check staged vs unstaged, word-diff, and reading patches in re…

## Sources
- [Pro Git book](https://git-scm.com/book/en/v2) — deep-dive
- [Git reference documentation](https://git-scm.com/docs) — overview

## Key Concepts
```bash
git diff --name-only;
git diff --cached --name-only;
git diff main.. --name-only;
git diff --name-status;
```
- **compare one:** compare one file between two branches
```bash
git diff branch1 branch2 -- <file path>;
```
```bash
git diff --stat
git diff --shortstat
```
```bash
git diff --cached;
git diff --staged;
git diff HEAD;
git diff HEAD~1 HEAD;
git diff main...HEAD;
git diff main..feature;
```
```bash
git diff v1.2.3 v1.3.0 --name-only;
git diff abc123..def456;
git diff --since="2 days ago" --name-only;
```
### Filter by path/pattern
```bash
git diff -- src/;
git diff -- '*.js' '*.ts' '*.tsx';
git diff -- . ':!node_modules';
git diff --diff-filter=R --name-only;
```

## Technical Details
```bash
git diff                            # unstaged changes
git diff --cached                   # staged changes
git diff HEAD                       # staged + unstaged
git diff main..feature              # commits on feature not on main
git diff branch1 branch2 -- path/   # one file between branches
git diff --stat
```

## Mistakes to Avoid
> [!WARNING]
> `git diff` without flags shows **working tree versus index** — not last commit.

| Symptom | Check | Fix |
|---------|-------|-----|
| Empty diff but file changed | Line endings / assume-unchanged | `git diff --ignore-cr-at-eol`; `git update-index` |
| Diff shows whole file | File mode or encoding flip | Check `core.filemode`; normalize encoding |
| Cannot diff binary | Expected for images/binaries | `git diff --numstat`; use external diff tool |
| Wrong comparison range | `..` versus `...` syntax | `A..B` = reachable from B not A; `A...B` = symmetric difference since merge base |

## Pros/Cons or Trade-offs
- Do not rely on diff alone for merge conflict resolution
