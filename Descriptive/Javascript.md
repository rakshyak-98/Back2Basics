[[Descriptive]] [[javascript]] [[Asynchronous]]

# Javascript

> JavaScript — language of the browser (and Node): single-threaded event loop, prototypes, and first-class functions.

---

## How it works

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

---


## Configuration and commands

```bash
node -e 'console.log(1)'
node --watch app.js
```

| Knob | Why it matters |
|------|----------------|
| `"use strict"` / modules | Safer defaults |
| Engine (V8) | Perf quirks |
| Bundler | Ship size |

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| UI freeze | Sync heavy work | Worker / split |
| Unhandled rejection | Missing catch | Attach handlers |
| `undefined is not a function` | Wrong type/import | Log; fix export |
| Module not found | Path/CJS/ESM | Align module type |

---


## Gotchas

> [!WARNING]
> **`==` coercion** — prefer `===`.

> [!WARNING]
> **Floating point** — money needs decimals/integers.

---


## When not to use

- **CPU-bound HPC** — native/Go/Rust.
- **Shared-memory threads model** — careful with workers.

---


## Related

[[Asynchronous]] [[Call stack]] [[promise]] [[typescript]]

## Sources

- [Wikipedia — Javascript](https://en.wikipedia.org/wiki/Javascript)
