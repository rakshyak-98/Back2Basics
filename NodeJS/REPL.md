[[NodeJS]]

# node repl

> watch

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

```bash
.load <file path>;
.save session.js
```
```bash
```
Read-Eval-Print-Loop.
- interactive shell.
- allows to execute JavaScript code.
- view the output immediately.
if `require.main` is `undefined` in your NodeJS REPL, you're likely in REPL mode started with `node` directly, and not from a script file, so `require.main` is not set.
```js
const { pathToFileURL } = require('url');
const { argv } = process;
const fs = require('fs')
const __filename = argv[0] || fs.replpathSync('.');
pathTOFileURL(__filename).href;
```
> [!NOTE] `require.main.filename` returns the path of the file that started the REPL session (usually some internal Node REPL).
> - you won't get the current `command's virtula file` because REPL isn't a real file.
```mjs
// exmaple.mjs
console.log(import.meta.url);
```

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
