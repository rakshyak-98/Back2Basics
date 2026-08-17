[[react hooks]] [[RSC (React Server Component boundaries)]] [[React Application Architecture for Production]] [[React Architecture]] [[React State management]] [[React code smells]]

# React build

> Compile and bundle React into static assets — minify, split chunks, hash filenames for CDN caching.

```txt
        React build ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers ask what a production build does differently from dev (minify, t…

## Sources
- [Vite production build](https://vitejs.dev/guide/build.html) — deep-dive
- [React projects](https://react.dev/learn/start-a-new-react-project) — overview

## Key Concepts
- **Dev vs prod:** HMR and verbose errors vs minified hashed assets.
- **Code splitting:** route-level `lazy` chunks.
- **Source maps:** upload to error tracker, restrict public access.


- **Core:** A React production build transforms source into optimized JS/CSS assets with …

## Technical Details
```bash
vite build                 # emit dist/
vite preview               # smoke-test production assets locally
```

## Mistakes to Avoid
- **Mistake:** Serving the dev server in production
- **Mistake:** Forgetting `base` when app is hosted under a subpath

## Pros/Cons or Trade-offs
- **Pro:** Fast loads via caching and splitting.
- **Con:** Misconfigured base path breaks asset URLs behind proxies.

## Comparison
- vs [[React project config]]: config is knobs; build is the artifact step.


### Use cases
- CI runs `vite build` + bundle size budget
