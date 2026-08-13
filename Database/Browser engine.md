<!-- note-strategy: operational -->
[[Database]] [[content security policy]] [[ESM]]

# Browser engine

> A browser engine turns HTML/CSS/JS into pixels and a live DOM — layout + paint + script, not a database.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Parse HTML → build DOM/CSSOM → layout → paint → composite; JS mutates the DOM and can force reflows.

```txt
HTML/CSS/JS
    │
    ▼
  DOM + CSSOM → render tree → layout → paint → pixels
         ▲
         └── JS / DOM APIs / CSP rules
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **DOM** | Tree JS can read/write | “Script talks to the page through the DOM.” |
| **Layout / reflow** | Compute geometry | “Reading layout then writing style thrashing costs frames.” |
| **Paint / composite** | Draw layers | “Transform/opacity often stay on the compositor.” |
| **CSP** | Who may load/run what | “Engine enforces Content-Security-Policy.” |
| **ESM** | Static module graph | “Browser can prefetch deps; CJS isn’t native there.” |
| **CJS** | `require` sync modules | “Node-era; bundlers rewrite for browsers.” |

### Modules in one glance

| Kind | Load | Browser-native? |
|------|------|-----------------|
| **ESM** | Async + static imports | Yes |
| **CJS** | Sync + dynamic `require` | No (bundle or avoid) |

---

## Standard config / commands

```html
<script type="module" src="/app.js"></script>
```

```js
// ESM — static imports (browser + modern bundlers)
import { render } from './ui.js'
```

DevTools (Blink):

```txt
Performance → record  → long tasks / layout
Rendering   → paint flashing / layout shift regions
Application → Frames / CSP violations in Console
```

| Knob | Why it matters |
|------|----------------|
| `type="module"` | Enables ESM semantics in page |
| CSP headers | Blocks inline/script sources you didn’t allow |
| Forced sync layout | `offsetHeight` after style writes → jank |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Blank page / script blocked | Console CSP errors | Adjust CSP or stop inline script |
| Janky scroll/input | Performance profile | Reduce layout thrash; defer work |
| `require is not defined` | CJS in browser | Bundle to ESM or use native ESM |
| FOUC / wrong layout | CSS load order | Critical CSS; avoid late conflicting sheets |
| Module 404 waterfall | Network waterfalls | Correct paths; HTTP/2; prefetch |

---

## Gotchas

> [!WARNING]
> **Browser engine ≠ JS engine alone** — V8/SpiderMonkey run script; Blink/WebKit/Gecko also layout and paint.

> [!WARNING]
> **CJS in the browser** — native runtime expects ESM; ship a bundle or use modules.

> [!WARNING]
> **CSP is enforced by the engine** — “works on localhost without headers” fails in locked-down prod.

---

## When NOT to use

- **This note for MySQL/Postgres engines** — those are [[mysql engine]] / storage engines; different meaning of “engine.”
- **Hand-rolling a browser engine** — use Chromium/WebKit/Firefox; don’t reinvent.
- **Putting Node CJS unchanged on a static host** — transpile or use ESM.

---

## Related

[[content security policy]] [[ESM]] [[mysql engine]] [[Critical rendering path]] [[DOM]]
