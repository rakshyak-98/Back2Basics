[[NodeJS]] [[node command]] [[nvm]] [[Node.js run as a non-privileged user]] [[inputs]] [[node inspect]]

# Node.js CLI

> Node.js CLI — the node binary executes JavaScript (file or -e). npm run sets PATH to local node_modules/.bin and injects npm lifecycle env. npx runs package

## Interview Relevance

Interviewers probe **Node.js CLI** to see if you understand what it does operationally and when it is the wrong tool — not just the definition.

## Sources

- [Node.js — Command-line options](https://nodejs.org/api/cli.html) — deep-dive
- [npm — run-script](https://docs.npmjs.com/cli/v10/commands/npm-run-script) — overview
- [Wikipedia — CLI](https://en.wikipedia.org/wiki/CLI) — overview

## Core Definition

The **`node` binary** executes JavaScript (file or `-e`). **`npm run`** sets PATH to local `node_modules/.bin` and injects npm lifecycle environment. **`npx`** runs package binaries without global install. Production services rarely use CLI ad hoc — they use systemd/Docker with pinned paths.

## Key Concepts

- The **`node` binary** executes JavaScript (file or `-e`). **`npm run`** sets PATH to local `node_modules/.bin` and injects npm lifecycle environment. **`npx`** runs package bina…

## Technical Details

The **`node` binary** executes JavaScript (file or `-e`). **`npm run`** sets PATH to local `node_modules/.bin` and injects npm lifecycle environment. **`npx`** runs package binaries without global install. Production services rarely use CLI ad hoc — they use systemd/Docker with pinned paths.

```
Developer shell          CI / systemd
     │                        │
     ├─ node app.js           ├─ /opt/node/bin/node app.js
     ├─ npm run start         ├─ EnvironmentFile + User=
     └─ npx tsx watch src     └─ no nvm unless explicit load
```

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

### Quick reference

| Task | Command |
|------|---------|
| … | `…` |

### Options and flags

| Flag | Effect | When to use |
|------|--------|-------------|
| … | … | … |

### Examples

```bash
```

## Real-World Applications

In production APIs and tooling, **CLI** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **`sudo node` uses root's PATH** — not your nvm Node; use `sudo -u` with login shell; **Remote inspect on 0.0.0.0** — exposes debugger; never in prod without tunnel/VPN.

## Pros/Cons or Trade-offs

- **Pro:** Solves the job described above when used in the right layer (Node.js CLI — the node binary executes JavaScript (file or -e). npm run sets PAT…).
- **Con / when not:** **Production scaling** — process manager (systemd, K8s) not manual CLI.
- **Con / when not:** **Heavy REPL exploration** — use `node` REPL or [[REPL]] note for interactive debugging.

## Comparison

vs [[node command]]: know when each applies — do not treat them as interchangeable. vs [[nvm]]: know when each applies — do not treat them as interchangeable. vs [[Node.js run as a non-privileged user]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid

- **`sudo node` uses root's PATH** — not your nvm Node; use `sudo -u` with login shell.
- **Remote inspect on 0.0.0.0** — exposes debugger; never in prod without tunnel/VPN.
- **`npm run` hides failures** — scripts may swallow exit codes; use `set -e` in shell wrappers.
- **`command not found: node`:** check PATH; nvm not loaded; fix: Absolute path; source nvm in shell profile
- **Wrong Node version:** check `node -v` vs engines; fix: `nvm use`; align Docker/CI
- **Module not found ESM/CJS:** check `"type":"module"` in package.json; fix: Use `.mjs` or `"type":"module"` consistently
- **Env vars undefined:** check Not loaded before import; fix: `--import dotenv/config` or systemd EnvironmentFile
- **Permission errors:** check Running as root vs appuser; fix: [[Node.js run as a non-privileged user]]
- **Works in npm script, not direct:** check Relative cwd; fix: `cd` to project root; check `process.cwd()`
