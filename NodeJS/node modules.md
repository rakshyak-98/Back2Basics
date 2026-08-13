<!-- note-strategy: operational -->
[[NodeJS]] [[node package json]] [[npm command]]

# node modules

> Each file is a module — dependencies resolve at runtime via `require` / `import`, not a C-style linker.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** CommonJS loads on first `require` and caches the `exports`; ESM is static/`import` with live bindings. No separate link step — resolution is at load time.

```txt
app.js ──require/import──► ./lib.js (cached after first load)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **require cache** | Singleton per resolved path | “Mutating exports affects everyone.” |
| **CJS vs ESM** | `require` vs `import` | “TLA and `__dirname` differ.” |
| **exports** | Public surface | “Only export what callers need.” |

## Standard config / commands

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

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| ERR_REQUIRE_ESM | CJS requiring ESM | Dynamic `import()` or convert |
| Duplicate copies | Nested node_modules | Deduplicate; check peer deps |
| Stale mock in tests | require cache | `delete require.cache[…]` |
| Wrong file | Extension / exports map | Check `package.json` exports |

---

## Gotchas

> [!WARNING]
> **Circular requires** — partial exports; redesign or lazy require.

> [!WARNING]
> **Global leaks** — assignment without `const`/`let`/`var` still pollutes in sloppy mode.

---

## When NOT to use

- **Browser bundles** — bundler graph differs; don’t assume Node resolution.

---

## Related

[[node package json]] [[npm command]] [[Runtime Errors]]
