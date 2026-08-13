[[NextJS]] [[React]] [[express build]]

# Next JS

> Next.js — React framework with file-based routing, server components/SSR, and a production build toolchain.

---

## How it works

```txt
request → Next server → RSC/SSR/HTML → hydrate client islands
```

| Piece | Job |
|-------|-----|
| App Router | Layouts/nested routes |
| Server Actions | Mutations |
| next/image | Image pipeline |

---


## Configuration and commands

```bash
npx create-next-app@latest
npm run dev
npm run build && npm start
```

| Knob | Why it matters |
|------|----------------|
| `app/` vs `pages/` | Router generation |
| `dynamic` / `revalidate` | Caching |
| Edge vs Node runtime | API limits |

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| Window is not defined | Client API in server | `"use client"` or dynamic |
| Hydration mismatch | Server≠client HTML | Stabilize random/dates |
| 404 after deploy | Base path / trailing slash | Align config/host |
| Slow TTFB | Blocking data | Stream; cache |

---


## Gotchas

> [!WARNING]
> **Mixing routers** — prefer one.

> [!WARNING]
> **Env vars** — `NEXT_PUBLIC_` only for browser.

---


## When not to use

- **Pure API service** — Fastify/Express.
- **Static brochure without React** — simpler SSG/HTML.

---


## Related

[[NextJS configuration]] [[Next js Build]] [[RSC (React Server Component boundaries)]] [[React]]

## Sources

- [Wikipedia — Next JS](https://en.wikipedia.org/wiki/Next_JS)
