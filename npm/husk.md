[[git hook]] [[git commit]] [[node package json]] [[npm script]] [[Jenkins]] [[Docker compose]]

# Husky

> Tiny bridge from npm install to Git hooks — installs scripts under `.husky/` so pre-commit and pre-push gates run before code leaves a laptop.

```txt
        Husky ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers ask about Husky to separate *local* quality gates from *remote* …

## Sources
- [Husky documentation](https://typicode.github.io/husky/) — deep-dive
- [lint-staged documentation](https://github.com/lint-staged/lint-staged) — overview
- [Git Hooks documentation](https://git-scm.com/docs/githooks) — deep-dive

## Key Concepts
- **Hook scripts in the repository:** `.husky/pre-commit` is versioned → every clone gets the same gates after `pre…
- **`prepare` script:** runs after `npm install` / `npm ci` → installs hooks for that developer machi…
- **lint-staged:** run ESLint/Prettier only on staged files → keeps commits fast.
- **Not a continuous integration replacement:** `--no-verify` and disabled hooks skip local gates → remote required checks re…
- **Hook choice:** pre-commit for fast checks; pre-push or CI for slow tests and builds.


- **Core:** Husky (this vault file is `husk.md`) configures Git’s `core.hooksPath` (or in…

## Technical Details
```txt
git commit
  → .husky/pre-commit
      → lint-staged (changed files)
  → commit proceeds or aborts
```

| Hook | Typical gate |
|------|--------------|
| **pre-commit** | ESLint, Prettier, typecheck staged files |
| **commit-msg** | Conventional Commits / ticket-id regex |
| **pre-push** | unit tests, build, secret scan |
| **prepare** (npm script) | `husky` — install hooks after install |

### Install (Husky 9)

```shell
npm install -D husky
npm pkg set scripts.prepare="husky"
npm run prepare
npx husky init
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
HUSKY=2 git commit -m "test"    # verbose husky logging
git config core.hooksPath       # expect .husky when configured
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Hooks never run | `.git/hooks` / `core.hooksPath` | Re-run `npm run prepare`; commit `.husky/` |
| `husky` not found | `HUSKY=0` in environment | Unset locally; CI may set intentionally |
| Wrong Node in hook | PATH inside hook | Use version-manager shims in the hook script |
| `^M` / bash `\r` | CRLF in `.husky/*` | Force LF for hook scripts |
| Slow commits | Full suite in pre-commit | Move heavy tests to pre-push or CI |
| `prepare` skipped | `npm ci --ignore-scripts` | Document manual `npm run prepare` |

## Mistakes to Avoid
- **Mistake:** Making `--no-verify` a team habit instead of fixing slow or flak…
- **Mistake:** Putting heavy integration tests in pre-commit
- **Mistake:** Shipping a library whose `prepare` runs Husky for *consumers* of…

## Pros/Cons or Trade-offs
- **Pro:** Fast feedback on the developer machine; shared hook scripts in Git.
- **Con:** Easy to bypass with `--no-verify` or `HUSKY=0`.
- **Con:** Docker-only workflows run Git on the host — tool versions must still match.

## Comparison
- vs bare [[git hook]]: Husky standardizes install via npm `prepare` for Node projects.
- vs [[Jenkins]] / GitHub Actions: remote CI is authoritative; Husky is an optional accelerator.


### Use cases
- Teams block formatting and lint errors before review, and enforce Conventiona…

- **Example:** `pre-commit` runs lint-staged
