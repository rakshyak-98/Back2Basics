[[git]] [[git command]] [[git commit]]

# Git Hooks

> One-line: scripts Git runs at lifecycle events — enforce quality locally (pre-commit) or gate pushes (pre-push); server-side hooks live on the remote.

## Mental model

Hooks are executable scripts in `.git/hooks/` (or managed via tools). Client hooks run on **your** machine; server-side hooks run on receive (GitHub/GitLab use their own hook systems — not raw `.git/hooks` on server for hosted SaaS).

```
git commit  →  pre-commit → commit-msg → post-commit
git push    →  pre-push → (remote) pre-receive / update / post-receive
```

Exit non-zero from a hook **blocks** the operation.

---

## Standard config / commands

### Built-in sample hooks

```bash
ls .git/hooks/
# *.sample files — rename and chmod +x to activate
cp .git/hooks/pre-commit.sample .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

### Modern approach: `core.hooksPath` + framework

```bash
# Point all repos at shared hooks (optional global)
git config --global core.hooksPath ~/.githooks
mkdir -p ~/.githooks

# Or use husky / lefthook / pre-commit (Python) in repo
npx husky init
echo "npm test" > .husky/pre-commit
chmod +x .husky/pre-commit
git config core.hooksPath .husky
```

### Useful hook scripts

**pre-commit** — lint staged files only:

```bash
#!/bin/sh
npm run lint-staged || exit 1
```

**commit-msg** — enforce Conventional Commits:

```bash
#!/bin/sh
commit_msg_file=$1
grep -qE '^(feat|fix|docs|chore)(\(.+\))?: .+' "$commit_msg_file" || {
  echo "Commit message must match Conventional Commits"
  exit 1
}
```

**pre-push** — block force-push to main:

```bash
#!/bin/sh
while read local_ref local_sha remote_ref remote_sha; do
  if [ "$remote_ref" = "refs/heads/main" ]; then
    if [ "$local_sha" = "0000000000000000000000000000000000000000" ]; then
      continue
    fi
    # reject non-FF push (simplified)
    merge_base=$(git merge-base "$local_sha" "$remote_sha")
    [ "$merge_base" = "$remote_sha" ] || { echo "Non-FF push to main blocked"; exit 1; }
  fi
done
```

### Bypass (emergency only)

```bash
git commit --no-verify
git push --no-verify
```

Document when bypass is acceptable (hotfix with failing unrelated test).

---

## Common hooks reference

| Hook | Trigger | Typical use |
|------|---------|-------------|
| `pre-commit` | Before commit recorded | Lint, format, secrets scan |
| `commit-msg` | After message entered | Message format, ticket ID |
| `pre-push` | Before push | Run tests, block protected branches |
| `post-merge` | After merge | `npm install` if lockfile changed |
| `pre-rebase` | Before rebase | Prevent rebase onto wrong branch |

Server-side (self-hosted bare repo): `pre-receive`, `update`, `post-receive`.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Commit silently slow | Hook running full test suite | Scope to staged files; move heavy checks to CI/pre-push |
| Hook not running | `ls -la .git/hooks/pre-commit` | Must be executable; verify `core.hooksPath` |
| Works locally, not for teammate | Hooks not in repo | Commit husky/lefthook config; hooks aren't cloned from `.git/hooks` |
| CI passes, pre-commit fails | Different Node/Python version | Pin versions in `.tool-versions` / `engines` |
| `--no-verify` abuse | Audit culture | Protected branches on remote + required checks |

---

## Gotchas

> [!WARNING]
> **`.git/hooks` is not versioned** — use husky, lefthook, or `core.hooksPath` to share hooks via repo.

> [!WARNING]
> **Windows line endings** — shebang scripts need LF; `CRLF` breaks `#!/bin/sh`.

> [!WARNING]
> **Hooks don't run on `git commit --amend`** inconsistently across versions — test amend path.

> [!WARNING]
> **Secret scanners in pre-commit** — can false-positive on test fixtures; tune allowlists.

---

## When NOT to use

- **Heavy integration tests in pre-commit** — belongs in CI; local hook should stay under ~10s.
- **Security-only on client hooks** — attacker can bypass; enforce on server/PR checks.

---

## Related

[[git command]] [[git commit]] [[git commit template]] [[gpg sign]]
