[[NodeJS/node package json]] [[NodeJS/node command]] [[npm/husk]]

# npm scripts

> Named shortcuts in `package.json` → shell commands — the standard entry point for dev, test, and build.

## Mental model

`npm run <script>` executes the command in a shell with `node_modules/.bin` on PATH. Lifecycle hooks (`prestart`, `postinstall`) run automatically around named scripts. Arguments after `--` pass through to the underlying command without npm interpreting them.

```
package.json scripts → npm run dev → nodemon (local bin)
npm run dev -- file.js  → nodemon file.js
```

## Standard config / commands

### Pass args through `--`

```json
{
  "scripts": {
    "dev": "nodemon",
    "test": "vitest run",
    "lint": "eslint ."
  }
}
```

```bash
npm run dev -- src/index.js
npm test -- --coverage
```

### Forward flags to nested bash

```json
{
  "scripts": {
    "dev": "bash -c 'nodemon \"$0\"' --"
  }
}
```

```bash
npm run dev -- myfile.js
```

### Cross-platform env (prefer `cross-env`)

```json
{
  "scripts": {
    "start:prod": "cross-env NODE_ENV=production node dist/index.js"
  }
}
```

### CLI flags in scripts (minimist / yargs / commander)

```bash
npm install minimist yargs commander
```

```js
// bin/cli.js with commander — npm run cli -- deploy --env prod
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `command not found` | Local bin | Use `npx` or script name without path; `npm ci` |
| Args not reaching tool | Missing `--` | `npm run x -- --flag` |
| Works on Mac, fails Windows | Shell syntax | Use `cross-env`, avoid bash-only |
| `ELIFECYCLE` opaque error | Scroll up | Run underlying command directly |
| Infinite restart | nodemon watching wrong | `--ignore` or fix glob |

## Gotchas

> [!WARNING]
> **`npm start` vs `npm run start`** — `start`/`test`/`restart` have shortcuts; others need `run`.
>
> **Secrets in scripts** — visible in `package.json` and process list; use env files.
>
> **`pre*` hooks surprise** — `predeploy` runs before `deploy` automatically.

## When NOT to use

- Don't put 50-line bash in scripts — extract to `scripts/` shell file.
- Don't use npm scripts as a process manager in prod — use [[pm2/ecosystem]] or systemd.

## Related

[[NodeJS/node package json]] [[npm/yarn]] [[NodeJS/nvm]] [[pm2/ecosystem]]
