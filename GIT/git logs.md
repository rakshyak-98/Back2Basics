[[git command]] [[git diff]] [[git blame]] [[git branch]]

# Git log

> One-line: traverse commit DAG — file history, ranges, merge-aware views, and formatted output for audits and bisect prep.

## Mental model

`git log` walks commits reachable from refs, newest first by default. Ranges use **double-dot** `A..B` = commits reachable from B not from A (merge-base relative). **Path filter** limits to commits touching files.

```
git log main..feature     commits on feature not in main
git log -p file.js        patches per commit for file
git show <sha>            one commit detail
```

For merge commits, default log may hide individual parents — use `-m` or `--first-parent` depending on question.

## Standard config / commands

### Basics

```bash
git log --oneline -20
git log --graph --oneline --decorate --all
git log -5 --stat
```

### File history with patches

```bash
git log -p -- path/to/file
git log --follow -p -- renamed_file   # track renames
```

### Range between commits

```bash
git log abc123..def456
git log -p abc123..def456
git log main..HEAD --author="Ada"
```

### Merge commit as normal commits

```bash
git log -m --name-only -1 merge_commit_sha
```

### Files changed in commit

```bash
git show --name-only --pretty=format: merge_commit_sha
git diff --name-only --cached          # staged
git diff --name-only HEAD~1..HEAD
```

### Search messages / content

```bash
git log --grep="fix login" -i
git log -S "functionName" -- path/     # pickaxe: added/removed string
git log -G "regex" -- path/
```

### Format placeholders

```bash
git log --pretty=format:"%h - %an (%ar): %s"
```

See [[git formating]] for full placeholder table.

### Since/until

```bash
git log --since="2025-01-01" --until="2025-06-01"
git log --after="2 weeks ago"
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Empty range | Reversed or equal SHAs | Swap order; verify merge-base |
| Missing commits on branch | Not reachable from ref | Log from correct branch; `--all` |
| File history stops at rename | No `--follow` | Add `--follow` |
| Merge commit shows no files | Need `-m` | `git log -m -1 merge_sha` |
| Huge slow log | Entire repo history | Narrow path/date; `--oneline` |
| Wrong author in audit | Author vs committer | `%an` vs `%cn` in format |

## Gotchas

> [!WARNING]
> **`A..B` dot is mandatory** — three-dot `A...B` is symmetric difference (different question).

> [!WARNING]
> **Shallow clone** — history truncated; log may end early; `git fetch --unshallow`.

> [!WARNING]
> **Rebase rewrites SHAs** — old SHAs from tickets may not exist locally.

## When NOT to use

- **Working tree diff** — use [[git diff]] for unstaged/staged changes.
- **Find introducing bug** — prefer `git bisect` over manual log scroll.

## Related

[[git command]] [[git formating]] [[git diff]] [[git blame]] [[git branch]]
