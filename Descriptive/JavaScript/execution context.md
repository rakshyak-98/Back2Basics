[[Descriptive/JavaScript/function]] [[Descriptive/JavaScript/new]] [[javascript]] [[Operating System/Stack Frame]] [[Descriptive/JavaScript/constructor function]]

# Execution context

> The environment in which JavaScript runs a chunk of code — variables, `this`, outer scope, and hoisting — **ECMAScript spec + debugger mental model**.

```txt
        Execution context ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Interview Relevance
- **Interview probes:** Execution context interviews cover lexical environments, this binding, and ho…

## Sources
- [MDN Web Docs](https://developer.mozilla.org/) — overview

## Key Concepts
- **Note:** Every time JS runs code, the engine creates an **execution context** on the *…

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

- **Note:** **Global context:** one per script/module

## Technical Details
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

## Mistakes to Avoid
> [!WARNING]
> Closures keep the **entire lexical environment** alive — capturing large objects in nested callbacks causes memory leaks in long-lived servers.

- **Mistake:** **`var` hoists to function context
- **Mistake:** **Eval** can mutate outer lexical environment in non-strict lega…
- **Mistake:** **Async functions** suspend, pop stack, resume later
- **Mistake:** **Multiple globals:** iframes, workers, Node vm

| Symptom | Check | Fix |
|---------|-------|-----|
| `ReferenceError: x is not defined` | Variable not in scope chain | Declare in outer scope or pass as arg |
| Wrong `this` in callback | Lost binding | Arrow fn, `.bind`, or wrapper |
| Stale closure in loop | `var` + async callback | Use `let` or IIFE |
| `Maximum call stack exceeded` | Infinite recursion | Base case; tail-call not guaranteed in JS |
| TDZ errors at module top | Access before `let` init | Reorder declarations |

## Pros/Cons or Trade-offs
- Don't manually simulate contexts
