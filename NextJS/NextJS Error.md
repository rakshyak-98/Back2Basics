[[Next JS]] [[NextJS navigation]] [[NextJS Config]] [[RSC (React Server Component boundaries)]] [[hydration]]

# NextJS Error

> Common Next.js errors usually mean the wrong router API, a broken path alias, or React Server Component boundaries — read the message as a routing or boundary bug, not a random crash.

```txt
        NextJS Error ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers care less about memorizing error strings and more about whether …

## Sources
- [Next.js Docs — `NextRouter` was not mounted](https://nextjs.org/docs/messages/next-router-not-mounted) — deep-dive
- [Next.js Docs — Migrating to the App Router](https://nextjs.org/docs/app/guides/migrating/app-router-migration) — overview
- [Next.js Docs — Absolute Imports and Module Path Aliases](https://nextjs.org/docs/app/getting-started/installation#set-up-absolute-imports-and-module-path-aliases) — overview

## Key Concepts
- **`NextRouter` was not mounted:** `useRouter` from `next/router` used under `app/`, or outside a Next provider …
- **App Router hooks:** `useRouter`, `useSearchParams`, `useParams` from `next/navigation` → designed…
- **Path aliases:** `@/` only works if `tsconfig`/`jsconfig` `paths` match the project layout.
- **RSC boundary errors:** importing client React (`useContext`, hooks) into a Server Component graph → …
- **Vendored RSC React:** errors mentioning `app-rsc` / vendored `react.js` → wrong React entry pulled …


- **Core:** Next.js surfaces framework-specific failures when client-only hooks run in th…

## Technical Details
### Router not mounted (App Router)

```js
// Wrong under app/
import { useRouter } from 'next/router'

// Correct for App Router (Client Component)
import { useRouter, useSearchParams, useParams } from 'next/navigation'
```

- Why: App Router is Server Components first.
- Pages Router hooks expect a client routing context that does not exist in tha…
- See [[RSC (React Server Component boundaries)]].

### Module not found for `@/`

```text
Module not found: Can't resolve '@/app/store/store.js'
```

- Ensure `tsconfig.json` (or `jsconfig.json`) includes:

```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./*"]
    }
  }
}
```

- Paths are relative to the TypeScript/JavaScript configuration file

### RSC / `useContext` is not a function

```text
TypeError: ... useContext is not a function
```

- Often means a client hook or client-only library is imported into a Server Co…
- Fix by adding `"use client"` to the component that uses hooks, or by splittin…

| Symptom | Check | Fix |
|---------|-------|-----|
| `NextRouter was not mounted` | Import path | `next/navigation` in `app/`; mock in tests |
| `Can't resolve '@/…'` | `paths` in tsconfig | Align alias; restart [[Next js Build]] / `next dev` |
| `useContext is not a function` (RSC) | Import graph | `"use client"` boundary; avoid client libs on server |
| Hydration mismatch overlay | Server vs client HTML | Stabilize output; see [[hydration]] |

## Mistakes to Avoid
- **Mistake:** Copy-pasting Pages Router examples into `app/` without changing …
- **Mistake:** Fixing alias errors by relative `../../../` sprawl instead of co…
- **Mistake:** Marking entire trees `"use client"` to silence RSC errors

## Pros/Cons or Trade-offs
- **Pro:** Explicit errors push you toward correct boundaries instead of silent wrong behavior.
- **Con:** Messages can look like React internals (`app-rsc`) until you map them to “client API on the server.”
- **Con:** Dual router eras (`next/router` vs `next/navigation`) double the failure modes during migration.

## Comparison
- vs generic React errors: Next.js adds router context and RSC packaging layers on top of React.
- vs [[NextJS navigation]]: wrong import is an error


### Use cases
- Migrations from `pages/` to `app/` hit router-not-mounted first

- **Example:** A shared `useAuth()` hook imported into a Server Component page …
