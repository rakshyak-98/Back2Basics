[[Lexical environment]] [[hoisting]] [[primitive non-primitive values]] [[abstract storage location]] [[javascript engine]] [[Destructuring]]

# Variable (JavaScript)

> Variable (JavaScript) — a variable is not the value itself — it's an identifier bound in an Environment Record (Lexical environment):

```txt
        Variable (JavaScri ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers probe **Variable (JavaScript)** to see if you understand what it…

## Sources
- [MDN — Declarations](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Grammar_and_types#declarations) — deep-dive
- [Wikipedia — variable](https://en.wikipedia.org/wiki/variable) — overview

## Key Concepts
- **A variable:** A variable is not the value itself
- **Primitives ([[primitive:** Primitives ([[primitive non-primitive values]]) copy by value; objects copy *…


- **Core:** A variable is not the value itself

## Technical Details
- A variable is not the value itself

```txt
let count = 42        → binding "count" → Number 42
let user = { id: 1 }  → binding "user" → reference to object in heap
```

| Declaration | Scope | Reassign | Hoist behavior |
|-------------|-------|----------|----------------|
| `var` | Function | Yes | Hoisted, init `undefined` ([[hoisting]]) |
| `let` | Block | Yes | TDZ until line runs |
| `const` | Block | No rebinding | TDZ; object contents mutable |

- Primitives ([[primitive non-primitive values]]) copy by value; objects copy *…

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

## Mistakes to Avoid
- **Mistake:** **`const` ≠ immutable object**
- **Mistake:** **Loop `var` closures**
- **Mistake:** **`ReferenceError: x before initialization`:** check TDZ / tempo…
- **Mistake:** **Unexpected `undefined`:** check Hoisted `var`
- **Mistake:** **Mutation surprises:** check Shared object reference
- **Mistake:** **`Assignment to constant`:** check Reassign `const`
- **Mistake:** **Global pollution:** check Missing declaration

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Variable (JavaScript) — a variable is not the value itself — it's an identifier …).
- **Con / when not:** **`var` in new code** — no benefit over `let`/`const`.
- **Con / when not:** **Reassigning everywhere**

## Comparison
- vs [[Lexical environment]]: know when each applies


### Use cases
- In production APIs and tooling, **variable** shows up whenever teams ship Nod…
