[[NodeJS]] [[node package json]] [[Packages/npm packages]] [[nvm]]

# npm command

> CLI for install, scripts, and registry — `--` separates npm’s flags from your script’s flags.

```txt
        npm command ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers use **npm command** to check whether you can explain the mechani…

## Sources
- [npm — CLI commands](https://docs.npmjs.com/cli/v10/commands) — deep-dive
- [Wikipedia — npm command](https://en.wikipedia.org/wiki/npm_command) — overview

## Key Concepts
- **`--`:** End of npm args — Pass flags through to the script.
- **npm ci:** Clean lockfile install — Reproducible CI; deletes node_modules.
- **dedupe / outdated:** Tree hygiene — Find duplicates and stale ranges.

## Technical Details
```txt
package.json + lockfile ──npm ci──► node_modules
npm run start -- --port 4000  →  script gets --port
```

```bash
npm install pkg@1.2.3
npm install pkg --save-exact
npm ci
npm update pkg
npm outdated
npm dedupe
npm run start -- --port 4000
npm view pkg version
npm explain pkg
npm config list
npm cache clean --force
```

| Knob | Why it matters |
|------|----------------|
| lockfile | Reproducible builds |
| `--save-exact` | Pin versions |
| `npm ci` vs `install` | CI vs local tinkering |

### Quick reference

| Task | Command |
|------|---------|
| … | `…` |

### Options and flags

| Flag | Effect | When to use |
|------|--------|-------------|
| … | … | … |

### Examples

```bash
```

## Mistakes to Avoid
- **Mistake:** **`npm upgrade` vs lockfile**
- **Mistake:** **Global `-g` installs** — avoid for app deps; pin in the project
- **Mistake:** **Script ignores flags:** check Missing `--`
- **Mistake:** **CI drift:** check Used `npm i`; fix: Use `npm ci`
- **Mistake:** **Phantom deps:** check Import without declare
- **Mistake:** **Corrupt cache:** check Weird ENOENT

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (CLI for install, scripts, and registry — `--` separates npm’s flags from your sc…).
- **Con / when not:** **Other package managers**

## Comparison
- vs [[node package json]]: know when each applies


### Use cases
- In production APIs and tooling, **npm command** shows up whenever teams ship …
