[[React Architecture]] [[React build]] [[RSC (React Server Component boundaries)]] [[Optimizing performance]] [[API handling]]

# React routes

> Map URLs → layouts → screens — prefer **relative routes + route objects** so base path changes don't break — **React Router v6+ docs**.

```txt
        React routes ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Use cases
```

## Interview Relevance
- **Interview probes:** Interviewers use React routes to test whether you can apply the idea under pr…

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

- Wrap with `RequireAuth` that reads authentication hook → `<Navigate to="/logi…

## Mistakes to Avoid
| Symptom | Check | Fix |
|---------|-------|-----|
| 404 on refresh (SPA) | Server not fallback to index | nginx `try_files` / Vercel rewrite |
| Wrong screen on deep link | Absolute vs relative paths | Prefer nested relative paths |
| Double layout render | Missing `<Outlet />` | Add outlet in parent |
| Loader data stale | No revalidation | `shouldRevalidate` / Query cache |
| Basename broken assets | Hardcoded `/` paths | `import.meta.env.BASE_URL` |

- **Mistake:** **All absolute paths** (`/manage-rooms`)
- **Mistake:** **Client-only router on SSR**

## Pros/Cons or Trade-offs
- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **File-based routing only**
- **Con / skip when:** **Hash routing (`#/`)**

## Real-World Applications
- **Scenario:** Apply React routes in feature code where the Key Concepts match
