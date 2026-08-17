[[javascript]] [[UMD global]] [[node modules]] [[IIFC]]

# AMD module

> Asynchronous Module Definition — browser modules loaded via `define`/`require` (RequireJS era) before native ESM.

```txt
        AMD module ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers use **AMD module** to check whether you can explain the mechanis…

## Sources
- [RequireJS — Why AMD](https://requirejs.org/docs/whyamd.html) — overview
- [Wikipedia — AMD module](https://en.wikipedia.org/wiki/AMD_module) — overview

## Key Concepts
- **AMD:** Async browser modules — RequireJS pattern.
- **define:** Register module — Deps + factory.
- **vs CJS:** Sync `require` — CJS grew on server; AMD on browsers.

## Technical Details
```txt
define(['dep'], function (dep) { return api })
```

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

## Mistakes to Avoid
- **Mistake:** **Don’t start new apps on AMD** — native ESM is the standard
- **Mistake:** **Anonymous define**
- **Mistake:** **Timeout loading:** check Wrong baseUrl/paths
- **Mistake:** **Undefined dep:** check Shim missing exports
- **Mistake:** **Order bugs:** check Undeclared dep
- **Mistake:** **Mixed ESM:** check Modern import in AMD app

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Asynchronous Module Definition — browser modules loaded via `define`/`require` (…).
- **Con / when not:** **New greenfield** — ESM.
- **Con / when not:** **Node services** — CJS/ESM, not RequireJS.

## Comparison
- vs [[UMD global]]: know when each applies


### Use cases
- In production APIs and tooling, **AMD module** shows up whenever teams ship N…
