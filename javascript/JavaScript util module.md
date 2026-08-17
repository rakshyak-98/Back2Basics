[[NodeJS]] [[promise]] [[Callback]] [[NodeJS/node fs]] [[Event Loop]]

# JavaScript util module (Node.js)

> JavaScript util module (Node.js) — legacy Node core APIs are callback-last (err, result) =>. util.promisify wraps them into Promises for async/await composition with promise chains.





## Interview Relevance
Interviewers probe **JavaScript util module (Node.js)** to see if you understand what it does operationally and when it is the wrong tool — not just the definition.

## Sources
- [Wikipedia — JavaScript util module](https://en.wikipedia.org/wiki/JavaScript_util_module) — overview

## Core Definition
Legacy Node core APIs are **callback-last** `(err, result) =>`. `util.promisify` wraps them into **Promises** for `async/await` composition with [[promise]] chains.

## Key Concepts
- Legacy Node core APIs are **callback-last** `(err, result) =>`. `util.promisify` wraps them into **Promises** for `async/await` composition with [[promise]] chains.
- Modern Node exposes **`fs/promises`** natively — prefer those over promisify for built-ins.

## Technical Details
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

## Real-World Applications
In production APIs and tooling, **JavaScript util module** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **Promisify functions with multiple success values** — only first cb arg after err becomes resolve value; rest dropped; **Browser bundle** — `node:util` doesn't ship to client; use fetch/ Web APIs instead.

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (JavaScript util module (Node.js) — legacy Node core APIs are callback-last (err,…).
- **Con / when not:** **New code with native promise APIs** — `fs/promises`, `dns/promises`.
- **Con / when not:** **Browser / Deno client** — no Node utility module.
- **Con / when not:** **EventEmitter → Promise** — `events.once(emitter, 'event')` (Node 15+).

## Comparison
vs [[promise]]: know when each applies — do not treat them as interchangeable. vs [[Callback]]: know when each applies — do not treat them as interchangeable. vs [[NodeJS/node fs]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid
- **Promisify functions with multiple success values** — only first cb arg after err becomes resolve value; rest dropped.
- **Browser bundle** — `node:util` doesn't ship to client; use fetch/ Web APIs instead.
- **`ERR_INVALID_ARG_TYPE`:** check Promisified non-callback fn; fix: Function must be last-arg callback style
- **Hangs forever:** check Callback never called; fix: Fix underlying API; add timeout wrapper
- **Double resolve:** check Callback called twice; fix: Bug in wrapped lib — don't promisify broken cb
- **Lost `this`:** check Method promisify; fix: `promisify(mod.method.bind(mod))`
- **Typo `require('utils')`:** check Wrong package name; fix: `node:util` not npm `utils`
