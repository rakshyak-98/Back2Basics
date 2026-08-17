[[variable]] [[hoisting]] [[Descriptive/JavaScript/execution context]] [[javascript engine]] [[Callback]] [[referential equality]]

# Lexical environment

> Lexical environment — each scope (function, block, module) has a Lexical Environment:





## Interview Relevance
Interviewers use **Lexical environment** to check whether you can explain the mechanism in plain words and apply it under failure. Expect follow-ups on **Lexical scope**, **`var`**.

## Sources
- [ECMA-262 — Lexical Environments](https://tc39.es/ecma262/#sec-lexical-environments) — deep-dive
- [Wikipedia — Lexical environment](https://en.wikipedia.org/wiki/Lexical_environment) — overview

## Core Definition
Each scope (function, block, module) has a **Lexical Environment**:

## Key Concepts
- **Lexical scope:** Defined by source text nesting — | **Closure**
- **`var`:** Function-scoped; hoisted ([[hoisting]]) — | **`let`/`const`**

## Technical Details
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

```javascript
function outer() {
  const a = 1;
  function inner() { console.log(a); } // closes over outer's env
  return inner;
}
```

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

## Real-World Applications
In production APIs and tooling, **Lexical environment** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **`var` in blocks** — leaks to function scope; legacy footgun in loops + timeouts; **Dynamic `eval`** — can mutate lexical bindings in non-strict legacy modes; avoid.

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Lexical environment — each scope (function, block, module) has a Lexical Environ…).
- **Con / when not:** **Explaining to juniors** — start with "scope chain" intuition; specification terms second.
- **Con / when not:** **Performance micro-hacks** — engines optimize closures; don't flatten scopes manually without profiling.

## Comparison
vs [[variable]]: know when each applies — do not treat them as interchangeable. vs [[hoisting]]: know when each applies — do not treat them as interchangeable. vs [[Descriptive/JavaScript/execution context]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid
- **`var` in blocks** — leaks to function scope; legacy footgun in loops + timeouts.
- **Dynamic `eval`** — can mutate lexical bindings in non-strict legacy modes; avoid.
- **`undefined` before assignment:** check `var` hoisting; fix: Use `let`; declare before use
- **Loop closure same index:** check Shared `var` binding; fix: `let i` in for-loop or IIFE
- **Cannot access before init:** check TDZ with `const`; fix: Reorder declarations
- **Unexpected global leak:** check Bare assignment; fix: `"use strict"`; declare with `let`
- **Stale closure in React:** check Captured old state; fix: Functional updates; refs ([[referential equality]])
