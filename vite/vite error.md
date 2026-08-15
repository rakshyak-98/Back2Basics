[[vite config]] [[vite internal]] [[Linux/Error status code]]

# Vite error

> Common Vite CLI failures — especially `Permission denied` on `node_modules/.bin/vite` after bad installs, WSL copies, or lost execute bits.

## Interview Relevance

Interviewers like a crisp diagnosis: script path exists but is not executable; fix install integrity before rewriting configs.

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

## Real-World Applications

CI agent checks out a cache of `node_modules` from another OS — bins lose execute bits; prefer caching the package manager cache, not committed `node_modules`.

**Example:** WSL project copied from Windows NTFS without exec — clean `npm ci` inside the Linux filesystem.

## Pros/Cons or Trade-offs

- **Pro:** Local bins keep CLI versions per project.
- **Con:** Filesystem/permission quirks show up as opaque shell errors.

## Comparison

- vs global `vite`: local pin is safer; global hides per-app version skew.
- vs [[vite config]]: config bugs mis-build; this error never starts the tool.

## Mistakes to Avoid

- Chmod-only forever without fixing how `node_modules` was produced.
- Committing `node_modules` into git.
- Running from a `noexec` mounted directory.
