
- TanStack Query (formerly React Query) caches data primarily at the frontend/client level, specifically in-memory (in the browser's JavaScript runtime/RAM).


### Optional Persistence (Still Client-Side)

If you want cache to survive page refreshes:

- Use plugins like @tanstack/react-query-persist-client.
- Persist to localStorage, IndexedDB, etc.
- On app load → rehydrate from storage into the in-memory cache.