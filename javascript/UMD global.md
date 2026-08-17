[[javascript]] [[AMD module]] [[IIFC]] [[node modules]]

# UMD global

> Universal Module Definition — one file that works as AMD, CommonJS, or a browser global.

```txt
        UMD global ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers use **UMD global** to check whether you can explain the mechanis…

## Sources
- [umdjs/umd](https://github.com/umdjs/umd) — overview
- [Wikipedia — UMD global](https://en.wikipedia.org/wiki/UMD_global) — overview

## Key Concepts
- **UMD:** Multi-loader wrapper — One artifact, many loaders.
- **global:** `window.Lib` — Script-tag fallback.
- **factory:** Build the export — Shared body for all targets.

## Technical Details
```txt
(typeof exports…) ? CJS
: (typeof define=== 'function' && define.amd) ? AMD
: root.Lib = factory()
```

```js
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory()
  else if (typeof define === 'function' && define.amd) define([], factory)
  else root.MyLib = factory()
})(typeof self !== 'undefined' ? self : this, function () {
  return { version: '1.0.0' }
})
```

| Knob | Why it matters |
|------|----------------|
| Bundler `umd` target | Rollup/webpack library mode |
| Global name | Avoid collisions |
| ESM dual publish | Modern packages prefer `exports` map |

## Mistakes to Avoid
- **Mistake:** **UMD isn’t ESM**
- **Mistake:** **Global pollution** — choose unique names
- **Mistake:** **`MyLib is not defined`:** check Wrong global name / defer
- **Mistake:** **Broken in bundler:** check Treated as ESM wrongly
- **Mistake:** **Duplicate globals:** check Two UMD copies
- **Mistake:** **SSR `window` missing:** check Used window directly

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Universal Module Definition — one file that works as AMD, CommonJS, or a browser…).
- **Con / when not:** **application code** — use ESM modules.
- **Con / when not:** **New libraries**

## Comparison
- vs [[AMD module]]: know when each applies


### Use cases
- In production APIs and tooling, **UMD global** shows up whenever teams ship N…
