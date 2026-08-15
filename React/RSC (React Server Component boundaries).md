[[react hooks]] [[React State management]] [[React Architecture]] [[react style inside component]] [[Component Presentational Pattern]] [[Controlled and Uncontrolled component Pattern]]

# RSC (React Server Component boundaries)

> Server Components render on the server and send UI to the client; use client marks the interactive boundary that ships JS.

## Interview Relevance

Interviewers probe what can run on the server, what must be client, and how data fetching moves out of the browser bundle.

## Sources

- [Server Components](https://react.dev/reference/rsc/server-components) — deep-dive
- [use client](https://react.dev/reference/rsc/use-client) — overview

## Core Definition

RSC boundaries separate server-only code (filesystem, secrets, direct DB) from client components that use state and browser APIs.

## Key Concepts

- **Default server:** less JS shipped.
- **`"use client"`:** opt into hooks/events.
- **Pass serializable props** across the boundary.
- **No server-only imports** into client files.

## Technical Details

```tsx
// Server Component (default in App Router)
async function Page() {
  const data = await db.posts()
  return <PostList posts={data} />  // Client child for likes button
}
```

## Real-World Applications

Next.js app router page fetches posts on the server; like button is a small client island.

## Pros/Cons or Trade-offs

- **Pro:** Smaller bundles, closer data.
- **Con:** Wrong boundary causes bundle bloat or serialisation errors.

## Comparison

- vs SSR of client trees: RSC can keep code off the client entirely; SSR still ships the component JS for hydration.

## Mistakes to Avoid

- Marking the root layout client “to use hooks.”
- Passing functions/classes across the server→client boundary.
