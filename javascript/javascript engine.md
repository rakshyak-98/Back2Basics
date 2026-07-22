[[Event Loop]] [[Descriptive/JavaScript/pre-parser]] [[wasm]] [[SWC]] [[NodeJS]]

# JavaScript engine

> Parses JS → bytecode/IR → executes on **call stack** + **heap**, coordinated by the **event loop** — V8 (Chrome/Node), SpiderMonkey (Firefox), JavaScriptCore (Safari).

---

## Mental model

Pipeline (simplified):

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
| **Hermes** | React Native (mobile bundle) |

Gecko is Firefox's **layout/rendering** engine; **SpiderMonkey** is its JS engine — check `about:support` / `about:buildconfig` in Firefox.

Node uses **V8** + libuv for I/O — same language, different embed API than browser ([[NodeJS]]).

---

## Standard config / commands

### Inspect V8 flags (Node)

```bash
node --v8-options | head
node --trace-opt --trace-deopt app.js   # deopt debugging (verbose)
node --max-old-space-size=4096 app.js # heap cap
```

### Chrome DevTools Performance

Record → Main thread → see **Parse HTML / Compile Script / Evaluate** — long yellow blocks = parse/compile cost.

### Feature detection (not engine sniffing)

```javascript
if ("structuredClone" in globalThis) { /* use */ }
// Avoid navigator.userAgent branching for language features
```

Prefer **Babel/target** ([[SWC]]) for syntax, polyfills ([[polyfills]]) for missing builtins.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Slow first load | Parse/compile huge bundle | Code-split; [[SWC]] minify; defer non-critical |
| Works Chrome, fails Safari | JSC semantics / date parsing | Test WebKit; avoid non-standard extensions |
| Memory climb | Detached DOM, closures | Heap snapshot in DevTools |
| Deopt storms | Polymorphic hot functions | Stable object shapes; avoid `delete` on props |
| Different Node vs browser | API surface | `globalThis` checks; separate builds |

---

## Gotchas

> [!WARNING]
> **User-agent engine detection** — brittle; use feature detects + integration tests.

> [!WARNING]
> **Micro-optimizing for one engine** — V8-specific tricks may hurt JSC or future versions.

---

## When NOT to use

- **Choosing framework** — engine differences rarely matter vs architecture.
- **Security boundaries** — sandbox with CSP/isolation, not "pick V8 version".

---

## Related

[[Event Loop]] · [[Lexical environment]] · [[wasm]] · [[SWC]] · [[polyfills]] · [[web workers]]
