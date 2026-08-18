[[NodeJS]] [[node package json]] [[Packages/npm packages]]

# npm command

> CLI for install, scripts, and registry — `--` separates npm’s flags from your script’s flags.

## Mental model

**Say it in one breath:** `npm install` resolves the tree into `node_modules` + lockfile; `npm run` executes `package.json` scripts; `npm ci` is the clean CI install from the lockfile.

```txt
package.json + lockfile ──npm ci──► node_modules
npm run start -- --port 4000  →  script gets --port
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **`--`** | End of npm args | “Pass flags through to the script.” |
| --- | --- | --- |
| **npm ci** | Clean lockfile install | “Reproducible CI; deletes node_modules.” |
| **dedupe / outdated** | Tree hygiene | “Find duplicates and stale ranges.” |

## Standard config / commands

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

| lockfile | Reproducible builds |
| --- | --- |
| `--save-exact` | Pin versions |
| `npm ci` vs `install` | CI vs local tinkering |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Script ignores flags | Missing `--` | `npm run x -- --flag` |
| CI drift | Used `npm i` | Use `npm ci` |
| Phantom deps | Import without declare | Add to package.json |
| Corrupt cache | Weird ENOENT | `npm cache clean --force` |

## Gotchas

> [!WARNING]
> **`npm upgrade` vs lockfile** — know whether you intend to bump ranges.

> [!WARNING]
> **Global `-g` installs** — avoid for app deps; pin in the project.

## When NOT to use

- **Other package managers** — pnpm/yarn if the repository standard says so; don’t mix casually.

## Related

[[node package json]] [[Packages/npm packages]] [[nvm]]
