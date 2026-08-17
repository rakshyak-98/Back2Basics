[[NodeJS]] [[npm command]] [[nvm]] [[node environment configuration]] [[node command]] [[Release cycle]]

# package.json

> package.json — npm's contract with the repo: dependencies (runtime), devDependencies (build/test), scripts (automation entrypoints), engines (supported Node/npm), and type (module vs CommonJS default).





## Interview Relevance
Interviewers probe **package.json** to see if you understand what it does operationally and when it is the wrong tool — not just the definition.

## Sources
- [npm — package.json](https://docs.npmjs.com/cli/v10/configuring-npm/package-json) — deep-dive
- [Wikipedia — node package json](https://en.wikipedia.org/wiki/node_package_json) — overview

## Core Definition
`package.json` is npm's contract with the repository: **dependencies** (runtime), **devDependencies** (build/test), **scripts** (automation entrypoints), **engines** (supported Node/npm), and **type** (`module` versus CommonJS default).

## Key Concepts
- `package.json` is npm's contract with the repository: **dependencies** (runtime), **devDependencies** (build/test), **scripts** (automation entrypoints), **engines** (supported …
- Lockfile (`package-lock.json` or `pnpm-lock.yaml`) is source of truth for reproducible installs — commit it.

## Technical Details
`package.json` is npm's contract with the repository: **dependencies** (runtime), **devDependencies** (build/test), **scripts** (automation entrypoints), **engines** (supported Node/npm), and **type** (`module` versus CommonJS default).

```
package.json
├── scripts.start  → npm run start → node dist/server.js
├── engines.node   → warn/fail install if mismatch
├── dependencies   → locked by package-lock.json
└── "type":"module" → .js files are ESM
```

Lockfile (`package-lock.json` or `pnpm-lock.yaml`) is source of truth for reproducible installs — commit it.

### Minimal production manifest

```json
{
  "name": "my-service",
  "version": "1.0.0",
  "private": true,
  "type": "module",
  "engines": {
    "node": ">=22.16.0 <23",
    "npm": ">=10"
  },
  "scripts": {
    "start": "node dist/server.js",
    "build": "tsc",
    "test": "node --test",
    "lint": "eslint ."
  },
  "dependencies": {
    "express": "^4.21.0"
  },
  "devDependencies": {
    "typescript": "^5.6.0"
  }
}
```

### Enforce engines in CI/local

```ini
# .npmrc
engine-strict=true
```

```bash
npm install   # fails if node -v outside engines range
```

### Pin exact Node in ops (with nvm)

```bash
echo "22.16.0" > .nvmrc
```

### exports (package public API)

```json
{
  "exports": {
    ".": "./dist/index.js",
    "./utils": "./dist/utils.js"
  }
}
```

### Common fields

| Field | Purpose |
|-------|---------|
| `main` / `exports` | Entry when package is imported |
| `bin` | CLI commands linked on global/local install |
| `files` | Whitelist for `npm publish` |
| `overrides` | Force transitive dependency versions (npm 8+) |

## Real-World Applications
In production APIs and tooling, **node package json** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **`engine-strict` only affects npm install** — runtime still needs ops to pin Node (Docker/systemd); **Caret ranges in prod** — lockfile pins; don't delete lock in deploy.

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (package.json — npm's contract with the repo: dependencies (runtime), devDependen…).
- **Con / when not:** **Monorepo workspace root** — use workspaces field; per-package manifests in packages/*.
- **Con / when not:** **Application secrets** — never put secrets in package.json; use environment/secret manager.

## Comparison
vs [[npm command]]: know when each applies — do not treat them as interchangeable. vs [[nvm]]: know when each applies — do not treat them as interchangeable. vs [[node environment configuration]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid
- **`engine-strict` only affects npm install** — runtime still needs ops to pin Node (Docker/systemd).
- **Caret ranges in prod** — lockfile pins; don't delete lock in deploy.
- **Works locally, fails CI Node version:** check `engines` vs runner; fix: Align `.nvmrc`, Docker, setup-node
- **`ERR_REQUIRE_ESM`:** check `"type":"module"`; fix: Consistent ESM or use `.cjs`
- **Phantom dependency:** check Import pkg not in dependencies; fix: Add explicit dep; enable lint rule
- **Script not found:** check Typo in scripts; fix: `npm run` lists available
- **Publish too large:** check Missing `files`; fix: Add `"files": ["dist"]`
- **Lockfile drift:** check Manual package.json edit; fix: Regenerate lock with install
