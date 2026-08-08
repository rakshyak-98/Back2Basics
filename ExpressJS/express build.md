[[ExpressJS]]

# express build

> express build — you must NOT bundle express, mongoose, cors, helmet, dotenv, morgan (and almost all other npm packages) when building a Node.js backend.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

```js
const esbuild = require("esbuild");
esbuild.build({
  entryPoints: ["index.js"],
  bundle: true,
  platform: "node",
  external: [
    // NEVER bundle these
    "bcrypt",
    "cookie-parser",
    "cors",
    "dotenv",
    "express",
    "express-mysql-session",
    "express-session",
    "mysql2",
    "nodemailer",
    "nodemon",
    "prettier"
  ],
  outfile: "dist/server.js",
  minify: true
});
```
- You must NOT bundle `express`, `mongoose`, `cors`, `helmet`, `dotenv`, `morgan` (and almost all other npm packages) when building a Node.js backend.
- If you bundle them, you will get broken or huge code in production.
> [!WARNING]
> Bundle only your source code, never bundle `node_modules`
> That's why `external: ['express', 'bcrypt', ...]` is required for a working production backend.

## Standard config / commands

…

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| … | … | … |

## Gotchas

> [!WARNING]
> …

## When NOT to use

…

## Related

[[…]]
