[[React Architecture]] [[React build]] [[RSC (React Server Component boundaries)]] [[Optimizing performance]] [[API handling]]

# React routes

> Map URLs → layouts → screens — prefer **relative routes + route objects** so base path changes don't break — **React Router v6+ docs**.

## Interview Relevance

Interviewers use React routes to test whether you can apply the idea under production constraints, not recite docs.

## Sources

- [Wikipedia — react routes](https://en.wikipedia.org/wiki/react_routes) — overview

## Key Concepts

React Router v6 uses nested routes:

```txt
/ app layout
  /dashboard
  /manage-rooms   ← absolute path works but couples to root
  rooms           ← relative — survives basename change
```

| Concept | Role |
|---------|------|
| `createBrowserRouter` | Data APIs, errorElement |
| `<Outlet />` | Render child route in layout |
| `lazy()` | Code-split route modules ([[React build]]) |
| `basename` | Deploy under `/app` subpath |

## Technical Details

```txt
URL /billing/invoices/42
  → Router matches route tree
  → layout (shell) + child route (page)
  → loaders/actions (data router) optional
```

```tsx
import { createBrowserRouter, RouterProvider, Outlet } from "react-router-dom";

const router = createBrowserRouter([
  {
    path: "/",
    element: <AppLayout />,
    errorElement: <RouteError />,
    children: [
      { index: true, element: <Home /> },
      {
        path: "manage-rooms",           // relative → /manage-rooms
        lazy: async () => {
          const mod = await import("./features/rooms/routes");
          return { Component: mod.RoomsPage };
        },
      },
      { path: "rooms/:id", element: <RoomDetail /> },
    ],
  },
]);

export function App() {
  return <RouterProvider router={router} />;
}

function AppLayout() {
  return (
    <main>
      <Nav />
      <Outlet />
    </main>
  );
}
```

### Basename for subpath deploy

```tsx
<RouterProvider router={router} basename="/admin" />
// links: /admin/manage-rooms
```

### Protected route

Wrap with `RequireAuth` that reads authentication hook → `<Navigate to="/login" />` or `<Outlet />`.

## Real-World Applications

Apply React routes in feature code where the Key Concepts match; verify with the Mistakes table.

## Pros/Cons or Trade-offs

- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **File-based routing only** — Next.js application Router owns routes; don't fight framework.
- **Con / skip when:** **Hash routing (`#/`)** — only legacy embeds without server rewrite support.

## Mistakes to Avoid

| Symptom | Check | Fix |
|---------|-------|-----|
| 404 on refresh (SPA) | Server not fallback to index | nginx `try_files` / Vercel rewrite |
| Wrong screen on deep link | Absolute vs relative paths | Prefer nested relative paths |
| Double layout render | Missing `<Outlet />` | Add outlet in parent |
| Loader data stale | No revalidation | `shouldRevalidate` / Query cache |
| Basename broken assets | Hardcoded `/` paths | `import.meta.env.BASE_URL` |

- **All absolute paths** (`/manage-rooms`) — works until app moves under `/v2`; use relative segments in nested config.
- **Client-only router on SSR** — hydrate with same route on server ([[RSC (React Server Component boundaries)]]).
