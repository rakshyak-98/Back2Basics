[[NodeJS]] [[promise]] [[Callback]] [[NodeJS/node fs]]

# JavaScript util module (Node.js)

> Node **`node:util`** helpers — `promisify`, `inspect`, `types`, deprecation — bridge callback APIs to async/await — **Node.js docs**.

---

## Mental model

Legacy Node core APIs are **callback-last** `(err, result) =>`. `util.promisify` wraps them into **Promises** for `async/await` composition with [[promise]] chains.

```txt
fs.readFile(path, cb)  →  promisify(fs.readFile)(path)  →  Promise<Buffer>
```

Modern Node exposes **`fs/promises`** natively — prefer those over promisify for built-ins.

| API | Use |
|-----|-----|
| `promisify(fn)` | Callback → Promise |
| `promisify.custom` | Native promise impl on fn |
| `inspect(obj, { depth })` | Safe logging |
| `types.isPromise(v)` | Duck typing |
| `deprecate(fn, msg)` | Library warnings |

---

## Standard config / commands

```javascript
import { promisify } from "node:util";
import { readFile } from "node:fs";
import { pipeline } from "node:stream";
import { inspect } from "node:util";

const readFileAsync = promisify(readFile);
const data = await readFileAsync("config.json", "utf8");

// Prefer built-in promises
import { readFile as readFileP } from "node:fs/promises";
const data2 = await readFileP("config.json", "utf8");

const pipe = promisify(pipeline);
await pipe(source, transform, dest);

console.log(inspect({ nested: { a: 1 } }, { depth: 2, colors: true }));
```

### Custom promisify on your callback API

```javascript
function query(sql, cb) { /* ... */ }
query[require("node:util").promisify.custom] = (sql) =>
  new Promise((resolve, reject) => query(sql, (err, rows) => err ? reject(err) : resolve(rows)));
```

### `callbackify` (reverse — rare)

```javascript
import { callbackify } from "node:util";
const readCb = callbackify(async () => readFileP("x"));
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `ERR_INVALID_ARG_TYPE` | Promisified non-callback fn | Function must be last-arg callback style |
| Hangs forever | Callback never called | Fix underlying API; add timeout wrapper |
| Double resolve | Callback called twice | Bug in wrapped lib — don't promisify broken cb |
| Lost `this` | Method promisify | `promisify(mod.method.bind(mod))` |
| Typo `require('utils')` | Wrong package name | `node:util` not npm `utils` |

---

## Gotchas

> [!WARNING]
> **Promisify functions with multiple success values** — only first cb arg after err becomes resolve value; rest dropped.

> [!WARNING]
> **Browser bundle** — `node:util` doesn't ship to client; use fetch/ Web APIs instead.

---

## When NOT to use

- **New code with native promise APIs** — `fs/promises`, `dns/promises`.
- **Browser / Deno client** — no Node util module.
- **EventEmitter → Promise** — `events.once(emitter, 'event')` (Node 15+).

---

## Related

[[NodeJS]] · [[promise]] · [[Callback]] · [[NodeJS/node fs]] · [[Event Loop]]
