[[Next JS]] [[NextJS Config]] [[NextJS Deployment]] [[express build]]

# Next js Build

> `next build` compiles the app into `.next` (static assets plus server chunks); `next start` serves that production build.

```txt
        Next js Build ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers probe `next build` to check whether you understand build-time ve…

## Sources
- [Next.js Docs — CLI `next build`](https://nextjs.org/docs/app/api-reference/cli/next#next-build-options) — deep-dive
- [Next.js Docs — Production](https://nextjs.org/docs/app/getting-started/deploying) — overview

## Key Concepts
- **`.next/` output:** hashed static assets + server runtime → what hosts actually run.
- **Prerender vs dynamic:** pages without dynamic APIs become static HTML → faster CDN serve.
- **Build-time environment:** values read during `next build` are baked in → missing CI environment breaks …
- **`output: 'standalone'`:** minimal Node tree for containers → copy `public/` and `.next/static` alongsid…
- **TypeScript gate:** production builds typecheck by default → `ignoreBuildErrors` hides real break…


- **Core:** The production build traces routes, prerenders static pages where possible, b…

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

## Mistakes to Avoid
- **Mistake:** Ignoring TypeScript errors in CI — you ship broken contracts
- **Mistake:** Assuming runtime environment variables exist at build time for c…
- **Mistake:** Skipping local `next build` before deploy

## Pros/Cons or Trade-offs
- **Pro:** One command produces optimized static + server output ready for production.
- **Con:** Build time and memory grow with route count and bundle size.
- **Con:** Confusing build-time with runtime environment variables causes “works locally, fails in CI” bugs.

## Comparison
- vs `next dev`: development has HMR and looser caching — never ship a dev server as production.
- vs [[express build]] / Vite SPA build: Next.js also prerenders and traces server dependencies, no…


### Use cases
- CI runs `next build` on every merge

- **Example:** A Docker image sets `output: 'standalone'`, copies `public` and …
