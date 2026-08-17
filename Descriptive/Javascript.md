[[Descriptive]] [[javascript]] [[Asynchronous]] [[Call stack]] [[promise]] [[typescript]]

# Javascript

> JavaScript — language of the browser (and Node): single-threaded event loop, prototypes, and first-class functions.

```txt
        Javascript ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Interview Relevance
- **Interview probes:** JavaScript interviews span runtime model

## Sources
- [MDN Web Docs](https://developer.mozilla.org/) — overview

## Key Concepts
```txt
call stack ←→ heap
     ↑
event loop ← tasks / microtasks
```

| Runtime | Role |
|---------|------|
| Browser | DOM + Web APIs |
| Node | FS/network modules |
| Workers | Parallel JS |

## Technical Details
```bash
node -e 'console.log(1)'
node --watch app.js
```

| Knob | Why it matters |
|------|----------------|
| `"use strict"` / modules | Safer defaults |
| Engine (V8) | Perf quirks |
| Bundler | Ship size |

## Mistakes to Avoid
> [!WARNING]
> **`==` coercion** — prefer `===`.

> [!WARNING]
> **Floating point** — money needs decimals/integers.

| Symptom | Check | Fix |
|---------|-------|-----|
| UI freeze | Sync heavy work | Worker / split |
| Unhandled rejection | Missing catch | Attach handlers |
| `undefined is not a function` | Wrong type/import | Log; fix export |
| Module not found | Path/CJS/ESM | Align module type |

## Pros/Cons or Trade-offs
- **CPU-bound HPC** — native/Go/Rust.
- **Shared-memory threads model** — careful with workers.
