[[Descriptive/JavaScript/Polyfilling]] [[javascript engine]] [[SWC]] [[React build]]

# Polyfills

> **Runtime implementation** of missing APIs on old engines — no syntax transform — fills the gap so **calling** `Array.prototype.at` works — **MDN + core-js**.

---

## Mental model

Two compatibility layers:

```txt
Syntax (optional chaining, class fields)  → transpiler ([[SWC]], Babel)
APIs (Promise.finally, structuredClone)   → polyfill script
```

Polyfill = shim that mimics spec behavior if `if (!Feature) { implement }`.

```txt
Transpile:  ?.  →  long helper code (syntax)
Polyfill:   Promise.allSettled  →  function added to prototype (API)
```

Ship polyfills only for **browsers you support** — unnecessary bytes on modern-only stacks.

---

## Standard config / commands

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

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `X is not a function` on old Safari | Missing polyfill | Add core-js module or manual shim |
| Polyfill but still syntax error | Need transpile not polyfill | [[SWC]]/`target` in tsconfig |
| Double polyfill conflict | Two libs patch same API | One provider (core-js) |
| Bundle huge | Import entire stable | Use `core-js/features/promise` only |
| Subtle spec mismatch | Hand-rolled shim incomplete | Use tested polyfill lib |

---

## Gotchas

> [!WARNING]
> **Polyfill ≠ transpile** — `?.` cannot be polyfilled; must compile away.

> [!WARNING]
> **Mutating prototypes** — can break if non-writable; order matters (load polyfills first).

---

## When NOT to use

- **Internal apps on latest Chrome only** — drop polyfills; set browserslist accordingly.
- **Node LTS with native API** — use `engines` in package.json instead.
- **Syntax features** — always transpile; don't "polyfill" classes with Function constructor hacks.

---

## Related

[[Descriptive/JavaScript/Polyfilling]] · [[javascript engine]] · [[SWC]] · [[React build]] · [[wasm]]
