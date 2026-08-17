[[Descriptive/JavaScript/Polyfilling]] [[javascript engine]] [[SWC]] [[React build]] [[wasm]]

# Polyfills

> **Runtime implementation** of missing APIs on old engines — no syntax transform — fills the gap so **calling** `Array.prototype.at` works — **MDN + core-js**.





## Interview Relevance
Interviewers probe **Polyfills** to see if you understand what it does operationally and when it is the wrong tool — not just the definition.

## Sources
- [MDN — Polyfill](https://developer.mozilla.org/en-US/docs/Glossary/Polyfill) — overview
- [Wikipedia — polyfills](https://en.wikipedia.org/wiki/polyfills) — overview

## Key Concepts
- Two compatibility layers:
- Polyfill = shim that mimics specification behavior if `if (!Feature) { implement }`.
- Ship polyfills only for **browsers you support** — unnecessary bytes on modern-only stacks.

## Technical Details
Two compatibility layers:

```txt
Syntax (optional chaining, class fields)  → transpiler ([[SWC]], Babel)
APIs (Promise.finally, structuredClone)   → polyfill script
```

Polyfill = shim that mimics specification behavior if `if (!Feature) { implement }`.

```txt
Transpile:  ?.  →  long helper code (syntax)
Polyfill:   Promise.allSettled  →  function added to prototype (API)
```

Ship polyfills only for **browsers you support** — unnecessary bytes on modern-only stacks.

### Manual minimal polyfill

```javascript
if (!Array.prototype.at) {
  Array.prototype.at = function (index) {
    const k = index >= 0 ? index : this.length + index;
    return k >= 0 && k < this.length ? this[k] : undefined;
  };
}
```

### core-js (bundled import)

```javascript
// Entry before app code (legacy support)
import "core-js/stable";
import "regenerator-runtime/runtime"; // generators if needed
```

### Vite legacy plugin

```bash
npm i @vitejs/plugin-legacy -D
```

```typescript
import legacy from "@vitejs/plugin-legacy";
export default defineConfig({
  plugins: [legacy({ targets: ["defaults", "not IE 11"] })],
});
```

Generates modern + legacy chunks with polyfills auto-detected.

### Feature detect (preferred over UA sniff)

```javascript
if (!globalThis.structuredClone) {
  globalThis.structuredClone = (obj) => JSON.parse(JSON.stringify(obj)); // limited fallback
}
```

## Real-World Applications
In production APIs and tooling, **polyfills** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **Polyfill ≠ transpile** — `?.` cannot be polyfilled; must compile away; **Mutating prototypes** — can break if non-writable; order matters (load polyfills first).

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (**Runtime implementation** of missing APIs on old engines — no syntax transform …).
- **Con / when not:** **Internal apps on latest Chrome only** — drop polyfills; set browserslist accordingly.
- **Con / when not:** **Node LTS with native API** — use `engines` in package.json instead.
- **Con / when not:** **Syntax features** — always transpile; don't "polyfill" classes with Function constructor hacks.

## Comparison
vs [[Descriptive/JavaScript/Polyfilling]]: know when each applies — do not treat them as interchangeable. vs [[javascript engine]]: know when each applies — do not treat them as interchangeable. vs [[SWC]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid
- **Polyfill ≠ transpile** — `?.` cannot be polyfilled; must compile away.
- **Mutating prototypes** — can break if non-writable; order matters (load polyfills first).
- **`X is not a function` on old Safari:** check Missing polyfill; fix: Add core-js module or manual shim
- **Polyfill but still syntax error:** check Need transpile not polyfill; fix: [[SWC]]/`target` in tsconfig
- **Double polyfill conflict:** check Two libs patch same API; fix: One provider (core-js)
- **Bundle huge:** check Import entire stable; fix: Use `core-js/features/promise` only
- **Subtle spec mismatch:** check Hand-rolled shim incomplete; fix: Use tested polyfill lib
