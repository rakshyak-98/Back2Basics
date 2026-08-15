[[react hooks]] [[RSC (React Server Component boundaries)]] [[React Application Architecture for Production]] [[React Architecture]] [[React State management]] [[React build]]

# React project config

> Tooling knobs — TypeScript, ESLint, path aliases, env files, test runner — that keep a React repo consistent.

## Interview Relevance

Interviewers may ask how you structure env, lint rules (especially hooks), and path aliases in a monorepo app.

## Sources

- [Vite config](https://vitejs.dev/config/) — deep-dive
- [typescript-eslint](https://typescript-eslint.io/) — overview

## Core Definition

Project config is the shared contract for compile, lint, test, and environment — so local and CI behave the same.

## Key Concepts

- **TS + JSX:** `jsx: react-jsx`.
- **ESLint:** `eslint-plugin-react-hooks` exhaustive-deps.
- **Env:** `VITE_` / `NEXT_PUBLIC_` only for browser-safe values.

## Technical Details

```bash
# typical scripts
pnpm lint && pnpm typecheck && pnpm test && pnpm build
```

## Real-World Applications

Monorepo app package shares ESLint config; app-level env schema validated at boot.

## Pros/Cons or Trade-offs

- **Pro:** One command CI gate.
- **Con:** Over-strict lint without autofix slows newcomers.

## Comparison

- vs [[React build]]: config enables build; build emits assets.

## Mistakes to Avoid

- Committing `.env` secrets.
- Disabling react-hooks plugin globally.
