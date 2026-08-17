[[NextJS Config]] [[Next js Build]] [[NextJS Deployment]] [[ISR (Incremental Static Regeneration)]] [[RSC (React Server Component boundaries)]] [[React]] [[hydration]]

# Next JS

> Next.js is a React framework with file-based routing, server rendering, and a production build — you ship pages, not a blank client shell.

```txt
        Next JS ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers use Next.js to test whether you can choose App Router versus Pag…

## Sources
- [Next.js Docs — Getting Started](https://nextjs.org/docs) — overview
- [Next.js Docs — App Router](https://nextjs.org/docs/app) — deep-dive
- [Wikipedia — Next.js](https://en.wikipedia.org/wiki/Next.js) — overview

## Key Concepts
- **App Router (`app/`):** layouts, nested routes, Server Components by default → less client JavaScript…
- **Pages Router (`pages/`):** `getStaticProps` / `getServerSideProps` → still common in older codebases.
- **Rendering modes:** static (SSG), server per request (SSR), incremental regenerate (ISR), or clie…
- **Server Actions:** server mutations from forms/components → fewer hand-rolled API routes for sim…
- **`next/image` / `next/font`:** built-in optimization pipelines → fewer layout shifts and smaller assets when…


- **Core:** Next.js wraps React with a Node (or Edge) server, a file-system router, and a…

## Technical Details
```txt
request → Next server → RSC/SSR HTML → hydrate client islands
```

| Piece | Job |
|-------|-----|
| App Router | Nested layouts and route segments |
| Server Actions | Mutations without a separate REST layer |
| `next/image` | Resize, formats, lazy loading |
| Edge vs Node runtime | Different APIs and package limits |

```bash
npx create-next-app@latest
npm run dev
npm run build && npm start
```

| Knob | Why it matters |
|------|----------------|
| `app/` vs `pages/` | Which router and data APIs you use |
| `dynamic` / `revalidate` | Cache freshness |
| Edge vs Node runtime | What libraries and Node APIs you can call |

| Symptom | Check | Fix |
|---------|-------|-----|
| `window is not defined` | Browser API in a Server Component | `"use client"` or dynamic import |
| Hydration mismatch | Server HTML ≠ client first paint | Stabilize dates/random; see [[hydration]] |
| 404 after deploy | `basePath` / trailing slash | Align [[NextJS Config]] with the host |
| Slow TTFB | Blocking data fetches | Stream; cache; shorten critical path |

## Mistakes to Avoid
- **Mistake:** Mixing App Router and Pages Router long-term
- **Mistake:** Exposing secrets with `NEXT_PUBLIC_`
- **Mistake:** Treating every page as SSR

## Pros/Cons or Trade-offs
- **Pro:** One stack for UI, routing, and rendering — strong default for React product apps.
- **Con:** Framework lock-in and hosting assumptions (Node server, ISR cache, image optimizer).
- **Con:** Mixing App and Pages routers increases cognitive load and dual APIs.

## Comparison
- vs plain [[React]] SPA (Vite/CRA): Next.js owns routing and first HTML
- vs [[express build]] / Fastify API: use a dedicated API service when you do not need React pages.


### Use cases
- Marketing sites (mostly static), SaaS dashboards (SSR + authenticated APIs), …

- **Example:** A blog uses `revalidate = 60` so editors see updates within a mi…
