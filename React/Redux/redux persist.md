[[Redux]] [[Redux toolkit]] [[Redux/Redux State sync with localstorage]]

# redux persist

> Save Redux state to storage and rehydrate on boot — `PersistGate` waits so UI doesn’t flash empty.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Wrap the root reducer with `persistReducer`; on load, read `localStorage`/`sessionStorage` into the store before showing the application.

```txt
dispatch → reducer → persist middleware writes storage
boot → rehydrate from storage → PersistGate releases UI
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **rehydrate** | Restore persisted state | “Until done, show a loader.” |
| **PersistGate** | Blocks children until rehydrate | “Avoids logged-out flash then logged-in.” |
| **blacklist / whitelist** | Which slices persist | “Don’t persist secrets or huge caches.” |

## Standard config / commands

```ts
import { persistStore, persistReducer } from 'redux-persist'
import storage from 'redux-persist/lib/storage'

const persistConfig = { key: 'root', storage, whitelist: ['auth', 'settings'] }
const store = configureStore({
  reducer: persistReducer(persistConfig, rootReducer),
  middleware: (gDM) =>
    gDM({ serializableCheck: { ignoredActions: ['persist/PERSIST', 'persist/REHYDRATE'] } }),
})
export const persistor = persistStore(store)

// Root
<Provider store={store}>
  <PersistGate loading={<Spinner />} persistor={persistor}>
    <App />
  </PersistGate>
</Provider>
```

| Knob | Why it matters |
|------|----------------|
| `whitelist` | Limit what hits disk |
| Ignore persist actions | RTK serializableCheck otherwise warns |
| `storage` vs `sessionStorage` | Survive tab close or not |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Flash of logged-out UI | No PersistGate / too late | Gate on `persistor` |
| Serializable warnings | Persist actions | Ignore in middleware config |
| Stale schema after deploy | Old shape in storage | Migrations / version + purge |
| QuotaExceeded | Huge state persisted | Blacklist large slices |
| State not saving | Wrong storage / SSR | Client-only storage; check key |

---

## Gotchas

> [!WARNING]
> **Tokens in localStorage** — XSS can steal them; prefer httpOnly cookies for session.

> [!WARNING]
> **SSR** — `localStorage` is browser-only; guard imports and rehydrate on client.

---

## When NOT to use

- **Server-authoritative session** — cookie + refetch user; don’t trust disk for authentication alone.
- **TanStack Query data** — use Query persister, not Redux persist for server cache.

---

## Related

[[Redux toolkit]] [[Redux/Redux State sync with localstorage]] [[react-query]]
