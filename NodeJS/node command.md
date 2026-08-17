[[NodeJS]] [[CLI]] [[nvm]] [[node package json]] [[node inspect]] [[Event Loop]]

# node command

> node command — node is the V8 runtime entrypoint. It loads your script (CJS or ESM per node package json "type"), applies V8 flags after --





## Interview Relevance
Interviewers probe **node command** to see if you understand what it does operationally and when it is the wrong tool — not just the definition.

## Sources
- [Node.js — Command-line options](https://nodejs.org/api/cli.html) — deep-dive
- [Wikipedia — node command](https://en.wikipedia.org/wiki/node_command) — overview

## Core Definition
`node` is the V8 runtime entrypoint. It loads your script (CJS or ESM per [[node package json]] `"type"`), applies V8 flags after `--`, and exposes `process.*` globals. CI and production should call a **pinned absolute path** to Node — not whatever `which node` returns after nvm shims.

## Key Concepts
- `node` is the V8 runtime entrypoint. It loads your script (CJS or ESM per [[node package json]] `"type"`), applies V8 flags after `--`, and exposes `process.*` globals. CI and p…

## Technical Details
`node` is the V8 runtime entrypoint. It loads your script (CJS or ESM per [[node package json]] `"type"`), applies V8 flags after `--`, and exposes `process.*` globals. CI and production should call a **pinned absolute path** to Node — not whatever `which node` returns after nvm shims.

```
node [options] [ -e script | script.js ] [arguments]
         │
         ├── --import / -r     preload modules (dotenv, tsx)
         ├── --inspect         debugger
         └── --max-old-space-size
```

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
In production APIs and tooling, **node command** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **`node -e` and top-level await** — need `--input-type=module` or wrap in async IIFE on older Node; **Different node in cron vs shell** — cron uses minimal PATH; use full path in crontab.

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (node command — node is the V8 runtime entrypoint. It loads your script (CJS or E…).
- **Con / when not:** **Package binary** — prefer `npm run` / `npx` for local CLI tools.
- **Con / when not:** **Production multi-process** — systemd/K8s with explicit ExecStart, not shell aliases.

## Comparison
vs [[CLI]]: know when each applies — do not treat them as interchangeable. vs [[nvm]]: know when each applies — do not treat them as interchangeable. vs [[node package json]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid
- **`node -e` and top-level await** — need `--input-type=module` or wrap in async IIFE on older Node.
- **Different node in cron vs shell** — cron uses minimal PATH; use full path in crontab.
- **`Cannot find module`:** check cwd; NODE_PATH; fix: Run from project root; install deps
- **ESM/CJS mismatch:** check `"type":"module"`; fix: Rename to `.cjs`/`.mjs` or adjust imports
- **`ERR_REQUIRE_ESM`:** check require() on ESM package; fix: Use dynamic `import()`
- **Old Node in CI:** check `node -v` in pipeline; fix: Pin setup-node / Docker base
- **dotenv not applied:** check Import order; fix: `--import dotenv/config` before app
- **OOM heap:** check `--max-old-space-size`; fix: Fix leak; scale memory
