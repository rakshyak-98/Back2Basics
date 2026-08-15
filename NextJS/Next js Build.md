[[Next JS]] [[NextJS Config]] [[NextJS Deployment]] [[express build]]

# Next js Build

> `next build` compiles the app into `.next` (static assets plus server chunks); `next start` serves that production build.

## Interview Relevance

Interviewers probe `next build` to check whether you understand build-time versus runtime environment variables, what fails the build (types, dynamic usage), and how CI caches and standalone output affect deploys.

## Sources

- [Next.js Docs — CLI `next build`](https://nextjs.org/docs/app/api-reference/cli/next#next-build-options) — deep-dive
- [Next.js Docs — Production](https://nextjs.org/docs/app/getting-started/deploying) — overview

## Core Definition

The production build traces routes, prerenders static pages where possible, bundles client and server code, and writes artifacts under `.next/` for `next start` or a platform adapter.

## Key Concepts

- **`.next/` output:** hashed static assets + server runtime → what hosts actually run.
- **Prerender vs dynamic:** pages without dynamic APIs become static HTML → faster CDN serve.
- **Build-time environment:** values read during `next build` are baked in → missing CI environment breaks the build or embeds wrong defaults.
- **`output: 'standalone'`:** minimal Node tree for containers → copy `public/` and `.next/static` alongside.
- **TypeScript gate:** production builds typecheck by default → `ignoreBuildErrors` hides real breakage.

## Technical Details

```txt
next build → .next/ → next start (or platform adapter)
```

```bash
npm run build
npm run start
# Docker often:
# next.config: output: 'standalone'
# then: node .next/standalone/server.js
```

| Knob | Why it matters |
|------|----------------|
| `ANALYZE=true` / bundle analyzer | Find oversized client chunks |
| CI cache of `.next/cache` | Faster rebuilds |
| `typescript.ignoreBuildErrors` | Do not enable |

| Symptom | Check | Fix |
|---------|-------|-----|
| Build out-of-memory | Huge pages / memory limit | Raise memory; split routes |
| Type errors | `tsc` / build log | Fix types |
| “Dynamic server usage” | Expected static route | Mark dynamic or remove dynamic APIs |
| Missing environment at build | Build-time reads | Provide variables in CI |

## Real-World Applications

CI runs `next build` on every merge; the artifact deploys to Vercel, Docker (`standalone`), or a Node host via `next start`.

**Example:** A Docker image sets `output: 'standalone'`, copies `public` and `.next/static` into the image, and starts `node server.js` — see [[NextJS Deployment]].

## Pros/Cons or Trade-offs

- **Pro:** One command produces optimized static + server output ready for production.
- **Con:** Build time and memory grow with route count and bundle size.
- **Con:** Confusing build-time with runtime environment variables causes “works locally, fails in CI” bugs.

## Comparison

- vs `next dev`: development has HMR and looser caching — never ship a dev server as production.
- vs [[express build]] / Vite SPA build: Next.js also prerenders and traces server dependencies, not only a browser bundle.

## Mistakes to Avoid

- Ignoring TypeScript errors in CI — you ship broken contracts.
- Assuming runtime environment variables exist at build time for code that runs during prerender.
- Skipping local `next build` before deploy — many errors only appear in production mode.
