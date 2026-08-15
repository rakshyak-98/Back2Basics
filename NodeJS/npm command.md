[[NodeJS]] [[node package json]] [[Packages/npm packages]] [[nvm]]

# npm command

> CLI for install, scripts, and registry — `--` separates npm’s flags from your script’s flags.

## Interview Relevance

Interviewers use **npm command** to check whether you can explain the mechanism in plain words and apply it under failure. Expect follow-ups on **`--`**, **npm ci**, **dedupe / outdated**.

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

## Real-World Applications

In production APIs and tooling, **npm command** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **`npm upgrade` vs lockfile** — know whether you intend to bump ranges; **Global `-g` installs** — avoid for app deps; pin in the project.

## Pros/Cons or Trade-offs

- **Pro:** Solves the job described above when used in the right layer (CLI for install, scripts, and registry — `--` separates npm’s flags from your sc…).
- **Con / when not:** **Other package managers** — pnpm/yarn if the repository standard says so; don’t mix casually.

## Comparison

vs [[node package json]]: know when each applies — do not treat them as interchangeable. vs [[Packages/npm packages]]: know when each applies — do not treat them as interchangeable. vs [[nvm]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid

- **`npm upgrade` vs lockfile** — know whether you intend to bump ranges.
- **Global `-g` installs** — avoid for app deps; pin in the project.
- **Script ignores flags:** check Missing `--`; fix: `npm run x -- --flag`
- **CI drift:** check Used `npm i`; fix: Use `npm ci`
- **Phantom deps:** check Import without declare; fix: Add to package.json
- **Corrupt cache:** check Weird ENOENT; fix: `npm cache clean --force`
