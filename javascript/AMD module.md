[[javascript]] [[UMD global]] [[node modules]] [[IIFC]]

# AMD module

> Asynchronous Module Definition — browser modules loaded via `define`/`require` (RequireJS era) before native ESM.

---

## How it works

```txt
define(['dep'], function (dep) { return api })
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **AMD** | Async browser modules | “RequireJS pattern.” |
| **define** | Register module | “Deps + factory.” |
| **vs CJS** | Sync `require` | “CJS grew on server; AMD on browsers.” |


## Configuration and commands

```js
define(['./math'], function (math) {
  return { run: () => math.add(1, 2) }
})

require(['app'], function (app) { app.start() })
```

| Knob | Why it matters |
|------|----------------|
| paths/shim config | Legacy non-AMD scripts |
| bundles | Fewer round trips |
| almond | Slim runtime for built code |

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| Timeout loading | Wrong baseUrl/paths | Fix RequireJS config |
| Undefined dep | Shim missing exports | `shim: { exports: '…' }` |
| Order bugs | Undeclared dep | List all deps explicitly |
| Mixed ESM | Modern import in AMD app | Migrate to bundler ESM |

---


## Gotchas

> [!WARNING]
> **Don’t start new apps on AMD** — native ESM is the standard.

> [!WARNING]
> **Anonymous define** — one per file; multiple confuse optimization.

---


## When not to use

- **New greenfield** — ESM.
- **Node services** — CJS/ESM, not RequireJS.

---


## Related

[[UMD global]] [[IIFC]] [[node modules]]

## Sources

- [Wikipedia — AMD module](https://en.wikipedia.org/wiki/AMD_module)
