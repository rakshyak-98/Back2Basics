[[Next JS]] [[NextJS navigation]] [[NextJS Config]] [[RSC (React Server Component boundaries)]] [[hydration]]

# NextJS Error

> Common Next.js errors usually mean the wrong router API, a broken path alias, or React Server Component boundaries — read the message as a routing or boundary bug, not a random crash.

## Interview Relevance

Interviewers care less about memorizing error strings and more about whether you can map “router not mounted,” module-not-found, and RSC `useContext` failures to App Router versus Pages Router and client/server boundaries.

## Sources

- [Next.js Docs — `NextRouter` was not mounted](https://nextjs.org/docs/messages/next-router-not-mounted) — deep-dive
- [Next.js Docs — Migrating to the App Router](https://nextjs.org/docs/app/guides/migrating/app-router-migration) — overview
- [Next.js Docs — Absolute Imports and Module Path Aliases](https://nextjs.org/docs/app/getting-started/installation#set-up-absolute-imports-and-module-path-aliases) — overview

## Core Definition

Next.js surfaces framework-specific failures when client-only hooks run in the wrong tree, imports resolve outside configured aliases, or a Server Component graph pulls in client React APIs.

## Key Concepts

- **`NextRouter` was not mounted:** `useRouter` from `next/router` used under `app/`, or outside a Next provider (tests) → migrate to `next/navigation` or mock the router.
- **App Router hooks:** `useRouter`, `useSearchParams`, `useParams` from `next/navigation` → designed for the App Router; need a Client Component when used in UI.
- **Path aliases:** `@/` only works if `tsconfig`/`jsconfig` `paths` match the project layout.
- **RSC boundary errors:** importing client React (`useContext`, hooks) into a Server Component graph → `"use client"` on the leaf that needs hooks, or move logic down.
- **Vendored RSC React:** errors mentioning `app-rsc` / vendored `react.js` → wrong React entry pulled into the server graph.

## Technical Details

### Router not mounted (App Router)

```js
// Wrong under app/
import { useRouter } from 'next/router'

// Correct for App Router (Client Component)
import { useRouter, useSearchParams, useParams } from 'next/navigation'
```

Why: App Router is Server Components first. Pages Router hooks expect a client routing context that does not exist in that tree. See [[RSC (React Server Component boundaries)]].

### Module not found for `@/`

```text
Module not found: Can't resolve '@/app/store/store.js'
```

Ensure `tsconfig.json` (or `jsconfig.json`) includes:

```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./*"]
    }
  }
}
```

Paths are relative to the TypeScript/JavaScript configuration file; restart the development server after changes.

### RSC / `useContext` is not a function

```text
TypeError: ... useContext is not a function
```

Often means a client hook or client-only library is imported into a Server Component. Fix by adding `"use client"` to the component that uses hooks, or by splitting a client child from a server parent.

| Symptom | Check | Fix |
|---------|-------|-----|
| `NextRouter was not mounted` | Import path | `next/navigation` in `app/`; mock in tests |
| `Can't resolve '@/…'` | `paths` in tsconfig | Align alias; restart [[Next js Build]] / `next dev` |
| `useContext is not a function` (RSC) | Import graph | `"use client"` boundary; avoid client libs on server |
| Hydration mismatch overlay | Server vs client HTML | Stabilize output; see [[hydration]] |

## Real-World Applications

Migrations from `pages/` to `app/` hit router-not-mounted first; monorepos hit alias resolution; shared UI kits that call hooks must be marked client when used under the App Router.

**Example:** A shared `useAuth()` hook imported into a Server Component page fails until the consuming component is a Client Component or the session is read on the server instead.

## Pros/Cons or Trade-offs

- **Pro:** Explicit errors push you toward correct boundaries instead of silent wrong behavior.
- **Con:** Messages can look like React internals (`app-rsc`) until you map them to “client API on the server.”
- **Con:** Dual router eras (`next/router` vs `next/navigation`) double the failure modes during migration.

## Comparison

- vs generic React errors: Next.js adds router context and RSC packaging layers on top of React.
- vs [[NextJS navigation]]: wrong import is an error; choosing `<Link>` vs `<a>` is an API design choice.

## Mistakes to Avoid

- Copy-pasting Pages Router examples into `app/` without changing imports.
- Fixing alias errors by relative `../../../` sprawl instead of correcting `paths`.
- Marking entire trees `"use client"` to silence RSC errors — shrink the client boundary instead.
