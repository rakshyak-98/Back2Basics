[[Descriptive]] [[javascript]] [[Asynchronous]]

# Javascript

> JavaScript — language of the browser (and Node): single-threaded event loop, prototypes, and first-class functions.

## Mental model

**Say it in one breath:** Run-to-completion on one thread; async via task/microtask queues. Types are dynamic; use TypeScript when contracts matter.

```txt
call stack ←→ heap
     ↑
event loop ← tasks / microtasks
```

| Runtime | Role |
| --- | --- |
| Browser | DOM + Web APIs |
| Node | FS/network modules |
| Workers | Parallel JS |

## Standard config / commands

```bash
node -e 'console.log(1)'
node --watch app.js
```

| Knob | Why it matters |

| `"use strict"` / modules | Safer defaults |
| --- | --- |
| Engine (V8) | Perf quirks |
| Bundler | Ship size |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| UI freeze | Sync heavy work | Worker / split |
| Unhandled rejection | Missing catch | Attach handlers |
| `undefined is not a function` | Wrong type/import | Log; fix export |
| Module not found | Path/CJS/ESM | Align module type |

## Gotchas

> [!WARNING]
> **`==` coercion** — prefer `===`.

> [!WARNING]
> **Floating point** — money needs decimals/integers.

## When NOT to use

- **CPU-bound HPC** — native/Go/Rust.
- **Shared-memory threads model** — careful with workers.

## Related

[[Asynchronous]] [[Call stack]] [[promise]] [[typescript]]
