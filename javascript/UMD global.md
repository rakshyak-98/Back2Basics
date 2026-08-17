[[javascript]] [[AMD module]] [[IIFC]] [[node modules]]

# UMD global

> Universal Module Definition — one file that works as AMD, CommonJS, or a browser global.





## Interview Relevance
Interviewers use **UMD global** to check whether you can explain the mechanism in plain words and apply it under failure. Expect follow-ups on **UMD**, **global**, **factory**.

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

## Real-World Applications
In production APIs and tooling, **UMD global** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **UMD isn’t ESM** — named exports / tree-shaking suffer; publish ESM when you can; **Global pollution** — choose unique names.

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Universal Module Definition — one file that works as AMD, CommonJS, or a browser…).
- **Con / when not:** **application code** — use ESM modules.
- **Con / when not:** **New libraries** — dual ESM/CJS via `package.json` `exports` beats hand UMD.

## Comparison
vs [[AMD module]]: know when each applies — do not treat them as interchangeable. vs [[IIFC]]: know when each applies — do not treat them as interchangeable. vs [[node modules]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid
- **UMD isn’t ESM** — named exports / tree-shaking suffer; publish ESM when you can.
- **Global pollution** — choose unique names.
- **`MyLib is not defined`:** check Wrong global name / defer; fix: Match script order; check name
- **Broken in bundler:** check Treated as ESM wrongly; fix: Set correct module type
- **Duplicate globals:** check Two UMD copies; fix: Dedupe; peer deps
- **SSR `window` missing:** check Used window directly; fix: Use `self`/root param
