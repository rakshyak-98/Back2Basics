[[Lexical environment]] [[hoisting]] [[primitive non-primitive values]] [[abstract storage location]] [[javascript engine]]

# Variable (JavaScript)

> **Named binding** in a lexical environment — holds a value (primitive or reference) — mutability rules depend on `var` / `let` / `const` — **ECMA-262**.

---

## Mental model

A variable is not the value itself — it's an **identifier bound** in an Environment Record ([[Lexical environment]]):

```txt
let count = 42        → binding "count" → Number 42
let user = { id: 1 }  → binding "user" → reference to object in heap
```

| Declaration | Scope | Reassign | Hoist behavior |
|-------------|-------|----------|----------------|
| `var` | Function | Yes | Hoisted, init `undefined` ([[hoisting]]) |
| `let` | Block | Yes | TDZ until line runs |
| `const` | Block | No rebinding | TDZ; object contents mutable |

Primitives ([[primitive non-primitive values]]) copy by value; objects copy **reference** — two vars can alias same object.

---

## Standard config / commands

```javascript
const API_URL = import.meta.env.VITE_API_URL; // prefer const for fixed refs
let retries = 0;                               // mutate when needed

function increment() {
  retries += 1; // reassign binding
}

const state = { count: 0 };
state.count += 1; // OK — mutating object, not rebinding `state`

// Destructuring = new bindings
const { name, ...rest } = user;
```

### Avoid implicit globals

```javascript
"use strict";
function leak() {
  // accidentalGlobal = 1; // ReferenceError in strict mode
}
```

### Naming for intent

```txt
UPPER_SNAKE   → module-level constants
camelCase     → variables and functions
PascalCase    → constructors / React components
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `ReferenceError: x before initialization` | TDZ / temporal dead zone | Declare before use; check block scope |
| Unexpected `undefined` | Hoisted `var` | Switch to `let`/`const` |
| Mutation surprises | Shared object reference | Clone `{ ...obj }` or structuredClone |
| `Assignment to constant` | Reassign `const` | Use `let` or mutate property intentionally |
| Global pollution | Missing declaration | `"use strict"`; ESLint no-undef |

---

## Gotchas

> [!WARNING]
> **`const` ≠ immutable object** — freezes binding, not deep object graph.

> [!WARNING]
> **Loop `var` closures** — classic setTimeout prints same index; use `let`.

---

## When NOT to use

- **`var` in new code** — no benefit over `let`/`const`.
- **Reassigning everywhere** — prefer smaller scopes and derived values ([[React State management]] patterns).

---

## Related

[[Lexical environment]] · [[hoisting]] · [[primitive non-primitive values]] · [[abstract storage location]] · [[Destructuring]]
