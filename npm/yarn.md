[[npm]] [[npm script]] [[node package json]] [[husk]] [[Release cycle]]

# Yarn

> Alternative Node package manager — deterministic installs via a lockfile, with strong workspace support for monorepos (Classic and Berry).

## Interview Relevance

Interviewers use Yarn to check whether you can explain lockfile discipline, Classic versus Berry (node_modules vs Plug’n’Play), and why mixing Yarn with [[npm]] in one project causes drift.

## Sources

- [Yarn Classic documentation](https://classic.yarnpkg.com/en/docs/) — overview
- [Yarn Berry documentation](https://yarnpkg.com/getting-started) — deep-dive
- [Wikipedia — Yarn (package manager)](https://en.wikipedia.org/wiki/Yarn_(package_manager)) — overview

## Core Definition

Yarn installs JavaScript packages from the npm registry (or mirrors) using its own resolver and lockfile format, aiming for reproducible installs and convenient monorepo workspaces.

## Key Concepts

- **Classic (v1) vs Berry (v2+):** Classic uses `yarn.lock` + hoisted `node_modules`; Berry uses `.yarnrc.yml`, can use Plug’n’Play (`.pnp.cjs`), and is enabled via Corepack.
- **Lockfile:** pins exact versions → everyone and continuous integration get the same tree.
- **Workspaces:** one root project owns multiple packages → install once, link locally.
- **`yarn why`:** explains why a package is present → debug duplicate versions and hoisting surprises.
- **Zero-install (Berry):** commit the cache for offline installs → large repository size trade-off.

## Technical Details

### Daily commands

```bash
yarn install                    # from lockfile
yarn add lodash
yarn add -D typescript
yarn add -E package@1.2.3       # exact version (Classic)
yarn remove lodash
yarn upgrade-interactive        # Classic: pick upgrades
yarn info lodash
yarn why lodash
yarn outdated
yarn licenses list
yarn cache clean
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

### Berry (v2+) setup

```bash
corepack enable
yarn set version stable
yarn install
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Lockfile merge conflict | `yarn.lock` | Checkout one side, re-run `yarn install` |
| Wrong hoisting / duplicates | `yarn why` | Align versions; Classic `nohoist` if needed |
| PnP cannot resolve module | `.pnp.cjs` / editor SDK | Install Yarn SDKs or use `nodeLinker: node-modules` |
| Classic and Berry mixed | `.yarnrc.yml` present? | Pick one major line; do not mix lockfile formats |
| Stale continuous integration cache | Cache key | Key cache on lockfile hash |

## Real-World Applications

Teams pick Yarn for monorepos, faster installs than older npm, or Berry’s Plug’n’Play and constraints.

**Example:** A polyrepo migrates to workspaces under one `yarn.lock` so shared libraries link locally without publishing for every change.

## Pros/Cons or Trade-offs

- **Pro:** Strong workspace story; `yarn why` and interactive upgrades help day-to-day maintenance.
- **Con:** Berry Plug’n’Play needs editor/tooling support; otherwise teams fall back to the node-modules linker.
- **Con:** Zero-install commits grow the Git history and complicate reviews.

## Comparison

- vs [[npm]]: Same registry; different lockfile and workspace UX. Prefer one manager per project.
- vs [[pnpm cli]]: pnpm focuses on a content-addressable store and strict dependency isolation; Yarn Berry focuses on PnP and project constraints.

## Mistakes to Avoid

- Running `yarn` and `npm install` interchangeably — two lockfiles mean silent version drift.
- Jumping majors with non-interactive upgrade without reading changelogs.
- Adopting Berry Plug’n’Play without committing the team to SDK and continuous integration setup.
