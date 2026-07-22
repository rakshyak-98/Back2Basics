[[NodeJS]] [[npm command]] [[nvm]] [[node environment configuration]]

# package.json

> One-line: project manifest — scripts, dependency graph, engine constraints, and module type; enforce Node/npm versions in CI and prod.

## Mental model

`package.json` is npm's contract with the repo: **dependencies** (runtime), **devDependencies** (build/test), **scripts** (automation entrypoints), **engines** (supported Node/npm), and **type** (`module` vs CommonJS default).

```
package.json
├── scripts.start  → npm run start → node dist/server.js
├── engines.node   → warn/fail install if mismatch
├── dependencies   → locked by package-lock.json
└── "type":"module" → .js files are ESM
```

Lockfile (`package-lock.json` or `pnpm-lock.yaml`) is source of truth for reproducible installs — commit it.

## Standard config / commands

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

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Works locally, fails CI Node version | `engines` vs runner | Align `.nvmrc`, Docker, setup-node |
| `ERR_REQUIRE_ESM` | `"type":"module"` | Consistent ESM or use `.cjs` |
| Phantom dependency | Import pkg not in dependencies | Add explicit dep; enable lint rule |
| Script not found | Typo in scripts | `npm run` lists available |
| Publish too large | Missing `files` | Add `"files": ["dist"]` |
| Lockfile drift | Manual package.json edit | Regenerate lock with install |

## Gotchas

> [!WARNING]
> **`engine-strict` only affects npm install** — runtime still needs ops to pin Node (Docker/systemd).

> [!WARNING]
> **Caret ranges in prod** — lockfile pins; don't delete lock in deploy.

> [!WARNING]
> **`"type":"module"` breaks require()** in `.js` files — rename CJS to `.cjs` if mixed.

## When NOT to use

- **Monorepo workspace root** — use workspaces field; per-package manifests in packages/*.
- **Application secrets** — never put secrets in package.json; use env/secret manager.

## Related

[[npm command]] [[nvm]] [[node command]] [[node environment configuration]] [[Release cycle]]
