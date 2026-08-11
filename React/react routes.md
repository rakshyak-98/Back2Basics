[[React Architecture]] [[React build]] [[RSC (React Server Component boundaries)]] [[Optimizing performance]]

# React routes

> Map URLs → layouts → screens — prefer **relative routes + route objects** so base path changes don't break — **React Router v6+ docs**.

---

## Mental model

```txt
URL /billing/invoices/42
  → Router matches route tree
  → layout (shell) + child route (page)
  → loaders/actions (data router) optional
```

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

---

## Standard config / commands

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

Wrap with `RequireAuth` that reads auth hook → `<Navigate to="/login" />` or `<Outlet />`.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| 404 on refresh (SPA) | Server not fallback to index | nginx `try_files` / Vercel rewrite |
| Wrong screen on deep link | Absolute vs relative paths | Prefer nested relative paths |
| Double layout render | Missing `<Outlet />` | Add outlet in parent |
| Loader data stale | No revalidation | `shouldRevalidate` / Query cache |
| Basename broken assets | Hardcoded `/` paths | `import.meta.env.BASE_URL` |

---

## Gotchas

> [!WARNING]
> **All absolute paths** (`/manage-rooms`) — works until app moves under `/v2`; use relative segments in nested config.

> [!WARNING]
> **Client-only router on SSR** — hydrate with same route on server ([[RSC (React Server Component boundaries)]]).

---

## When NOT to use

- **File-based routing only** — Next.js App Router owns routes; don't fight framework.
- **Hash routing (`#/`)** — only legacy embeds without server rewrite support.

---

## Related

[[React Architecture]] · [[React build]] · [[API handling]] · [[RSC (React Server Component boundaries)]]
