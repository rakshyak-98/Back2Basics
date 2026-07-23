[[NodeJS]] [[CLI]] [[nvm]] [[node package json]] [[node inspect]]

# node command

> One-line: the `node` executable and common flags — version pinning, env preload, inspect, and one-liners when npm scripts aren't enough.

## Mental model

`node` is the V8 runtime entrypoint. It loads your script (CJS or ESM per [[node package json]] `"type"`), applies V8 flags after `--`, and exposes `process.*` globals. CI and production should call a **pinned absolute path** to Node — not whatever `which node` returns after nvm shims.

```
node [options] [ -e script | script.js ] [arguments]
         │
         ├── --import / -r     preload modules (dotenv, tsx)
         ├── --inspect         debugger
         └── --max-old-space-size
```

## Standard config / commands

### Version & path

```bash
node -v
which node
command -v node
```

### Run script

```bash
node server.js
node --watch server.js          # Node 18+ auto-restart on change
node --env-file=.env server.js  # Node 20+ native env file
```

### Preload env (ESM)

```bash
node --import dotenv/config server.js
node -r dotenv/config server.js   # CJS preload
```

### Eval

```bash
node -e "console.log(process.env.HOME)"
node -p "1 + 1"                   # print result
```

### When Node isn't on PATH (fish/nvm)

```bash
set -gx NVM_DIR $HOME/.nvm
nvm install lts
nvm use lts
node -e "import 'dotenv/config'; console.log(process.env.NODE_ENV)"
```

### Inspect / profile

```bash
node --inspect server.js
node --cpu-prof server.js         # writes *.cpuprofile
node --heapsnapshot-signal=SIGUSR2 server.js
```

### Pass args to script

```bash
node cli.js --port 4000
# process.argv: ['node', 'cli.js', '--port', '4000']
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `Cannot find module` | cwd; NODE_PATH | Run from project root; install deps |
| ESM/CJS mismatch | `"type":"module"` | Rename to `.cjs`/`.mjs` or adjust imports |
| `ERR_REQUIRE_ESM` | require() on ESM package | Use dynamic `import()` |
| Old Node in CI | `node -v` in pipeline | Pin setup-node / Docker base |
| dotenv not applied | Import order | `--import dotenv/config` before app |
| OOM heap | `--max-old-space-size` | Fix leak; scale memory |

## Gotchas

> [!WARNING]
> **`node -e` and top-level await** — need `--input-type=module` or wrap in async IIFE on older Node.

> [!WARNING]
> **Different node in cron vs shell** — cron uses minimal PATH; use full path in crontab.

## When NOT to use

- **Package binary** — prefer `npm run` / `npx` for local CLI tools.
- **Production multi-process** — systemd/K8s with explicit ExecStart, not shell aliases.

## Related

[[CLI]] [[nvm]] [[node package json]] [[node inspect]] [[Event Loop]]
