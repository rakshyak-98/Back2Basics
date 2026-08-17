[[node package json]] [[node command]] [[husk]] [[yarn]] [[npm]] [[ecosystem]]

# npm script

> Named shortcuts in `package.json` that run shell commands — the standard entry point for develop, test, lint, and build.





## Interview Relevance
Interviewers ask about npm scripts to see if you know argument forwarding (`--`), lifecycle `pre*`/`post*` hooks, cross-platform pitfalls, and why scripts are not a production process manager.

## Sources
- [npm Docs — scripts](https://docs.npmjs.com/cli/v10/using-npm/scripts) — deep-dive
- [npm Docs — run-script](https://docs.npmjs.com/cli/v10/commands/npm-run-script) — overview

## Core Definition
An npm script is a key under `"scripts"` in `package.json`. `npm run <name>` executes that command with local `node_modules/.bin` on `PATH`, so project CLIs work without global installs.

## Key Concepts
- **Local bins on PATH:** `eslint`, `vitest`, etc. resolve from the project → no global install required.
- **Argument forwarding:** everything after `--` is passed to the underlying tool.
- **Lifecycle hooks:** `predeploy` runs automatically before `deploy` → surprising side effects if undocumented.
- **Shortcuts:** `npm start`, `npm test`, `npm stop`, `npm restart` omit `run`; other names need `npm run`.
- **Cross-platform:** shell syntax differs (Windows vs Unix) → prefer `cross-env` and avoid bash-only one-liners when the team is mixed.

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

Forward flags through nested bash carefully:

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

## Real-World Applications
Every Node project uses scripts as the team’s documented commands for local development and continuous integration jobs.

**Example:** Continuous integration runs `npm ci && npm test && npm run build` so humans and pipelines share one entry point.

## Pros/Cons or Trade-offs
- **Pro:** Zero extra tooling; works everywhere npm works; documents team commands in the repository.
- **Con:** Long bash in `package.json` becomes unreadable — extract to `scripts/*.sh`.
- **Con:** Not a supervisor — use [[ecosystem|pm2]], systemd, or a container orchestrator in production.

## Comparison
- vs Makefile / Taskfile: external runners are richer; npm scripts win on ubiquity for JavaScript repos.
- vs [[husk]]: Husky triggers Git hooks that often *call* npm scripts (e.g. lint-staged), not the other way around.

## Mistakes to Avoid
- Putting secrets in script strings — they appear in `package.json` and process listings; use environment files or a secret store.
- Relying on `pre*` hooks nobody knows about.
- Using npm scripts as the production process manager instead of a real supervisor.
