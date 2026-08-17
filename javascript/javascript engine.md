[[Event Loop]] [[Descriptive/JavaScript/pre-parser]] [[wasm]] [[SWC]] [[NodeJS]] [[Lexical environment]] [[polyfills]] [[web workers]]

# JavaScript engine

> JavaScript engine — source → parser → AST → interpreter (Ignition) → optimizing compiler (TurboFan/V8)

```txt
        JavaScript engine ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers use **JavaScript engine** to check whether you can explain the m…

## Sources
- [V8 — Docs](https://v8.dev/docs) — deep-dive
- [MDN — JS execution model](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Execution_model) — overview
- [Wikipedia — javascript engine](https://en.wikipedia.org/wiki/javascript_engine) — overview

## Key Concepts
- **V8:** Chrome, Edge, Node.js, Deno — | **SpiderMonkey**
- **JavaScriptCore:** Safari — | **Hermes**

## Technical Details
- Pipeline (simplified):

```txt
Source → parser → AST → interpreter (Ignition) → optimizing compiler (TurboFan/V8)
                ↓
         bytecode + inline caches
                ↓
    Call stack + heap + GC + [[Event Loop]] task queues
```

| Engine | Host |
|--------|------|
| **V8** | Chrome, Edge, Node.js, Deno |
| **SpiderMonkey** | Firefox (Gecko platform) |
| **JavaScriptCore** | Safari |

- Gecko is Firefox's **layout/rendering** engine; **SpiderMonkey** is its JS en…

- Node uses **V8** + libuv for I/O

### Inspect V8 flags (Node)

```bash
node --v8-options | head
node --trace-opt --trace-deopt app.js   # deopt debugging (verbose)
node --max-old-space-size=4096 app.js # heap cap
```

### Chrome DevTools Performance

- Record → Main thread → see **Parse HTML / Compile Script / Evaluate**

### Feature detection (not engine sniffing)

```javascript
if ("structuredClone" in globalThis) { /* use */ }
// Avoid navigator.userAgent branching for language features
```

- Prefer **Babel/target** ([[SWC]]) for syntax, polyfills ([[polyfills]]) for m…

## Mistakes to Avoid
- **Mistake:** **User-agent engine detection**
- **Mistake:** **Micro-optimizing for one engine**
- **Mistake:** **Slow first load:** check Parse/compile huge bundle
- **Mistake:** **Works Chrome, fails Safari:** check JSC semantics / date parsi…
- **Mistake:** **Memory climb:** check Detached DOM, closures
- **Mistake:** **Deopt storms:** check Polymorphic hot functions
- **Mistake:** **Different Node vs browser:** check API surface

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (JavaScript engine — source → parser → AST → interpreter (Ignition) → optimizing …).
- **Con / when not:** **Choosing framework**
- **Con / when not:** **Security boundaries**

## Comparison
- vs [[Event Loop]]: know when each applies


### Use cases
- In production APIs and tooling, **javascript engine** shows up whenever teams…
