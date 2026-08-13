<!-- note-strategy: operational -->
[[javascript]] [[prototype]] [[IIFC]]

# hoisting

> Declarations are visible in their scope before the line runs — `var`/`function` hoist differently from `let`/`const`.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** `function` declarations hoist fully; `var` hoists as `undefined`; `let`/`const` hoist to TDZ until initialized — access throws.

```txt
console.log(a) // undefined with var; TDZ ReferenceError with let
var a = 1
let b = 2
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **TDZ** | Temporal dead zone | “Binding exists but unread until init.” |
| **function decl** | Hoisted body | “Can call above definition.” |
| **function expr** | Not hoisted as fn | “`const f = () =>` is TDZ like const.” |

## Standard config / commands

```js
// Prefer
const x = 1
function f() {}
// Avoid relying on var hoisting
```

| Form | Before init |
|------|-------------|
| `var` | `undefined` |
| `let`/`const` | TDZ error |
| `function foo(){}` | Callable |
| `const foo = function(){}` | TDZ |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `undefined` unexpectedly | `var` use-before-assign | Use `let`/`const`; reorder |
| ReferenceError TDZ | `let` before line | Move declaration up |
| Not a function | Called const fn before init | Reorder |
| Duplicate decl errors | Redeclare `let` | One binding |

---

## Gotchas

> [!WARNING]
> **`var` in loops with async** — classic closure bug; use `let`.

> [!WARNING]
> **Class declarations** — also TDZ until evaluated.

---

## When NOT to use

- **Designing APIs around hoisting** — write top-down clarity instead.
- **`var` in new code** — prefer `let`/`const`.

---

## Related

[[prototype]] [[IIFC]] [[self-defining functions]]
