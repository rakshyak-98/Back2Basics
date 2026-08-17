[[react hooks]] [[RSC (React Server Component boundaries)]] [[React Application Architecture for Production]] [[React Architecture]] [[React State management]] [[React code smells]]

# React build

> Compile and bundle React into static assets — minify, split chunks, hash filenames for CDN caching.





## Interview Relevance
Interviewers ask what a production build does differently from dev (minify, tree-shake, no HMR) and how you debug a bad chunk.

## Sources
- [Vite production build](https://vitejs.dev/guide/build.html) — deep-dive
- [React projects](https://react.dev/learn/start-a-new-react-project) — overview

## Core Definition
A React production build transforms source into optimized JS/CSS assets with content hashes for cache busting.

## Key Concepts
- **Dev vs prod:** HMR and verbose errors vs minified hashed assets.
- **Code splitting:** route-level `lazy` chunks.
- **Source maps:** upload to error tracker, restrict public access.

## Technical Details
```bash
vite build                 # emit dist/
vite preview               # smoke-test production assets locally
```

## Real-World Applications
CI runs `vite build` + bundle size budget; fail the pipeline if the main chunk grows >10%.

## Pros/Cons or Trade-offs
- **Pro:** Fast loads via caching and splitting.
- **Con:** Misconfigured base path breaks asset URLs behind proxies.

## Comparison
- vs [[React project config]]: config is knobs; build is the artifact step.

## Mistakes to Avoid
- Serving the dev server in production.
- Forgetting `base` when app is hosted under a subpath.
