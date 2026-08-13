[[javascript]] [[AMD module]] [[IIFC]] [[node modules]]

# UMD global

> Universal Module Definition — one file that works as AMD, CommonJS, or a browser global.

---

## How it works

```txt
(typeof exports…) ? CJS
: (typeof define=== 'function' && define.amd) ? AMD
: root.Lib = factory()
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **UMD** | Multi-loader wrapper | “One artifact, many loaders.” |
| **global** | `window.Lib` | “Script-tag fallback.” |
| **factory** | Build the export | “Shared body for all targets.” |


## Configuration and commands

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

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| `MyLib is not defined` | Wrong global name / defer | Match script order; check name |
| Broken in bundler | Treated as ESM wrongly | Set correct module type |
| Duplicate globals | Two UMD copies | Dedupe; peer deps |
| SSR `window` missing | Used window directly | Use `self`/root param |

---


## Gotchas

> [!WARNING]
> **UMD isn’t ESM** — named exports / tree-shaking suffer; publish ESM when you can.

> [!WARNING]
> **Global pollution** — choose unique names.

---


## When not to use

- **application code** — use ESM modules.
- **New libraries** — dual ESM/CJS via `package.json` `exports` beats hand UMD.

---


## Related

[[AMD module]] [[IIFC]] [[node modules]]

## Sources

- [Wikipedia — UMD global](https://en.wikipedia.org/wiki/UMD_global)
