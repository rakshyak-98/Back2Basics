[[npm]] [[yarn]] [[npm script]] [[node package json]]

# pnpm cli

> Fast, disk-efficient Node package manager — hard-links packages from a shared store and blocks unapproved install scripts by default.

```txt
        pnpm cli ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers ask about pnpm to probe supply-chain awareness (`approve-builds`…

## Sources
- [pnpm — Build settings (`allowBuilds`)](https://pnpm.io/settings/build) — deep-dive
- [pnpm — Motivation](https://pnpm.io/motivation) — overview
- [pnpm 11.0 release notes](https://pnpm.io/blog/releases/11.0) — overview

## Key Concepts
- **Content-addressable store:** one copy of each package version on disk → projects hard-link or clone into a…
- **Strict node_modules:** packages only see declared dependencies → catches “phantom” imports that acci…
- **`allowBuilds` / `pnpm approve-builds`:** whitelist which packages may run `preinstall` / `install` / `postinstall` → r…
- **`dangerouslyAllowAllBuilds`:** runs all dependency build scripts without review → convenient but unsafe for …
- **Workspaces:** `pnpm-workspace.yaml` defines packages → efficient monorepo installs.


- **Core:** pnpm installs the same npm-registry packages as npm/Yarn, but stores content …

## Technical Details
- Packages such as `esbuild` download platform binaries in `postinstall`.
- pnpm may block that until approved:

```bash
pnpm approve-builds              # interactive approval
pnpm approve-builds esbuild      # allow one package (non-interactive)
pnpm approve-builds '!core-js'   # deny (prefix !)
pnpm install
pnpm add lodash
pnpm why lodash
```

- Modern setting shape (`pnpm-workspace.yaml` / project settings):

```yaml
allowBuilds:
  electron: true
  esbuild: true
  core-js: false
```

- Older settings (`onlyBuiltDependencies`, `neverBuiltDependencies`, …) were re…

| Symptom | Check | Fix |
|---------|-------|-----|
| Install blocked on build scripts | Unlisted package | `pnpm approve-builds` or set `allowBuilds` |
| Module not found that “worked on npm” | Phantom dependency | Add a real dependency declaration |
| Binary missing after deny | Build script skipped | Allow the package that downloads the binary |
| CI differs from laptop | Different allow-list | Commit `pnpm-workspace.yaml` / allow map |

## Mistakes to Avoid
- **Mistake:** Setting `dangerouslyAllowAllBuilds: true` permanently “to make C…
- **Mistake:** Ignoring phantom-dependency failures instead of declaring the re…
- **Mistake:** Mixing pnpm with npm/Yarn lockfiles in the same project

## Pros/Cons or Trade-offs
- **Pro:** Less disk use, faster installs, stricter dependency visibility.
- **Con:** Packages that relied on hoisting break until dependencies are declared correctly.
- **Con:** Build-script gating adds friction until the allow-list stabilizes.

## Comparison
- vs [[npm]]: Same registry; pnpm’s layout and script policy are stricter by default.
- vs [[yarn]]: Yarn Berry uses Plug’n’Play


### Use cases
- Large monorepos and security-conscious teams use pnpm to save disk and force …

- **Example:** After upgrading pnpm, `esbuild`’s postinstall is blocked
