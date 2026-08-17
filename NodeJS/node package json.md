[[NodeJS]] [[NodeJS CLI]] [[nvm]] [[node environment configuration]] [[NodeJS CLI]] [[Release cycle]]

# package.json

> package.json — npm's contract with the repo: dependencies (runtime), devDependencies (build/test), scripts (automation entrypoints), engines (supported Node/npm), and type (module vs CommonJS default).

```txt
        package.json ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers probe **package.json** to see if you understand what it does ope…

## Sources
- [npm — package.json](https://docs.npmjs.com/cli/v10/configuring-npm/package-json) — deep-dive
- [Wikipedia — node package json](https://en.wikipedia.org/wiki/node_package_json) — overview

## Key Concepts
- **`package.json` is:** `package.json` is npm's contract with the repository: **dependencies** (runti…
- **Lockfile (`package-lock.json`:** Lockfile (`package-lock.json` or `pnpm-lock.yaml`) is source of truth for rep…


- **Core:** `package.json` is npm's contract with the repository: **dependencies** (runti…

## Technical Details
- `package.json` is npm's contract with the repository: **dependencies** (runti…

```
package.json
├── scripts.start  → npm run start → node dist/server.js
├── engines.node   → warn/fail install if mismatch
├── dependencies   → locked by package-lock.json
└── "type":"module" → .js files are ESM
```

- Lockfile (`package-lock.json` or `pnpm-lock.yaml`) is source of truth for rep…

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

## Mistakes to Avoid
- **Mistake:** **`engine-strict` only affects npm install**
- **Mistake:** **Caret ranges in prod**
- **Mistake:** **Works locally, fails CI Node version:** check `engines` vs run…
- **Mistake:** **`ERR_REQUIRE_ESM`:** check `"type":"module"`
- **Mistake:** **Phantom dependency:** check Import pkg not in dependencies
- **Mistake:** **Script not found:** check Typo in scripts
- **Mistake:** **Publish too large:** check Missing `files`
- **Mistake:** **Lockfile drift:** check Manual package.json edit

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (package.json — npm's contract with the repo: dependencies (runtime), devDependen…).
- **Con / when not:** **Monorepo workspace root**
- **Con / when not:** **Application secrets**

## Comparison
- vs [[NodeJS CLI]]: know when each applies


### Use cases
- In production APIs and tooling, **node package json** shows up whenever teams…
