[[npm]] [[npm error]] [[npm script]] [[yarn]] [[pnpm cli]]

# npm

> npm is Node's default package manager — it resolves dependency trees, runs lifecycle scripts, and publishes packages to the registry.

## Mental model

**Say it in one breath:** `package.json` declares direct dependencies; npm walks the graph, writes `package-lock.json`, and installs into `node_modules` — peer-dependency mismatches surface as `ERESOLVE` warnings.

```bash
npm root -g          # global node_modules location
npm ls --depth=0     # top-level deps in this project
npm outdated         # available upgrades
```

### Peer dependency conflicts

`npm warn ERESOLVE overriding peer dependency` means the resolver found a version mismatch between what a package expects and what is installed.

```shell
npm info <package> peerDependencies
npm install <compatible-package>@<version>
npm install --legacy-peer-deps   # last resort — skips strict peer resolution
```

## Standard config / commands

```bash
npm ci                 # clean install from lockfile (CI)
npm install            # update lockfile when package.json changes
npm run <script>       # runs scripts from package.json
npm publish --access public
```

| Command | When to use |
| --- | --- |
| `npm ci` | Reproducible builds; fails if lockfile out of sync |
| `npm install` | Local dev after editing `package.json` |
| `npm audit fix` | Known CVE patches (review diff first) |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| `ERESOLVE` peer conflict | `npm info <pkg> peerDependencies` | Install matching peer version or `--legacy-peer-deps` |
| Docker `COPY` fails on `node_modules` | `.dockerignore` missing | Ignore `node_modules`; run `npm ci` inside image |
| Script not found | `npm run` list | Add script to `package.json` `scripts` block |
| Wrong Node version | `node -v` vs `engines` | Use `nvm` / `.nvmrc` to match `engines` field |

## Gotchas

> [!WARNING]
> **`npm install` in Docker after `COPY . .`** — host `node_modules` can poison the layer; use multi-stage builds and `.dockerignore`.

> [!WARNING]
> **`--legacy-peer-deps` hides real incompatibilities** — acceptable for migration; not a permanent fix.

## When NOT to use

- **Monorepos with shared workspaces** — prefer `pnpm` or `yarn` workspaces for disk and speed.
- **Publishing libraries without lockfile discipline** — consumers need semver ranges, not your local tree.

## Related

[[npm error]] [[npm script]] [[yarn]] [[pnpm cli]] [[NodeJS/node package json]]
