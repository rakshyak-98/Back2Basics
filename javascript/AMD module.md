[[javascript]] [[UMD global]] [[node modules]] [[IIFC]]

# AMD module

> Asynchronous Module Definition — browser modules loaded via `define`/`require` (RequireJS era) before native ESM.





## Interview Relevance
Interviewers use **AMD module** to check whether you can explain the mechanism in plain words and apply it under failure. Expect follow-ups on **AMD**, **define**, **vs CJS**.

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

## Real-World Applications
In production APIs and tooling, **AMD module** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **Don’t start new apps on AMD** — native ESM is the standard; **Anonymous define** — one per file; multiple confuse optimization.

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Asynchronous Module Definition — browser modules loaded via `define`/`require` (…).
- **Con / when not:** **New greenfield** — ESM.
- **Con / when not:** **Node services** — CJS/ESM, not RequireJS.

## Comparison
vs [[UMD global]]: know when each applies — do not treat them as interchangeable. vs [[node modules]]: know when each applies — do not treat them as interchangeable. vs [[IIFC]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid
- **Don’t start new apps on AMD** — native ESM is the standard.
- **Anonymous define** — one per file; multiple confuse optimization.
- **Timeout loading:** check Wrong baseUrl/paths; fix: Fix RequireJS config
- **Undefined dep:** check Shim missing exports; fix: `shim: { exports: '…' }`
- **Order bugs:** check Undeclared dep; fix: List all deps explicitly
- **Mixed ESM:** check Modern import in AMD app; fix: Migrate to bundler ESM
