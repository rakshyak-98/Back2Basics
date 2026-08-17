[[variable]] [[hoisting]] [[Descriptive/JavaScript/execution context]] [[javascript engine]] [[Callback]] [[referential equality]]

# Lexical environment

> Lexical environment — each scope (function, block, module) has a Lexical Environment:

```txt
        Lexical environmen ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers use **Lexical environment** to check whether you can explain the…

## Sources
- [ECMA-262 — Lexical Environments](https://tc39.es/ecma262/#sec-lexical-environments) — deep-dive
- [Wikipedia — Lexical environment](https://en.wikipedia.org/wiki/Lexical_environment) — overview

## Key Concepts
- **Lexical scope:** Defined by source text nesting — | **Closure**
- **`var`:** Function-scoped; hoisted ([[hoisting]]) — | **`let`/`const`**


- **Core:** Each scope (function, block, module) has a **Lexical Environment**:

## Technical Details
- Each scope (function, block, module) has a **Lexical Environment**:

```txt
┌─────────────────────────────┐
│ Environment Record          │  ← local bindings (let, const, fn)
│ [[OuterEnv]] ───────────────┼──► parent scope (closure chain)
└─────────────────────────────┘
```

- **Variable:** access = walk the chain until name found ([[variable]]).
- You cannot inspect LexicalEnvironment objects from user code

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

- Debug scope in DevTools **Scope** panel during breakpoint

## Mistakes to Avoid
- **Mistake:** **`var` in blocks**
- **Mistake:** **Dynamic `eval`**
- **Mistake:** **`undefined` before assignment:** check `var` hoisting
- **Mistake:** **Loop closure same index:** check Shared `var` binding
- **Mistake:** **Cannot access before init:** check TDZ with `const`
- **Mistake:** **Unexpected global leak:** check Bare assignment
- **Mistake:** **Stale closure in React:** check Captured old state

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Lexical environment — each scope (function, block, module) has a Lexical Environ…).
- **Con / when not:** **Explaining to juniors**
- **Con / when not:** **Performance micro-hacks**

## Comparison
- vs [[variable]]: know when each applies


### Use cases
- In production APIs and tooling, **Lexical environment** shows up whenever tea…
