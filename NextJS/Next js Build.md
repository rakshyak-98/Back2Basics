[[NextJS]] [[Next JS]] [[NextJS configuration]]

# Next js Build

> `next build` — compiles the app into `.next` (static + server chunks); `next start` serves the production build.

---

## How it works

```txt
next build → .next/ → next start (or platform adapter)
```

---


## Configuration and commands

```bash
npm run build
npm run start
# Docker often:
# output: 'standalone' then node server.js
```

| Knob | Why it matters |
|------|----------------|
| `ANALYZE=true` | Bundle size |
| CI cache `.next/cache` | Speed |
| `typescript.ignoreBuildErrors` | Don’t enable |

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| Build OOM | Huge pages | Increase mem; split |
| Type errors | `tsc` | Fix types |
| Dynamic server usage | Static expectation | Mark dynamic |
| Missing env at build | Used at build time | Provide CI env |

---


## Gotchas

> [!WARNING]
> **Build-time env ≠ runtime env** — know which.

> [!WARNING]
> **Ignoring TS errors** — ships broken contracts.

---


## When not to use

- **development iteration** — `next dev`.
- **Non-Next React SPA** — Vite build.

---


## Related

[[Next JS]] [[NextJS configuration]] [[express build]]

## Sources

- [Wikipedia — Next js Build](https://en.wikipedia.org/wiki/Next_js_Build)
