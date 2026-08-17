[[pnpm CLI]] [[npm]] [[npm error]]

# pnpm logs

> Where pnpm writes debug output when an install or command fails — use verbose reporters and redirect stdout when the default log is not enough.

```txt
        pnpm logs ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers rarely quiz “where is the log file,” but debugging a broken inst…

## Sources
- [pnpm CLI — install](https://pnpm.io/cli/install) — overview
- [pnpm — Error Codes](https://pnpm.io/errors) — deep-dive
- [pnpm — Configuration](https://pnpm.io/npmrc) — overview

## Key Concepts
- **Store vs project:** the global content-addressable store holds packages; temporary paths under th…
- **Log level:** default output is brief
- **Redirect:** shell redirection captures everything when pnpm does not write a durable debu…
- **Lockfile + allow-list:** many “log” investigations end in peer conflicts, network mirrors, or blocked …


- **Core:** pnpm prints progress and errors to the terminal

## Technical Details
- Typical store locations (versioned paths vary by pnpm major):

| Platform | Common store / temp area |
|----------|---------------------------|
| Linux | `~/.local/share/pnpm/store/` |
| macOS | `~/Library/pnpm/store/` (or XDG-style under home) |
| Windows | `%LOCALAPPDATA%\pnpm\store\` |

```bash
pnpm install --loglevel debug
pnpm install --reporter ndjson
pnpm install > pnpm-debug.log 2>&1
pnpm store path                  # print store location when available
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Sparse error only | Default reporter | Re-run with `--loglevel debug` |
| Cannot reproduce in CI | Missing full log | Redirect stdout/stderr to artifact |
| Fetch failures | Registry / proxy | Inspect debug lines for URL and HTTP status |
| Build script denied | `allowBuilds` | See [[pnpm CLI]] approve-builds |

## Mistakes to Avoid
- **Mistake:** Digging only in store `tmp` folders when the real failure is a r…
- **Mistake:** Sharing logs that contain registry tokens or private package URLs

## Pros/Cons or Trade-offs
- **Pro:** Verbose reporters make dependency resolution debuggable without extra tools.
- **Con:** `ndjson` / debug output is noisy — capture to a file, do not paste entire traces into chat by default.

## Comparison
- vs [[npm error]]: npm often writes `npm-debug.log` on failure
- vs [[pnpm CLI]]: this note is about *observability*


### Use cases
- When `pnpm install` fails only in continuous integration, attach a debug log …
