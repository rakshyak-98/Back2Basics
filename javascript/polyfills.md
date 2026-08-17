[[Descriptive/JavaScript/Polyfilling]] [[javascript engine]] [[SWC]] [[React build]] [[wasm]]

# Polyfills

> **Runtime implementation** of missing APIs on old engines — no syntax transform — fills the gap so **calling** `Array.prototype.at` works — **MDN + core-js**.

```txt
        Polyfills ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers probe **Polyfills** to see if you understand what it does operat…

## Sources
- [MDN — Polyfill](https://developer.mozilla.org/en-US/docs/Glossary/Polyfill) — overview
- [Wikipedia — polyfills](https://en.wikipedia.org/wiki/polyfills) — overview

## Key Concepts
- **Two compatibility:** Two compatibility layers:
- **Polyfill =:** Polyfill = shim that mimics specification behavior if `if (!Feature) { implem…
- **Ship polyfills:** Ship polyfills only for **browsers you support**

## Technical Details
- Two compatibility layers:

```txt
Syntax (optional chaining, class fields)  → transpiler ([[SWC]], Babel)
APIs (Promise.finally, structuredClone)   → polyfill script
```

- Polyfill = shim that mimics specification behavior if `if (!Feature) { implem…

```txt
Transpile:  ?.  →  long helper code (syntax)
Polyfill:   Promise.allSettled  →  function added to prototype (API)
```

- Ship polyfills only for **browsers you support**

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

- Generates modern + legacy chunks with polyfills auto-detected.

### Feature detect (preferred over UA sniff)

```javascript
if (!globalThis.structuredClone) {
  globalThis.structuredClone = (obj) => JSON.parse(JSON.stringify(obj)); // limited fallback
}
```

## Mistakes to Avoid
- **Mistake:** **Polyfill ≠ transpile**
- **Mistake:** **Mutating prototypes**
- **Mistake:** **`X is not a function` on old Safari:** check Missing polyfill
- **Mistake:** **Polyfill but still syntax error:** check Need transpile not po…
- **Mistake:** **Double polyfill conflict:** check Two libs patch same API
- **Mistake:** **Bundle huge:** check Import entire stable
- **Mistake:** **Subtle spec mismatch:** check Hand-rolled shim incomplete

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (**Runtime implementation** of missing APIs on old engines — no syntax transform …).
- **Con / when not:** **Internal apps on latest Chrome only**
- **Con / when not:** **Node LTS with native API**
- **Con / when not:** **Syntax features**

## Comparison
- vs [[Descriptive/JavaScript/Polyfilling]]: know when each applies


### Use cases
- In production APIs and tooling, **polyfills** shows up whenever teams ship No…
