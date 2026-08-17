[[NodeJS]] [[node package json]] [[NodeJS CLI]] [[Runtime Errors]]

# node modules

> Each file is a module — dependencies resolve at runtime via `require` / `import`, not a C-style linker.

```txt
        node modules ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers use **node modules** to check whether you can explain the mechan…

## Sources
- [Node.js — Modules (CJS)](https://nodejs.org/api/modules.html) — deep-dive
- [Node.js — ECMAScript modules](https://nodejs.org/api/esm.html) — deep-dive
- [Wikipedia — node modules](https://en.wikipedia.org/wiki/node_modules) — overview

## Key Concepts
- **require cache:** Singleton per resolved path — Mutating exports affects everyone.
- **CJS vs ESM:** `require` vs `import` — TLA and `__dirname` differ.
- **exports:** Public surface — Only export what callers need.

## Technical Details
```txt
app.js ──require/import──► ./lib.js (cached after first load)
```

```js
// CommonJS
const fs = require('node:fs')
module.exports = { ok: true }

// ESM (package.json "type": "module" or .mjs)
import fs from 'node:fs'
export const ok = true
```

| Knob | Why it matters |
|------|----------------|
| `"type": "module"` | Default parse mode |
| `node:` prefix | Built-ins, unambiguous |
| Conditional exports | Package entry points |

## Mistakes to Avoid
- **Mistake:** **Circular requires** — partial exports; redesign or lazy require
- **Mistake:** **Global leaks**
- **Mistake:** **ERR_REQUIRE_ESM:** check CJS requiring ESM
- **Mistake:** **Duplicate copies:** check Nested node_modules
- **Mistake:** **Stale mock in tests:** check require cache
- **Mistake:** **Wrong file:** check Extension / exports map

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Each file is a module — dependencies resolve at runtime via `require` / `import`…).
- **Con / when not:** **Browser bundles**

## Comparison
- vs [[node package json]]: know when each applies


### Use cases
- In production APIs and tooling, **node modules** shows up whenever teams ship…
