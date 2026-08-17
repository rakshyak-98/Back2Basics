[[pnpm CLI]] [[NodeJS CLI]] [[INDEX]]

# npm CLI

> npm and pnpm CLI — install, scripts, and workspace commands.

---

## pnpm

From [[pnpm CLI]].

```bash
pnpm approve-builds              # interactive approval
pnpm approve-builds esbuild      # allow one package (non-interactive)
pnpm approve-builds '!core-js'   # deny (prefix !)
pnpm install
pnpm add lodash
pnpm why lodash
```


## npm

From [[NodeJS CLI]].

```bash
npm install pkg@1.2.3
npm install pkg --save-exact
npm ci
npm update pkg
npm outdated
npm dedupe
npm run start -- --port 4000
npm view pkg version
npm explain pkg
npm config list
npm cache clean --force
```
