[[Redux]] [[Redux toolkit]] [[Redux/RTQ/Middleware]] [[Redux/Redux createApi]]

# Store Architecture Guide

> Feature slices + split listeners + API endpoints — keep storage, API side effects, and cross-slice sync in separate middleware files.

---

## Mental model

**Say it in one breath:** Store folder only wires reducers/middleware. Features own slice+selectors. API owns `createApi` + domain endpoint files. Listeners split by job: storage, API responses, cross-slice sync.

```txt
store/index → rootReducer + middleware/*
features/*/slice + selectors
api/apiSlice + endpoints/*
utils/storage + keys
```

### Interview map (words you can say)

| File | Job in one line |
|------|-----------------|
| **storageMiddleware** | Slice → session/localStorage |
| **apiMiddleware** | React to Query fulfilled/rejected |
| **stateMiddleware** | Keep two slices consistent |
| **listenerApi ≠ api** | Import RTK Query `api`; rename listener param |

## Standard config / commands

```txt
src/store/
  index.js              # configureStore only
  rootReducer.js
  middleware/
    index.js
    storageMiddleware.js
    apiMiddleware.js
    stateMiddleware.js
src/features/<name>/
  <name>Slice.js        # export initialState
  <name>Selectors.js
src/api/
  apiSlice.js
  endpoints/*.js
src/utils/
  storage.js
  browserStorageKeys.js
```

```ts
// ✅ export initial state for reset/tests/middleware
export const guestRoomInitialState = { /* … */ }

// ✅ after reset, persist from getState — not closure
storageMiddleware.startListening({
  actionCreator: guestRoom.actions.reset,
  effect: (_a, api) => {
    storage.session.set(KEYS.roomChooises, api.getState().guestRoom.roomChooises)
  },
})

// ✅ RTK Query from listener
import { api } from '@/api/apiSlice'
effect: (_a, listenerApi) => {
  listenerApi.dispatch(api.endpoints.getData.initiate(payload))
}
```

| Rule | Why |
|------|-----|
| Selectors in `*Selectors.js` | Keep slices thin |
| Endpoint files by domain | Avoid mega `apiSlice` |
| Storage key constants | No stringly typos |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Storage has pre-reset data | Wrote from closure after `reset` | Persist inside listener via `getState()` |
| `api.endpoints` undefined in effect | Param named `api` is listenerApi | Import Query `api`; rename param |
| Date off by timezone | `DateObject.toDate()` + moment | `date.format('YYYY-MM-DD')` directly |
| Double-formatted dates | `formatDate(alreadyFormatted)` | Pass formatted string once |
| Unsure which middleware file | Ask: storage / API response / slice sync | That answer picks the file |

---

## Gotchas

> [!WARNING]
> **Cross-slice sync in components** — races; use `stateMiddleware` listeners.

> [!WARNING]
> **Mega middleware file** — split early; matchers duplicate otherwise.

---

## When NOT to use

- **Tiny apps (1–2 slices)** — one middleware file is enough.
- **Server cache only** — RTK Query without custom storage sync.

---

## Related

[[Redux/Redux concept and data flow]] [[Redux/RTQ/Middleware]] [[Redux/Redux State sync with localstorage]] [[Redux/Redux createApi]] [[Redux toolkit]]
