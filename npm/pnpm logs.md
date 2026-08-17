[[pnpm cli]] [[npm]] [[npm error]]

# pnpm logs

> Where pnpm writes debug output when an install or command fails — use verbose reporters and redirect stdout when the default log is not enough.





## Interview Relevance
Interviewers rarely quiz “where is the log file,” but debugging a broken install under time pressure shows whether you can raise log level, capture output, and distinguish store/cache paths from project errors.

## Sources
- [pnpm CLI — install](https://pnpm.io/cli/install) — overview
- [pnpm — Error Codes](https://pnpm.io/errors) — deep-dive
- [pnpm — Configuration](https://pnpm.io/npmrc) — overview

## Core Definition
pnpm prints progress and errors to the terminal. For failures, raise `--loglevel` / change `--reporter`, and redirect output to a file so you can share a full trace with teammates or support.

## Key Concepts
- **Store vs project:** the global content-addressable store holds packages; temporary paths under the store may hold transient files — do not confuse them with application logs.
- **Log level:** default output is brief; `debug` / `ndjson` reporters expose resolution and fetch detail.
- **Redirect:** shell redirection captures everything when pnpm does not write a durable debug file by default.
- **Lockfile + allow-list:** many “log” investigations end in peer conflicts, network mirrors, or blocked build scripts ([[pnpm cli]]).

## Technical Details
Typical store locations (versioned paths vary by pnpm major):

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
| Build script denied | `allowBuilds` | See [[pnpm cli]] approve-builds |

## Real-World Applications
When `pnpm install` fails only in continuous integration, attach a debug log artifact so you can see the exact package, registry response, and script block that aborted the job.

## Pros/Cons or Trade-offs
- **Pro:** Verbose reporters make dependency resolution debuggable without extra tools.
- **Con:** `ndjson` / debug output is noisy — capture to a file, do not paste entire traces into chat by default.

## Comparison
- vs [[npm error]]: npm often writes `npm-debug.log` on failure; pnpm more often expects explicit log level or redirection.
- vs [[pnpm cli]]: this note is about *observability*; that note covers CLI behavior and build approval.

## Mistakes to Avoid
- Digging only in store `tmp` folders when the real failure is a registry 403 or blocked postinstall.
- Sharing logs that contain registry tokens or private package URLs.
