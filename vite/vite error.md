[[vite config]] [[vite internal]] [[Linux/Error status code]]

# Vite error

> Common Vite CLI failures — especially `Permission denied` on `node_modules/.bin/vite` after bad installs, WSL copies, or lost execute bits.

```txt
        Vite error ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers like a crisp diagnosis: script path exists but is not executable

## Sources
- [Vite — Troubleshooting](https://vitejs.dev/guide/troubleshooting.html) — overview
- [npm — npx](https://docs.npmjs.com/cli/v10/commands/npx) — overview

## Key Concepts
- **`npm run build` → local bin:** runs `node_modules/.bin/vite` (often via `npx`).
- **Execute bit:** missing `+x` → `sh: vite: Permission denied`.
- **Corrupt `node_modules`:** copied across OS/WSL or partial installs.

## Technical Details
```text
sh: 1: vite: Permission denied
```

```bash
ls -l node_modules/.bin/vite
rm -rf node_modules
npm ci   # or npm install
chmod +x node_modules/.bin/vite   # temporary; prefer clean reinstall
npx vite build
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Permission denied | `ls -l` on bin | Reinstall modules; fix mount `noexec` |
| Cannot find module | Install incomplete | Delete lock mismatch; `npm ci` |
| Wrong Vite version | `npx vite --version` | Align package.json / lockfile |

## Mistakes to Avoid
- **Mistake:** Chmod-only forever without fixing how `node_modules` was produced
- **Mistake:** Committing `node_modules` into git
- **Mistake:** Running from a `noexec` mounted directory

## Pros/Cons or Trade-offs
- **Pro:** Local bins keep CLI versions per project.
- **Con:** Filesystem/permission quirks show up as opaque shell errors.

## Comparison
- vs global `vite`: local pin is safer; global hides per-app version skew.
- vs [[vite config]]: config bugs mis-build; this error never starts the tool.


### Use cases
- CI agent checks out a cache of `node_modules` from another OS

- **Example:** WSL project copied from Windows NTFS without exec
