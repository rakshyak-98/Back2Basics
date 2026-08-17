[[NodeJS]] [[CLI]] [[nvm]] [[node package json]] [[node inspect]] [[Event Loop]]

# node command

> node command — node is the V8 runtime entrypoint. It loads your script (CJS or ESM per node package json "type"), applies V8 flags after --

```txt
        node command ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers probe **node command** to see if you understand what it does ope…

## Sources
- [Node.js — Command-line options](https://nodejs.org/api/cli.html) — deep-dive
- [Wikipedia — node command](https://en.wikipedia.org/wiki/node_command) — overview

## Key Concepts
- **`node` is:** `node` is the V8 runtime entrypoint


- **Core:** `node` is the V8 runtime entrypoint. It loads your script (CJS or ESM per [[n…

## Technical Details
- `node` is the V8 runtime entrypoint.
- It loads your script (CJS or ESM per [[node package json]] `"type"`), applies…
- CI and production should call a **pinned absolute path** to Node

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

## Mistakes to Avoid
- **Mistake:** **`node -e` and top-level await**
- **Mistake:** **Different node in cron vs shell**
- **Mistake:** **`Cannot find module`:** check cwd
- **Mistake:** **ESM/CJS mismatch:** check `"type":"module"`
- **Mistake:** **`ERR_REQUIRE_ESM`:** check require() on ESM package
- **Mistake:** **Old Node in CI:** check `node -v` in pipeline
- **Mistake:** **dotenv not applied:** check Import order
- **Mistake:** **OOM heap:** check `--max-old-space-size`

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (node command — node is the V8 runtime entrypoint. It loads your script (CJS or E…).
- **Con / when not:** **Package binary**
- **Con / when not:** **Production multi-process**

## Comparison
- vs [[CLI]]: know when each applies


### Use cases
- In production APIs and tooling, **node command** shows up whenever teams ship…
