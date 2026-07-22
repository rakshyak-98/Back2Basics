[[npm/npm script]] [[NodeJS/node package json]] [[Release cycle]]

# Yarn (Classic / Berry)

> Alternative Node package manager — lockfile, deterministic installs, workspace monorepos.

## Mental model

Yarn resolves dependencies from `package.json`, writes `yarn.lock` (Classic v1) or `.yarn/cache` (Berry v2+). `yarn install` is CI's first step. Commands mirror npm with different flags. Berry adds Plug'n'Play (no `node_modules`) unless `nodeLinker: node-modules`.

## Standard config / commands

### Daily commands

```bash
yarn install                    # from lockfile
yarn add lodash
yarn add -D typescript
yarn add -E package@1.2.3       # exact version (Classic)
yarn remove lodash
yarn upgrade-interactive        # Classic: pick upgrades
```

### Diagnostics

```bash
yarn info lodash
yarn why lodash                 # who depends on it
yarn outdated
yarn licenses list
yarn cache clean                # free disk (Classic global cache)
```

### Workspaces (monorepo)

```json
{
  "private": true,
  "workspaces": ["packages/*"]
}
```

```bash
yarn workspace @app/web add react
```

### Berry (v2+) notes

```bash
corepack enable
yarn set version stable
yarn install
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Lockfile conflict | `yarn.lock` merge | Regenerate: checkout one side, `yarn install` |
| Wrong hoisting | `yarn why` | Align versions; `nohoist` in workspaces |
| PnP can't find module | `.pnp.cjs` | `yarn dlx @yarnpkg/sdks vscode` or switch to node-modules linker |
| Classic vs Berry mix | `.yarnrc.yml` exists? | Pick one; don't mix lockfile formats |
| CI cache stale | Cache key | Key on lockfile hash |

## Gotchas

> [!WARNING]
> **npm + yarn same repo** — two lockfiles = drift; pick one package manager.
>
> **`yarn upgrade` without interactive** — can jump majors; read changelog.
>
> **Berry zero-install** — commits cache to git; huge repo size tradeoff.

## When NOT to use

- Don't run `yarn` and `npm install` interchangeably on the same project.
- Don't use Berry PnP without tooling support unless team commits to SDK setup.

## Related

[[npm/npm script]] [[NodeJS/node package json]] [[npm/husk]]
