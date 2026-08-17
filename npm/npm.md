[[yarn]] [[pnpm cli]] [[npm script]] [[npm error]] [[node package json]] [[node modules]]

# npm

> Node’s default package manager — installs dependencies from the registry, writes a lockfile, and runs lifecycle scripts defined in `package.json`.

```txt
        npm ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers ask about npm to see whether you understand dependency trees, pe…

## Sources
- [npm Docs — About npm](https://docs.npmjs.com/about-npm) — overview
- [npm RFC 0031 — Handling peer conflicts](https://github.com/npm/rfcs/blob/main/implemented/0031-handling-peer-conflicts.md) — deep-dive
- [npm Docs — package-lock.json](https://docs.npmjs.com/cli/v10/configuring-npm/package-lock-json) — deep-dive

## Key Concepts
- **Registry + semver ranges:** `^` / `~` declare allowed versions → the lockfile pins what actually installs.
- **Peer dependencies:** a package expects the *host* project to provide a shared library (e.g
- **Lockfile vs tree:** `npm ci` installs exactly from the lockfile → preferred in continuous integra…
- **Lifecycle scripts:** `preinstall` / `install` / `postinstall` run during install → supply-chain ri…
- **Workspaces:** monorepo packages share one lockfile → hoist and link local packages.


- **Core:** npm (Node Package Manager) resolves a dependency graph from `package.json`, i…

## Technical Details
```bash
npm install                  # resolve + update lockfile as needed
npm ci                       # clean install from lockfile only
npm install lodash --save
npm install -D typescript
npm outdated
npm ls                       # dependency tree
npm why lodash               # who depends on it
npm root -g                  # global node_modules path
npm info <package> peerDependencies
```

- **Peer conflict (`ERESOLVE`):** since npm v7, conflicting `peerDependencies` …
- Prefer aligning versions or `overrides` in `package.json`

```bash
npm install --legacy-peer-deps   # ignore peer enforcement (escape hatch)
npm install --force              # override with heuristics / warnings
```

| Symptom | Likely cause |
|---------|--------------|
| `ERESOLVE unable to resolve` | Incompatible peer ranges in the tree |
| Lockfile out of sync with `package.json` | Manual edits or mixed package managers |
| Docker `COPY` fails on `node_modules` | Host/platform `node_modules` copied into image |
| Scripts fail after `npm ci --ignore-scripts` | Lifecycle hooks skipped on purpose |

## Mistakes to Avoid
- **Mistake:** Committing `node_modules` or relying on `npm install` in continu…
- **Mistake:** Treating `--legacy-peer-deps` as a permanent fix instead of reco…
- **Running two package managers in the sam…:** → version drift)

## Pros/Cons or Trade-offs
- **Pro:** Default toolchain, huge registry, mature lockfile and workspace support.
- **Con:** Nested `node_modules` can be large and slow compared with [[pnpm cli]]’s content-addressable store.
- **Con:** Mixing npm and Yarn/pnpm in one project causes lockfile drift.

## Comparison
- vs [[yarn]]: Yarn Classic/Berry emphasize deterministic installs and workspaces
- vs [[pnpm cli]]: pnpm hard-links from a global store and is stricter about phantom dependencies a…


### Use cases
- Almost every Node.js service and frontend uses npm (or a compatible client) t…

- **Example:** A React 18 app adds a UI library that peers React 17 → install f…
