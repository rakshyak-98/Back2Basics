[[Lexical environment]] [[hoisting]] [[primitive non-primitive values]] [[abstract storage location]] [[javascript engine]] [[Destructuring]]

# Variable (JavaScript)

> Variable (JavaScript) — a variable is not the value itself — it's an identifier bound in an Environment Record (Lexical environment):





## Interview Relevance
Interviewers probe **Variable (JavaScript)** to see if you understand what it does operationally and when it is the wrong tool — not just the definition.

## Sources
- [MDN — Declarations](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Grammar_and_types#declarations) — deep-dive
- [Wikipedia — variable](https://en.wikipedia.org/wiki/variable) — overview

## Core Definition
A variable is not the value itself — it's an **identifier bound** in an Environment Record ([[Lexical environment]]):

## Key Concepts
- A variable is not the value itself — it's an **identifier bound** in an Environment Record ([[Lexical environment]]):
- Primitives ([[primitive non-primitive values]]) copy by value; objects copy **reference** — two variables can alias same object.

## Technical Details
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

Primitives ([[primitive non-primitive values]]) copy by value; objects copy **reference** — two variables can alias same object.

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

## Real-World Applications
In production APIs and tooling, **variable** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **`const` ≠ immutable object** — freezes binding, not deep object graph; **Loop `var` closures** — classic setTimeout prints same index; use `let`.

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Variable (JavaScript) — a variable is not the value itself — it's an identifier …).
- **Con / when not:** **`var` in new code** — no benefit over `let`/`const`.
- **Con / when not:** **Reassigning everywhere** — prefer smaller scopes and derived values ([[React State management]] patterns).

## Comparison
vs [[Lexical environment]]: know when each applies — do not treat them as interchangeable. vs [[hoisting]]: know when each applies — do not treat them as interchangeable. vs [[primitive non-primitive values]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid
- **`const` ≠ immutable object** — freezes binding, not deep object graph.
- **Loop `var` closures** — classic setTimeout prints same index; use `let`.
- **`ReferenceError: x before initialization`:** check TDZ / temporal dead zone; fix: Declare before use; check block scope
- **Unexpected `undefined`:** check Hoisted `var`; fix: Switch to `let`/`const`
- **Mutation surprises:** check Shared object reference; fix: Clone `{ ...obj }` or structuredClone
- **`Assignment to constant`:** check Reassign `const`; fix: Use `let` or mutate property intentionally
- **Global pollution:** check Missing declaration; fix: `"use strict"`; ESLint no-undef
