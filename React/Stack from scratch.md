[[react hooks]] [[React State management]] [[React Architecture]] [[Separate functional logic from persentation components]]

# Stack from scratch

> Build a React app toolchain yourself — bundler, JSX transform, TypeScript, lint, test — to know what Vite/CRA hide.

```txt
        Stack from scratch ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers rarely want you to invent Webpack from memory

## Sources
- [Vite guide](https://vitejs.dev/guide/) — overview
- [Start a React project](https://react.dev/learn/start-a-new-react-project) — overview

## Key Concepts
- **Core:** A from-scratch stack wires compile (TS/JSX), bundle/dev server, env, and test…

## Technical Details
- Minimal mental model:

1. Resolve modules
2. Transform JSX/TS
3. Serve with HMR (dev) or emit assets (build)
4. Run typecheck + unit tests in CI

## Mistakes to Avoid
- **Mistake:** Copying outdated CRA eject configs in 2026
- **Mistake:** Skipping typecheck because “the bundler compiled.”

## Pros/Cons or Trade-offs
- **Pro:** Learning the pipeline debugs production build issues.
- **Con:** Maintaining a custom bundler config is usually wasted effort.

## Comparison
- vs [[React build]]: build is the production artifact step; stack includes DX tooling around it.


### Use cases
- Greenfield admin UI: Vite + React + TS + ESLint + Vitest instead of custom We…
