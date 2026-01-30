
> [!WARNING]
> `TanStack` Query (formerly React Query) caches data primarily at the frontend/client level, specifically in-memory (in the browser's JavaScript runtime/RAM).

> [!NOTE]
> TanStack Query caches data exclusively in the browser's memory (RAM) per tab using its internal `QueryCache`. It is not a persistent cache, not `IndexedDB`, not `localStorage`, and definitely not a replacement for backend caching (Redis, CDN, MySQL query cache, etc.).
> - Limited by available JS heap (~1.5GB max usually much less)

Hard refresh (Ctrl + F5) clear the cache -> because JS runtime is destroyed.
Soft refresh (Ctrl + r) keep the cache -> devtool -> Application -> Clear site data -> only then it's gone

### Optional Persistence (Still Client-Side)

If you want cache to survive page refreshes:

- Use plugins like `@tanstack/react-query-persist-client`.
- Persist to `localStorage`, `IndexedDB`, etc.
- On app load → rehydrate from storage into the in-memory cache.

You can persist it
```js
// Using persistQueryClient + localForage or IndexedDB
import { persistQueryClient } from '@tanstack/react-query-persist-client'
import { createSyncStoragePersister } from '@tanstack/query-sync-storage-persister'

const persister = createSyncStoragePersister({
  storage: window.localStorage,
})

persistQueryClient({
  queryClient,
  persister,
  maxAge: 24 * 60 * 60 * 1000, // 24h
})
```

## Server state

Server-state needs: -> all of these coordinated by single `QueryClient` instance
- Automatic caching
- Background refetching
- Deduping requests

- Stale-while-revalidate
- Error/retry handling
- Mutations with optimistic updates