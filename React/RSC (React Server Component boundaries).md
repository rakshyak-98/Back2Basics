[[react hooks]] [[React State management]] [[React Architecture]] [[react style inside component]] [[Component Presentational Pattern]] [[Controlled and Uncontrolled component Pattern]]

# RSC (React Server Component boundaries)

> Server Components render on the server and send UI to the client; use client marks the interactive boundary that ships JS.

```txt
        RSC (React Server  ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers probe what can run on the server, what must be client, and how d…

## Sources
- [Server Components](https://react.dev/reference/rsc/server-components) — deep-dive
- [use client](https://react.dev/reference/rsc/use-client) — overview

## Key Concepts
- **Default server:** less JS shipped.
- **`"use client"`:** opt into hooks/events.
- **Pass serializable props:** across the boundary.
- **No server-only imports:** into client files.


- **Core:** RSC boundaries separate server-only code (filesystem, secrets, direct DB) fro…

## Technical Details
```tsx
// Server Component (default in App Router)
async function Page() {
  const data = await db.posts()
  return <PostList posts={data} />  // Client child for likes button
}
```

## Mistakes to Avoid
- **Mistake:** Marking the root layout client “to use hooks.”
- **Mistake:** Passing functions/classes across the server→client boundary

## Pros/Cons or Trade-offs
- **Pro:** Smaller bundles, closer data.
- **Con:** Wrong boundary causes bundle bloat or serialisation errors.

## Comparison
- vs SSR of client trees: RSC can keep code off the client entirely


### Use cases
- Next.js app router page fetches posts on the server
