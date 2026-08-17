[[react hooks]] [[React State management]] [[React Architecture]] [[Separate functional logic from persentation components]]

# Stack from scratch

> Build a React app toolchain yourself — bundler, JSX transform, TypeScript, lint, test — to know what Vite/CRA hide.





## Interview Relevance
Interviewers rarely want you to invent Webpack from memory; they want you to know what each tool does in the pipeline.

## Sources
- [Vite guide](https://vitejs.dev/guide/) — overview
- [Start a React project](https://react.dev/learn/start-a-new-react-project) — overview

## Core Definition
A from-scratch stack wires compile (TS/JSX), bundle/dev server, env, and test runner — usually better adopted via Vite/Next than hand-rolled.

## Recall Cues
- Why do interviewers care about Interviewers rarely want you to invent Webpack from memory; they want you to know what each tool does in the pipeline?
- What is step 1: Resolve modules?
- What is step 2: Transform JSX/TS?
- What is step 3: Serve with HMR (dev) or emit assets (build)?
- What is step 4: Run typecheck + unit tests in CI?
- What mistake is **Copying outdated CRA eject configs in 2026**?
- What mistake is **Skipping typecheck because “the bundler compiled.”**?

## Technical Details
Minimal mental model:

1. Resolve modules
2. Transform JSX/TS
3. Serve with HMR (dev) or emit assets (build)
4. Run typecheck + unit tests in CI

## Mistakes to Avoid
- Copying outdated CRA eject configs in 2026.
- Skipping typecheck because “the bundler compiled.”

## Comparison
- vs [[React build]]: build is the production artifact step; stack includes DX tooling around it.

## Real-World Applications
Greenfield admin UI: Vite + React + TS + ESLint + Vitest instead of custom Webpack.

## Pros/Cons or Trade-offs
- **Pro:** Learning the pipeline debugs production build issues.
- **Con:** Maintaining a custom bundler config is usually wasted effort.
