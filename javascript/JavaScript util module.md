[[NodeJS]] [[promise]] [[Callback]] [[NodeJS/node fs]] [[Event Loop]]

# JavaScript util module (Node.js)

> JavaScript util module (Node.js) — legacy Node core APIs are callback-last (err, result) =>. util.promisify wraps them into Promises for async/await composition with promise chains.

```txt
        JavaScript util mo ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers probe **JavaScript util module (Node.js)** to see if you underst…

## Sources
- [Wikipedia — JavaScript util module](https://en.wikipedia.org/wiki/JavaScript_util_module) — overview

## Key Concepts
- **Legacy Node:** Legacy Node core APIs are **callback-last** `(err, result) =>`
- **Modern Node:** Modern Node exposes **`fs/promises`** natively


- **Core:** Legacy Node core APIs are **callback-last** `(err, result) =>`

## Technical Details
- Legacy Node core APIs are **callback-last** `(err, result) =>`.
- `util.promisify` wraps them into **Promises** for `async/await` composition w…

```txt
fs.readFile(path, cb)  →  promisify(fs.readFile)(path)  →  Promise<Buffer>
```

- Modern Node exposes **`fs/promises`** natively

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

## Mistakes to Avoid
- **Mistake:** **Promisify functions with multiple success values**
- **Mistake:** **Browser bundle**
- **Mistake:** **`ERR_INVALID_ARG_TYPE`:** check Promisified non-callback fn
- **Mistake:** **Hangs forever:** check Callback never called
- **Mistake:** **Double resolve:** check Callback called twice
- **Mistake:** **Lost `this`:** check Method promisify
- **Mistake:** **Typo `require('utils')`:** check Wrong package name

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (JavaScript util module (Node.js) — legacy Node core APIs are callback-last (err,…).
- **Con / when not:** **New code with native promise APIs**
- **Con / when not:** **Browser / Deno client** — no Node utility module.
- **Con / when not:** **EventEmitter → Promise**

## Comparison
- vs [[promise]]: know when each applies


### Use cases
- In production APIs and tooling, **JavaScript util module** shows up whenever …
