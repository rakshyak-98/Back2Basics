[[NextJS]] [[React]] [[express build]]

# Next JS

> Next.js — React framework with file-based routing, server components/SSR, and a production build toolchain.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Routes live under `app/` (application Router) or `pages/`. Server Components render on server by default; mark client interactivity with `"use client"`.

```txt
request → Next server → RSC/SSR/HTML → hydrate client islands
```

| Piece | Job |
|-------|-----|
| App Router | Layouts/nested routes |
| Server Actions | Mutations |
| next/image | Image pipeline |

---

## Standard config / commands

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

## Triage (when things break)

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

## When NOT to use

- **Pure API service** — Fastify/Express.
- **Static brochure without React** — simpler SSG/HTML.

---

## Related

[[NextJS configuration]] [[Next js Build]] [[RSC (React Server Component boundaries)]] [[React]]
