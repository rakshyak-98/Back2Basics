[[NodeJS]] [[node command]] [[nvm]] [[Node.js run as a non-privileged user]] [[inputs]] [[node inspect]]

# Node.js CLI

> Node.js CLI — the node binary executes JavaScript (file or -e). npm run sets PATH to local node_modules/.bin and injects npm lifecycle env. npx runs package

```txt
        Node.js CLI ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers probe **Node.js CLI** to see if you understand what it does oper…

## Sources
- [Node.js — Command-line options](https://nodejs.org/api/cli.html) — deep-dive
- [npm — run-script](https://docs.npmjs.com/cli/v10/commands/npm-run-script) — overview
- [Wikipedia — CLI](https://en.wikipedia.org/wiki/CLI) — overview

## Key Concepts
- **The:** `node`:** The **`node` binary** executes JavaScript (file or `-e`)


- **Core:** The **`node` binary** executes JavaScript (file or `-e`). **`npm run`** sets …

## Technical Details
- The **`node` binary** executes JavaScript (file or `-e`).
- **`npm run`:** sets PATH to local `node_modules/.bin` and injects npm lifecycl…
- **`npx`:** runs package binaries without global install.
- Production services rarely use CLI ad hoc

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

## Mistakes to Avoid
- **Mistake:** **`sudo node` uses root's PATH**
- **Mistake:** **Remote inspect on 0.0.0.0**
- **Mistake:** **`npm run` hides failures**
- **Mistake:** **`command not found: node`:** check PATH
- **Mistake:** **Wrong Node version:** check `node -v` vs engines
- **Mistake:** **Module not found ESM/CJS:** check `"type":"module"` in package…
- **Mistake:** **Env vars undefined:** check Not loaded before import
- **Mistake:** **Permission errors:** check Running as root vs appuser
- **Mistake:** **Works in npm script, not direct:** check Relative cwd

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Node.js CLI — the node binary executes JavaScript (file or -e). npm run sets PAT…).
- **Con / when not:** **Production scaling**
- **Con / when not:** **Heavy REPL exploration**

## Comparison
- vs [[node command]]: know when each applies


### Use cases
- In production APIs and tooling, **CLI** shows up whenever teams ship Node/JS …
