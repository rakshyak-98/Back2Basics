[[NodeJS]] [[node package json]] [[npm command]] [[Runtime Errors]]

# node modules

> Each file is a module — dependencies resolve at runtime via `require` / `import`, not a C-style linker.

## Interview Relevance

Interviewers use **node modules** to check whether you can explain the mechanism in plain words and apply it under failure. Expect follow-ups on **require cache**, **CJS vs ESM**, **exports**.

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

## Real-World Applications

In production APIs and tooling, **node modules** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **Circular requires** — partial exports; redesign or lazy require; **Global leaks** — assignment without `const`/`let`/`var` still pollutes in sloppy mode.

## Pros/Cons or Trade-offs

- **Pro:** Solves the job described above when used in the right layer (Each file is a module — dependencies resolve at runtime via `require` / `import`…).
- **Con / when not:** **Browser bundles** — bundler graph differs; don’t assume Node resolution.

## Comparison

vs [[node package json]]: know when each applies — do not treat them as interchangeable. vs [[npm command]]: know when each applies — do not treat them as interchangeable. vs [[Runtime Errors]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid

- **Circular requires** — partial exports; redesign or lazy require.
- **Global leaks** — assignment without `const`/`let`/`var` still pollutes in sloppy mode.
- **ERR_REQUIRE_ESM:** check CJS requiring ESM; fix: Dynamic `import()` or convert
- **Duplicate copies:** check Nested node_modules; fix: Deduplicate; check peer deps
- **Stale mock in tests:** check require cache; fix: `delete require.cache[…]`
- **Wrong file:** check Extension / exports map; fix: Check `package.json` exports
