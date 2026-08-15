[[NodeJS]] [[Error handeling]] [[node modules]] [[node error]] [[Node.js run as a non-privileged user]]

# Runtime Errors

> Common Node runtime failures — await/module-mode mistakes, ESM path helpers, and `super()` order in custom errors.

## Interview Relevance

Interviewers use **Runtime Errors** to check whether you can explain the mechanism in plain words and apply it under failure. Expect follow-ups on **Top-level await**, **`import.meta.url`**, **`super()` first**.

## Sources

- [Wikipedia — Runtime Errors](https://en.wikipedia.org/wiki/Runtime_Errors) — overview

## Key Concepts

- **Top-level await:** `await` at file top — ESM yes; CJS no.
- **`import.meta.url`:** Module URL — Build `__dirname` yourself in ESM.
- **`super()` first:** Derived ctor rule — Touch `this` only after super.

## Technical Details

```txt
CJS: require, __dirname     ESM: import, import.meta.url
await: async fn or ESM top-level — not bare CJS top-level
```

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
|------------|--------------|
| `await is only valid in async…` | CJS top-level await |
| `__dirname is not defined` | ESM without polyfill |
| `Must call super constructor…` | `this` before `super()` |

## Real-World Applications

In production APIs and tooling, **Runtime Errors** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **Mixing CJS require of ESM** — `ERR_REQUIRE_ESM`; use dynamic `import()`; **Deploy sudo prompts** — non-interactive shells can’t type passwords.

## Pros/Cons or Trade-offs

- **Pro:** Solves the job described above when used in the right layer (Common Node runtime failures — await/module-mode mistakes, ESM path helpers, and…).
- **Con / when not:** This is a **symptom catalog** — for intentional error design see [[Error handeling]].

## Comparison

vs [[Error handeling]]: know when each applies — do not treat them as interchangeable. vs [[node modules]]: know when each applies — do not treat them as interchangeable. vs [[node error]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid

- **Mixing CJS require of ESM** — `ERR_REQUIRE_ESM`; use dynamic `import()`.
- **Deploy sudo prompts** — non-interactive shells can’t type passwords.
- **await at top fails:** check `"type"` / extension; fix: Use ESM or wrap async main
- **`__dirname` crash:** check ESM file; fix: `fileURLToPath(import.meta.url)`
- **Error subclass throws:** check ctor order; fix: `super` then `this`
- **sudo needs TTY:** check CI `sudo nginx -t`; fix: NOPASSWD or non-interactive `-S`
