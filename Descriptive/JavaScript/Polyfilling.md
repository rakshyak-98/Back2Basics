[[javascript/polyfills]] [[javascript]] [[Descriptive/JavaScript/javascript web API]] [[npm]]

# Polyfilling

> Ship missing runtime APIs via script — fill gaps older browsers/Node versions lack — **compat tables + core-js / polyfill.io**.

## Mental model

**Transpiling** rewrites syntax (`class` → function). **Polyfilling** adds **missing functions or prototypes** at runtime. No syntax change — only implementation.

```
Target browsers (IE11, old Safari)
        │
        ▼
Bundle: your app + polyfills (Promise, Array.prototype.flat, fetch)
        │
        └── feature detect OR build-time target list
```

| Approach | When |
|----------|------|
| **Global polyfill** | `import 'core-js/stable'` — patches prototypes |
| **Selective** | `import 'core-js/features/array/flat'` |
| **CDN service** | polyfill.io (legacy) — URL with `features=` list |
| **Native only** | Modern baseline — no polyfill, smaller bundle |

See also: [[polyfills]] (companion note on mechanics).

## Standard config / commands

### Browsers — core-js + Babel preset-env

```bash
npm i core-js
```

```javascript
// entry.js (before other imports)
import 'core-js/stable';
import 'regenerator-runtime/runtime'; // if async/generators needed
```

```json
// babel.config.json
{
  "presets": [["@babel/preset-env", {
    "useBuiltIns": "usage",
    "corejs": 3,
    "targets": "> 0.5%, not dead"
  }]]
}
```

### Manual feature detect + load

```javascript
if (!Array.prototype.at) {
  Array.prototype.at = function (n) {
    n = Math.trunc(n) || 0;
    if (n < 0) n += this.length;
    return this[n];
  };
}
```

Prefer spec-accurate implementations from core-js over hand-rolled shims.

### Check support before shipping

- [ECMAScript compat table](https://compat-table.github.io/compat-table/es6/)
- [Can I use](https://caniuse.com/) for Web APIs (`fetch`, `IntersectionObserver`)

### Node version baseline

Node 18+ includes `fetch`, `structuredClone` — polyfill only if supporting Node 16 LTS.

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `X is not a function` in old browser | Missing polyfill | Add feature to Babel `useBuiltIns` or import |
| Polyfill conflicts with native | Double-patching | Feature detect `if (!Array.prototype.flat)` |
| Bundle size exploded | Full `core-js/stable` | Switch to `usage` + narrow `targets` |
| Subtle spec mismatch | Hand-rolled shim | Replace with core-js |
| CSP blocks CDN polyfill | Inline script policy | Self-host bundle |

## Gotchas

> [!WARNING]
> **Mutating prototypes** affects all code in the page including third-party libs — order polyfills before app code.

- **`Object.prototype` pollution** from bad polyfills breaks `for...in` — never patch Object.prototype casually.
- **Frozen environments** (SES, some embeds) forbid polyfills — target native only.
- **polyfill.io supply-chain history** — self-host or npm, don't trust blind CDN in prod.

## When NOT to use

- Internal apps on locked Chrome version — set baseline, skip polyfills.
- Syntax-only gaps — use Babel/TypeScript transpile, not polyfill.
- Server Node with pinned LTS — upgrade runtime instead of patching `fetch`.

## Related

[[polyfills]] [[javascript]] [[Descriptive/JavaScript/javascript web API]] [[npm]]
