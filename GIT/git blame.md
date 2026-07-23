[[git]] [[git rebase]] [[git error]] [[git worktree]]

# git blame

> Line-level authorship: which commit last touched each line — **forensics for regressions**, not a performance review weapon.

---

## Mental model

```txt
file.c line 42 → commit abc1234 (2024-03-01, alice) → "fix timeout"
```

`git blame` walks **blob history** backward via `git log -L` mechanics — shows **last modifying commit per line**, not who originally wrote the logic if it moved.

**Copy/move detection** (`-M`, `-C`) follows lines across files/renames — essential after refactors or you'll blame the wrong person/commit.

**Blame ≠ bug owner** — understand *why* the line exists (`git show abc1234`) before reverting.

---

## Standard config / commands

### Basic

```bash
git blame path/to/file
git blame -- path/to/file          # disambiguate from revision
git blame -L 10,40 path/to/file    # line range only
git blame --date=short path/to/file
```

### Historical blame (before refactor)

```bash
git blame <commit>^ -- path/to/file   # file at parent of commit
git blame v1.2.0 -- path/to/file      # release tag snapshot
```

### Follow renames and moves

```bash
git blame -M path/to/file              # moves within file
git blame -C path/to/file              # lines copied from other files
git blame -C -C -C path/to/file        # aggressive copy detection
git blame -w path/to/file              # ignore whitespace-only changes
git blame -w -M -C path/to/file        # combine for post-refactor forensics
```

### Find introducing commit quickly

```bash
git log -L 42,42:path/to/file --oneline
git bisect start  # when blame points to ancient huge commit
```

### Ignore cosmetic commits

```bash
# .git-blame-ignore-revs (Git 2.23+)
echo abc1234567890abcdef >> .git-blame-ignore-revs
git config blame.ignoreRevsFile .git-blame-ignore-revs
git blame path/to/file
```

### IDE / GitHub

```txt
GitHub: "Blame" button on file view
VS Code / Cursor: GitLens or built-in blame gutter
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Whole file blamed on one commit | Mass rename without `-M` | `git blame -M -C file` |
| Blame stops at unrelated commit | File rename break | `git log --follow -- file` then blame old path |
| Line shows wrong date | Author date vs committer | `git blame --date=iso`; `git show` for details |
| Ignore-revs not applied | Config path | `blame.ignoreRevsFile` in repo `.git/config` or local |
| Binary / generated file noise | Should be gitignored | Stop blaming; fix `.gitattributes` export-ignore |
| Slow on huge file | Full history | `-L` range; or blame specific commit snapshot |

---

## Gotchas

> [!WARNING]
> **Force-pushed rebased history** — blame SHAs won't match old PR discussions; use reflog on maintainer machine if still available.

> [!WARNING]
> **Generated code** (protobuf, lockfiles) — blame misleads; mark `linguist-generated` or don't review line-by-line.

> [!WARNING]
> **Cherry-pick duplicates** — same patch new SHA; blame may point at cherry-pick not original fix.

> [!WARNING]
> **Using blame in perf reviews** — incentivizes tiny commits and avoids refactors; use for incident/debug only.

---

## When NOT to use

- **Finding why code exists** — read commit message + PR + tests; blame only points to where.
- **Binary files** — meaningless line blame.
- **Before `-M/-C` on moved code** — you'll chase the wrong commit.

---

## Related

[[git rebase]] · [[git error]] · [[git worktree]] · [[git ssh config]]
