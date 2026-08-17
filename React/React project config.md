[[react hooks]] [[RSC (React Server Component boundaries)]] [[React Application Architecture for Production]] [[React Architecture]] [[React State management]] [[React build]]

# React project config

> Tooling knobs — TypeScript, ESLint, path aliases, env files, test runner — that keep a React repo consistent.

```txt
        React project conf ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers may ask how you structure env, lint rules (especially hooks), an…

## Sources
- [Vite config](https://vitejs.dev/config/) — deep-dive
- [typescript-eslint](https://typescript-eslint.io/) — overview

## Key Concepts
- **TS + JSX:** `jsx: react-jsx`.
- **ESLint:** `eslint-plugin-react-hooks` exhaustive-deps.
- **Env:** `VITE_` / `NEXT_PUBLIC_` only for browser-safe values.


- **Core:** Project config is the shared contract for compile, lint, test, and environment

## Technical Details
```bash
# typical scripts
pnpm lint && pnpm typecheck && pnpm test && pnpm build
```

## Mistakes to Avoid
- **Mistake:** Committing `.env` secrets
- **Mistake:** Disabling react-hooks plugin globally

## Pros/Cons or Trade-offs
- **Pro:** One command CI gate.
- **Con:** Over-strict lint without autofix slows newcomers.

## Comparison
- vs [[React build]]: config enables build; build emits assets.


### Use cases
- Monorepo app package shares ESLint config
