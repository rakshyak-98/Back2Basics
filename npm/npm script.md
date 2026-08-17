[[node package json]] [[node command]] [[husk]] [[yarn]] [[npm]] [[ecosystem]]

# npm script

> Named shortcuts in `package.json` that run shell commands — the standard entry point for develop, test, lint, and build.

```txt
        npm script ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers ask about npm scripts to see if you know argument forwarding (`-…

## Sources
- [npm Docs — scripts](https://docs.npmjs.com/cli/v10/using-npm/scripts) — deep-dive
- [npm Docs — run-script](https://docs.npmjs.com/cli/v10/commands/npm-run-script) — overview

## Key Concepts
- **Local bins on PATH:** `eslint`, `vitest`, etc
- **Argument forwarding:** everything after `--` is passed to the underlying tool.
- **Lifecycle hooks:** `predeploy` runs automatically before `deploy` → surprising side effects if u…
- **Shortcuts:** `npm start`, `npm test`, `npm stop`, `npm restart` omit `run`
- **Cross-platform:** shell syntax differs (Windows vs Unix) → prefer `cross-env` and avoid bash-on…


- **Core:** An npm script is a key under `"scripts"` in `package.json`

## Technical Details
```
package.json scripts → npm run dev → local bin (e.g. nodemon)
npm run dev -- file.js           → nodemon file.js
```

```json
{
  "scripts": {
    "dev": "nodemon",
    "test": "vitest run",
    "lint": "eslint .",
    "start:production": "cross-env NODE_ENV=production node dist/index.js"
  }
}
```

```bash
npm run dev -- src/index.js
npm test -- --coverage
npm run lint
```

- Forward flags through nested bash carefully:

```json
{
  "scripts": {
    "dev": "bash -c 'nodemon \"$0\"' --"
  }
}
```

| Symptom | Check | Fix |
|---------|-------|-----|
| `command not found` | Local bin / install | Use script name; run `npm ci` |
| Flags never reach tool | Missing `--` | `npm run x -- --flag` |
| Works on macOS, fails on Windows | Shell syntax | `cross-env`; avoid bash-only |
| Opaque `ELIFECYCLE` | Scroll up | Run the underlying command directly |
| Infinite restart | Watcher globs | Ignore build output; fix watch paths |

## Mistakes to Avoid
- **Mistake:** Putting secrets in script strings
- **Mistake:** Relying on `pre*` hooks nobody knows about
- **Mistake:** Using npm scripts as the production process manager instead of a…

## Pros/Cons or Trade-offs
- **Pro:** Zero extra tooling; works everywhere npm works; documents team commands in the repository.
- **Con:** Long bash in `package.json` becomes unreadable — extract to `scripts/*.sh`.
- **Con:** Not a supervisor — use [[ecosystem|pm2]], systemd, or a container orchestrator in production.

## Comparison
- vs Makefile / Taskfile: external runners are richer
- vs [[husk]]: Husky triggers Git hooks that often *call* npm scripts (e.g


### Use cases
- Every Node project uses scripts as the team’s documented commands for local d…

- **Example:** Continuous integration runs `npm ci && npm test && npm run build…
