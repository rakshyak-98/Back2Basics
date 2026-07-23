[[variable]] [[hoisting]] [[Descriptive/JavaScript/execution context]] [[javascript engine]] [[Callback]]

# Lexical environment

> Internal record holding **bindings** (variables, functions) + link to **outer** environment — scope is lexical, not dynamic — **ECMA-262 spec / You Don't Know JS**.

---

## Mental model

Each scope (function, block, module) has a **Lexical Environment**:

```txt
┌─────────────────────────────┐
│ Environment Record          │  ← local bindings (let, const, fn)
│ [[OuterEnv]] ───────────────┼──► parent scope (closure chain)
└─────────────────────────────┘
```

**Variable** access = walk the chain until name found ([[variable]]). You cannot inspect LexicalEnvironment objects from user code — engines implement them internally.

| Concept | Behavior |
|---------|----------|
| **Lexical scope** | Defined by source text nesting |
| **Closure** | Function + reference to outer env |
| **`var`** | Function-scoped; hoisted ([[hoisting]]) |
| **`let`/`const`** | Block-scoped; temporal dead zone until init |
| **Module scope** | Top-level `let` not global property |

```javascript
function outer() {
  const a = 1;
  function inner() { console.log(a); } // closes over outer's env
  return inner;
}
```

---

## Standard config / commands

### Block vs function scope

```javascript
function demo() {
  if (true) {
    var v = 1;
    let l = 2;
  }
  console.log(v); // 1
  // console.log(l); // ReferenceError
}
```

### TDZ (temporal dead zone)

```javascript
{
  // console.log(x); // ReferenceError
  let x = 10;
}
```

### Module doesn't pollute global

```javascript
// module.mjs
export const secret = 42;
// no window.secret in browser
```

Debug scope in DevTools **Scope** panel during breakpoint — practical view of environment records.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `undefined` before assignment | `var` hoisting | Use `let`; declare before use |
| Loop closure same index | Shared `var` binding | `let i` in for-loop or IIFE |
| Cannot access before init | TDZ with `const` | Reorder declarations |
| Unexpected global leak | Bare assignment | `"use strict"`; declare with `let` |
| Stale closure in React | Captured old state | Functional updates; refs ([[referential equality]]) |

---

## Gotchas

> [!WARNING]
> **`var` in blocks** — leaks to function scope; legacy footgun in loops + timeouts.

> [!WARNING]
> **Dynamic `eval`** — can mutate lexical bindings in non-strict legacy modes; avoid.

---

## When NOT to use

- **Explaining to juniors** — start with "scope chain" intuition; spec terms second.
- **Performance micro-hacks** — engines optimize closures; don't flatten scopes manually without profiling.

---

## Related

[[variable]] · [[hoisting]] · [[Descriptive/JavaScript/execution context]] · [[javascript engine]] · [[referential equality]]
