[[Descriptive/JavaScript/function]] [[Descriptive/JavaScript/new]] [[javascript]] [[Operating System/Stack Frame]]

# Execution context

> The environment in which JavaScript runs a chunk of code — variables, `this`, outer scope, and hoisting — **ECMAScript spec + debugger mental model**.

## Mental model

Every time JS runs code, the engine creates an **execution context** on the **call stack**. Contexts nest: global first, then each function call, then blocks (let/const) in modern engines.

```
Call stack (top = running now):

  ┌─────────────────────┐
  │ foo() context       │  ← Lexical env: locals, params
  │  this, LexicalEnv   │  ← Outer env → bar's scope
  ├─────────────────────┤
  │ bar() context       │
  ├─────────────────────┤
  │ global context      │  ← one per realm (window / module)
  └─────────────────────┘
```

| Phase (creation) | What happens |
|------------------|--------------|
| **Creation** | Allocate env record, bind `this`, setup outer reference, hoist `var`/functions |
| **Execution** | Run statements line by line |

**Global context:** one per script/module — top-level `let`/`const` live in script scope, not `window` (in modules).

## Standard config / commands

### Observe scope chain in debugger

```javascript
const globalVar = 'g';

function outer() {
  const outerVar = 'o';
  function inner() {
    const innerVar = 'i';
    debugger; // inspect Closure / Scope in DevTools
    return innerVar + outerVar + globalVar;
  }
  return inner();
}
outer();
```

### `this` differs by call site (same function, new context each call)

```javascript
function show() { console.log(this); }
show();           // strict: undefined; sloppy: global
const obj = { show };
obj.show();       // obj
show.call(42);    // Number(42)
```

### Module vs script global

```javascript
// ESM module — own top-level scope, strict mode always
export const x = 1;
// var y = 2;  // not property of globalThis
```

### Temporal dead zone

```javascript
console.log(a); // ReferenceError (let hoisted but uninitialized)
let a = 1;
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `ReferenceError: x is not defined` | Variable not in scope chain | Declare in outer scope or pass as arg |
| Wrong `this` in callback | Lost binding | Arrow fn, `.bind`, or wrapper |
| Stale closure in loop | `var` + async callback | Use `let` or IIFE |
| `Maximum call stack exceeded` | Infinite recursion | Base case; tail-call not guaranteed in JS |
| TDZ errors at module top | Access before `let` init | Reorder declarations |

## Gotchas

> [!WARNING]
> Closures keep the **entire lexical environment** alive — capturing large objects in nested callbacks causes memory leaks in long-lived servers.

- **`var` hoists to function context; `let`/`const` hoist to block** — different TDZ behavior.
- **Eval** can mutate outer lexical env in non-strict legacy code — avoid.
- **Async functions** suspend, pop stack, resume later — context restored via continuation, not same stack frame.
- **Multiple globals:** iframes, workers, Node vm — separate contexts, separate globals.

## When NOT to use

- Don't manually simulate contexts — use modules, closures, and classes instead of `with` or dynamic scoping hacks.

## Related

[[Descriptive/JavaScript/function]] [[Descriptive/JavaScript/constructor function]] [[Operating System/Stack Frame]] [[javascript]]
