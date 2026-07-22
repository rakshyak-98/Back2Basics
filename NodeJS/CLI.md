[[NodeJS]] [[node command]] [[nvm]] [[Node.js run as a non-privileged user]] [[inputs]]

# Node.js CLI

> One-line: run scripts, eval snippets, and switch users/environments from the shell — know when `node` vs `npm run` vs `npx` applies.

## Mental model

The **`node` binary** executes JavaScript (file or `-e`). **`npm run`** sets PATH to local `node_modules/.bin` and injects npm lifecycle env. **`npx`** runs package binaries without global install. Production services rarely use CLI ad hoc — they use systemd/Docker with pinned paths.

```
Developer shell          CI / systemd
     │                        │
     ├─ node app.js           ├─ /opt/node/bin/node app.js
     ├─ npm run start         ├─ EnvironmentFile + User=
     └─ npx tsx watch src     └─ no nvm unless explicit load
```

## Standard config / commands

### Run application

```bash
node server.js
node --import dotenv/config server.js   # load env before ESM imports
NODE_ENV=production node server.js
```

### One-liner eval

```bash
node -e "console.log(process.version)"
node -e "import('dotenv/config').then(() => console.log(process.env.PORT))"
```

### npm scripts

```bash
npm run start          # from package.json scripts
npm run dev -- --port 4000   # pass args after --
```

### npx (no global install)

```bash
npx prisma migrate deploy
npx tsx src/cli.ts
```

### Run as different user

```bash
sudo -u appuser node /path/to/app.js
sudo -u appuser -H bash -lc 'cd /app && source ~/.nvm/nvm.sh && nvm use && node app.js'
```

### Debug / inspect

```bash
node --inspect server.js
node --inspect-brk=0.0.0.0:9229 server.js   # bind for remote debug (firewall!)
```

### Memory / V8 flags

```bash
node --max-old-space-size=4096 server.js
node --trace-warnings server.js
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `command not found: node` | PATH; nvm not loaded | Absolute path; source nvm in shell profile |
| Wrong Node version | `node -v` vs engines | `nvm use`; align Docker/CI |
| Module not found ESM/CJS | `"type":"module"` in package.json | Use `.mjs` or `"type":"module"` consistently |
| Env vars undefined | Not loaded before import | `--import dotenv/config` or systemd EnvironmentFile |
| Permission errors | Running as root vs appuser | [[Node.js run as a non-privileged user]] |
| Works in npm script, not direct | Relative cwd | `cd` to project root; check `process.cwd()` |

## Gotchas

> [!WARNING]
> **`sudo node` uses root's PATH** — not your nvm Node; use `sudo -u` with login shell.

> [!WARNING]
> **Remote inspect on 0.0.0.0** — exposes debugger; never in prod without tunnel/VPN.

> [!WARNING]
> **`npm run` hides failures** — scripts may swallow exit codes; use `set -e` in shell wrappers.

## When NOT to use

- **Production scaling** — process manager (systemd, K8s) not manual CLI.
- **Heavy REPL exploration** — use `node` REPL or [[REPL]] note for interactive debugging.

## Related

[[node command]] [[nvm]] [[inputs]] [[node inspect]] [[Node.js run as a non-privileged user]]
