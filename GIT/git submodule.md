[[git]] [[git command]] [[git branch]]

# Git Submodule

> One-line: pin another repo at a specific commit inside your repo — powerful for vendoring, painful if treated like a shortcut for package management.

## Mental model

A submodule is a **gitlink**: parent repo records a path + exact commit SHA of nested repo. Cloning parent does not auto-fetch submodule contents unless `--recurse-submodules`.

```
parent-repo/
  vendor/lib/     → commit abc1234 of github.com/org/lib
  .gitmodules     → URL + path mapping
```

Parent tracks **pointer**, not submodule files directly.

---

## Standard config / commands

### Clone with submodules

```bash
git clone --recurse-submodules <url>

# Already cloned without submodules
git submodule update --init --recursive
```

### Add submodule

```bash
git submodule add https://github.com/org/lib.git vendor/lib
git commit -m "Add lib submodule at v2.1.0"
```

Creates `.gitmodules` + gitlink entry.

### Day-to-day updates

```bash
git submodule status                  # + = dirty, - = not init, space = clean at pinned SHA
cd vendor/lib && git fetch && git checkout v2.2.0
cd ../.. && git add vendor/lib && git commit -m "Bump lib to v2.2.0"

# Pull latest remote default branch for all submodules
git submodule update --remote --merge
```

### Convert existing directory to submodule

```bash
# Remove tracked content (backup first!)
git rm -r vendor/lib
git submodule add <url> vendor/lib
```

### Remove submodule completely

```bash
git submodule deinit -f -- vendor/lib
git rm -f vendor/lib
rm -rf .git/modules/vendor/lib
git commit -m "Remove lib submodule"
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Empty directory after clone | Submodule not initialized | `git submodule update --init --recursive` |
| "modified content" in `git status` | Submodule on different commit than pinned | Commit new SHA in parent or reset submodule |
| Detached HEAD in submodule | Normal after update | Checkout branch inside submodule or stay detached at tag |
| Push rejected from submodule | Submodule has own remote | `cd submodule && git push` then update parent pointer |
| CI checkout missing files | CI didn't init submodules | `submodules: recursive` in GitHub Actions / `GIT_SUBMODULE_STRATEGY` |
| Merge conflict on gitlink | Both sides bumped submodule | Pick correct SHA, `git add path` |

```bash
# See what commit parent expects vs what is checked out
git diff vendor/lib
git submodule foreach 'git rev-parse HEAD'
```

---

## Gotchas

> [!WARNING]
> **Detached HEAD is default** inside submodule — easy to commit locally and forget to push submodule remote before updating parent.

> [!WARNING]
> **`git pull` in parent doesn't update submodule working tree** — run `git submodule update` after pull.

> [!WARNING]
> **Recursive submodules** — nested submodules multiply pain; prefer monorepo or package registry when possible.

> [!WARNING]
> **Renaming path** — edit `.gitmodules` AND `git mv`; run `git submodule sync`.

---

## When NOT to use

- **npm/cargo/go modules exist** — use proper package manager unless you need to fork/patch at source level.
- **Teams unfamiliar with gitlinks** — onboarding cost exceeds benefit for app repos.

---

## Related

[[git command]] [[git worktree]] [[git merge]]
