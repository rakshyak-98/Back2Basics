[[NodeJS]] [[nvm]] [[node package json]] [[node inspect]] [[INDEX]]

# NodeJS CLI

> Node.js, npm, and npx CLI — runtime flags, scripts, debugging, and production pinning.

---

## Node runtime

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

### Examples

```bash

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

## npm

### Examples

```bash

```
