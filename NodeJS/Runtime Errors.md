[[NodeJS]] [[Error handeling]] [[node modules]] [[node error]]

# Runtime Errors

> Common Node runtime failures — await/module-mode mistakes, ESM path helpers, and `super()` order in custom errors.

## Mental model

**Say it in one breath:** Most “mysterious” Node errors are mode mismatches (CJS versus ESM) or using APIs before the language allows them (`await`, `super`).

```txt
CJS: require, __dirname     ESM: import, import.meta.url
await: async fn or ESM top-level — not bare CJS top-level
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **Top-level await** | `await` at file top | “ESM yes; CJS no.” |
| --- | --- | --- |
| **`import.meta.url`** | Module URL | “Build `__dirname` yourself in ESM.” |
| **`super()` first** | Derived ctor rule | “Touch `this` only after super.” |

## Standard config / commands

```js
// ESM __dirname
import path from 'node:path'
import { fileURLToPath } from 'node:url'
const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

// Custom error — super before this
class AppError extends Error {
  constructor(statusCode, message) {
    super(message)
    this.name = this.constructor.name
    this.statusCode = statusCode
  }
}
```

| Error text | Likely cause |

| `await is only valid in async…` | CJS top-level await |
| --- | --- |
| `__dirname is not defined` | ESM without polyfill |
| `Must call super constructor…` | `this` before `super()` |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| await at top fails | `"type"` / extension | Use ESM or wrap async main |
| `__dirname` crash | ESM file | `fileURLToPath(import.meta.url)` |
| Error subclass throws | ctor order | `super` then `this` |
| sudo needs TTY | CI `sudo nginx -t` | NOPASSWD or non-interactive `-S` |

## Gotchas

> [!WARNING]
> **Mixing CJS require of ESM** — `ERR_REQUIRE_ESM`; use dynamic `import()`.

> [!WARNING]
> **Deploy sudo prompts** — non-interactive shells can’t type passwords.

## When NOT to use

- This is a **symptom catalog** — for intentional error design see [[Error handeling]].

## Related

[[Error handeling]] [[node modules]] [[node error]] [[Node.js run as a non-privileged user]]
