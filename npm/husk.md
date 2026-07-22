[[git command]] [[git merge]] [[node package json]] [[Jenkins]] [[Docker compose]]

# Husky (filename: husk.md)

> Git hooks manager for Node repos — enforce lint/test/format at commit/push without relying on developer memory — **Husky v9+**.

---

## Mental model

**Husky** installs scripts into `.husky/` that Git invokes on events (`pre-commit`, `pre-push`, `commit-msg`). It bridges **npm lifecycle** and **Git hooks** so CI rules run locally first — cheaper than a failed pipeline.

```txt
git commit
  → .husky/pre-commit runs
      → lint-staged (changed files only)
      → vitest --related (optional)
  → commit proceeds or aborts
```

| Hook | Typical gate |
|------|--------------|
| **pre-commit** | ESLint, Prettier, typecheck staged files |
| **commit-msg** | Conventional Commits / JIRA regex |
| **pre-push** | unit tests, build, secret scan |
| **prepare** (npm script) | `husky` — installs hooks after `npm install` |

**Not a CI replacement** — developers can `--no-verify`; branch protection + remote CI is the real gate.

---

## Standard config / commands

### Install (Husky 9)

```shell
npm install -D husky
npm pkg set scripts.prepare="husky"
npm run prepare
npx husky init                     # creates .husky/pre-commit
```

### `.husky/pre-commit`

```shell
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

npx lint-staged
```

### `package.json` + lint-staged

```json
{
  "lint-staged": {
    "*.{ts,tsx,js}": ["eslint --fix", "prettier --write"],
    "*.{json,md}": ["prettier --write"]
  }
}
```

```shell
npm i -D lint-staged
```

### Commit message lint

```shell
npm i -D @commitlint/cli @commitlint/config-conventional
echo "export default { extends: ['@commitlint/config-conventional'] };" > commitlint.config.js
npx husky add .husky/commit-msg 'npx --no -- commitlint --edit $1'
```

### Monorepo

```shell
# Run only in package with changes (nx/lerna)
npx lint-staged --cwd apps/web
# or turbo run lint --filter=[HEAD^1]
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Hooks never run | `ls -la .git/hooks/pre-commit` | Re-run `npm run prepare`; ensure Husky not disabled |
| `husky - command not found` | `HUSKY=0` in env | Unset; CI sometimes sets `HUSKY=0` intentionally |
| Hook runs but wrong Node | `which node` in hook vs shell | Use `nvm`/`fnm` shim in hook script |
| Windows line endings | `^M` / `/usr/bin/env: bash\r` | `git config core.autocrlf`; LF in `.husky/*` |
| Slow commits | Full test suite in pre-commit | Move heavy tests to pre-push or CI |
| Works locally, not for teammate | Hooks not committed | Commit `.husky/` directory to repo |
| `prepare` skipped | `npm ci --ignore-scripts` | Document; run `npm run prepare` manually |

```shell
# Debug
HUSKY=2 git commit -m "test"       # verbose husky logging
git config core.hooksPath          # should be .husky or default with husky shim
```

---

## Gotchas

> [!WARNING]
> **`--no-verify` habit** — team bypasses hooks; enforce via CI required checks.

> [!WARNING]
> **Global `HUSKY=0`** in `.bashrc` — hooks silently disabled for one engineer.

> [!WARNING]
> **lint-staged on wrong glob** — misses `.tsx` or generated files; review globs when adding languages.

> [!WARNING]
> **pre-commit formatting** — unstaged hunks confuse; lint-staged stashes/restores — rare conflicts on conflicted merges.

> [!WARNING]
> **Docker-only dev** — hooks run on host Git, not in container; align tool versions.

---

## When NOT to use

- **Non-Node repos** — use `pre-commit` framework (Python) or native `.git/hooks`.
- **Heavy integration tests in pre-commit** — wrong stage; use CI.
- **Library consumed as dependency** — don't run `prepare`/husky for npm package consumers (`prepare` should be dev-only pattern).

---

## Related

[[git command]] [[git merge]] [[node package json]] [[Jenkins]] [[Docker compose]]
