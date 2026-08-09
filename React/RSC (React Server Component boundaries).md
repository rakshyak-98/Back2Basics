[[React]] [[hydration]] [[SSR]]

# RSC (React Server Component boundaries)

> Compile-time split: server components render on the server; `"use client"` marks the interactive island that hydrates in the browser.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Interview map (words you can say)]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Default under App Router is a Server Component. Crossing into hooks/events/browser APIs requires a Client Component boundary (`"use client"`).

```txt
Server Component ──props (serializable)──► Client Component
     │                         │
  DB / secrets OK          useState / onClick OK
  no hooks/events          ships JS to browser
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Server Component** | Runs on server, no client bundle for itself | “Fetch DB here; don’t send the query code.” |
| **`"use client"`** | This module + imports become client graph | “Boundary is the file with the directive.” |
| **Serializable props** | Only data that can cross the wire | “No functions/classes as props to client kids.” |

## Standard config / commands

```tsx
// app/page.tsx — Server Component (default)
import { ClientButton } from './client-button'

export default async function Page() {
  const data = await db.posts.findMany()
  return <ClientButton initial={data} />
}

// client-button.tsx
'use client'
export function ClientButton({ initial }: { initial: Post[] }) {
  const [n, setN] = useState(0)
  return <button onClick={() => setN(n + 1)}>{n}</button>
}
```

| Knob | Why it matters |
|------|----------------|
| Keep leaf interactive | Push `"use client"` down — less JS |
| Pass data, not functions | Props must serialize across RSC boundary |
| Server-only imports | `server-only` package prevents accidental client pull-in |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `createContext` / hooks error in server file | Missing `"use client"` | Add directive at top of that module |
| “Functions cannot be passed…” | Callback prop across boundary | Move handler into client child |
| Huge client bundle | `"use client"` too high | Split; keep data-fetching on server |
| Secret leaked to client | Server module imported by client | Audit import graph; use `server-only` |

---

## Gotchas

> [!WARNING]
> **`"use client"` is transitive** — everything it imports becomes part of the client bundle (unless marked server-only).

> [!WARNING]
> **Children can still be Server Components** — a client parent may render server-passed children as slots; don’t assume the whole subtree is client.

---

## When NOT to use

- **Pages Router / CRA SPA** — no RSC model; don’t force the pattern.
- **Highly interactive canvases** — mostly client; RSC buys little.

---

## Related

[[hydration]] [[SSR]] [[react cache]] [[NextJS]]
