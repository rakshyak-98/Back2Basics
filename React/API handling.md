[[React data management]] [[expressjs]] [[JWT authentication]] [[react-query]] [[Redux/RTQ/RTQ tags]]

# API handling (React)

> How the browser talks to backends — shared client, auth injection, cancellation, and cache ownership — **Martin Fowler (API client patterns)** + TanStack Query / RTK Query docs.

---

## Mental model

```txt
Component → hook (useQuery / useMutation) → api client (axios/fetch) → server
                ↑ cache / retry / dedupe              ↑ interceptors, baseURL
```

Separate concerns:

| Layer | Owns |
|-------|------|
| **HTTP client** | Base URL, headers, interceptors, timeouts |
| **Data library** | Cache keys, stale time, invalidation |
| **Component** | Loading UI, empty states, form submit |

Server state belongs in **Query cache**, not scattered `useState` copies ([[React data management]]).

---

## Standard config / commands

### Shared axios instance

```typescript
// lib/api.ts
import axios from "axios";

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  timeout: 15_000,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token"); // prefer httpOnly cookie in prod
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  (r) => r,
  async (err) => {
    if (err.response?.status === 401) {
      // refresh or redirect login — see [[JWT authentication]]
    }
    return Promise.reject(err);
  }
);
```

### TanStack Query wrapper

```typescript
import { useQuery } from "@tanstack/react-query";
import { api } from "./api";

export function usePosts() {
  return useQuery({
    queryKey: ["posts"],
    queryFn: async ({ signal }) => {
      const { data } = await api.get("/posts", { signal }); // AbortController
      return data;
    },
    staleTime: 60_000,
  });
}
```

### RTK Query (invalidation via tags)

See [[Redux/RTQ/RTQ tags]] — `providesTags` / `invalidatesTags` on mutations.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Double fetch on mount | Strict Mode + no dedupe | Query client dedupes; ignore duplicate in dev |
| Stale UI after mutation | Cache not invalidated | `invalidateQueries` or RTK tags |
| CORS errors | Response headers | [[CORS (Cross Origin Request Sharing)]] on server |
| Random 401 loops | Refresh token race | Single-flight refresh queue in interceptor |
| Cancel ignored | No `signal` passed | Pass Query `signal` to axios/fetch |
| Wrong env URL | `VITE_*` at build time | Rebuild; verify [[React project config]] |

---

## Gotchas

> [!WARNING]
> **Fetching in `useEffect` without cache** — every navigation refetches; race on fast route changes.

> [!WARNING]
> **Storing tokens in localStorage** — XSS exfiltration; prefer HttpOnly cookies for session ([[JWT authentication]]).

---

## When NOT to use

- **Static content only** — no API layer needed.
- **GraphQL with complex graphs** — use Apollo/urql with normalized cache, not ad hoc REST wrappers everywhere.
- **Server Components (RSC)** — fetch on server in loader/component; client cache optional.

---

## Related

[[React data management]] · [[react-query]] · [[Redux/RTQ/RTQ tags]] · [[expressjs]] · [[React build]]
