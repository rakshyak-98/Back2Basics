They are **compile-time enforced boundaries** that separate **Server Components** from **Client Components** in Next.js (App Router) using **React Server Components (RSC)**.

### What they actually _do_:
- **Server Components**: Rendered on the server at build- or request-time, serialized into HTML/JSON.
- **Client Components**: Hydrated in the browser and can include state, effects, event listeners, etc.
REC boundaries **define where the rendering model switches** between these two.

- Any file under `/app` is a **Server Component by default**
- You explicitly mark **Client Components** with `"use client"` directive.

`page.jsx` -> [[SSR]] entry point (cannot hydrate directly)