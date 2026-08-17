[[javascript/polyfills]] [[javascript]] [[Descriptive/JavaScript/javascript web API]] [[npm]] [[polyfills]]

# Polyfilling

> Polyfilling — transpiling rewrites syntax (class → function). Polyfilling adds missing functions or prototypes at runtime. No syntax change — only implementation.

```txt
        Polyfilling ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Why It Matters
- **Key signal:** Polyfill reviews cover shipping modern APIs on old runtimes

## Sources
- [MDN Web Docs](https://developer.mozilla.org/) — overview

## Key Concepts
- **Note:** **Transpiling** rewrites syntax (`class` → function). **Polyfilling** adds **…

```
Target browsers (IE11, old Safari)
        │
        ▼
- **Note:** Bundle: your app + polyfills (Promise, Array.prototype.flat, fetch)
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

## Technical Details
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

- Prefer specification-accurate implementations from core-js over hand-rolled s…

### Check support before shipping

- [ECMAScript compat table](https://compat-table.github.io/compat-table/es6/)
- [Can I use](https://caniuse.com/) for Web APIs (`fetch`, `IntersectionObserve…

### Node version baseline

- Node 18+ includes `fetch`, `structuredClone`

## Mistakes to Avoid
> [!WARNING]
> **Mutating prototypes** affects all code in the page including third-party libs — order polyfills before app code.

- **Mistake:** **`Object.prototype` pollution** from bad polyfills breaks `for.…
- **Mistake:** **Frozen environments** (SES, some embeds) forbid polyfills
- **Mistake:** **polyfill.io supply-chain history**

| Symptom | Check | Fix |
|---------|-------|-----|
| `X is not a function` in old browser | Missing polyfill | Add feature to Babel `useBuiltIns` or import |
| Polyfill conflicts with native | Double-patching | Feature detect `if (!Array.prototype.flat)` |
| Bundle size exploded | Full `core-js/stable` | Switch to `usage` + narrow `targets` |
| Subtle spec mismatch | Hand-rolled shim | Replace with core-js |
| CSP blocks CDN polyfill | Inline script policy | Self-host bundle |

## Pros/Cons or Trade-offs
- Internal apps on locked Chrome version — set baseline, skip polyfills.
- Syntax-only gaps — use Babel/TypeScript transpile, not polyfill.
- Server Node with pinned LTS — upgrade runtime instead of patching `fetch`.
