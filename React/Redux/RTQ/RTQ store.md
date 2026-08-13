[[Redux]] [[Redux/Redux createApi]] [[Redux/RTQ Toolkit]]

# RTQ store

> Wire RTK Query into the Redux store — mount reducer + middleware, then `setupListeners`.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Each `createApi` owns a `reducerPath` slice and middleware for cache, invalidation, and refetch. `setupListeners` turns on focus/reconnect/polling helpers.

```txt
createApi → reducerPath + middleware
configureStore concatenates middleware
setupListeners(dispatch) → focus / reconnect / poll
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **reducerPath** | Where cache lives in state | “`state.productApi.queries`.” |
| **api.middleware** | Cache + lifecycle | “Must `.concat(api.middleware)`.” |
| **setupListeners** | Window/network hooks | “Polling and refetch-on-focus need it.” |

## Standard config / commands

```ts
import { configureStore } from '@reduxjs/toolkit'
import { setupListeners } from '@reduxjs/toolkit/query'
import { productApi } from './apiSlice'

export const store = configureStore({
  reducer: { [productApi.reducerPath]: productApi.reducer },
  middleware: (gDM) => gDM().concat(productApi.middleware),
})
setupListeners(store.dispatch)

// optional: dial behaviors
setupListeners(store.dispatch, {
  refetchOnFocus: true,
  refetchOnReconnect: true,
})
```

| Knob | Why it matters |
|------|----------------|
| Multiple APIs | Mount each `reducerPath` + concat each middleware |
| Skip `setupListeners` | Polling / focus refetch won’t run |
| `ApiProvider` | Only if you have **no** Redux store |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Hooks throw / cache missing | Reducer not mounted | Add `[api.reducerPath]: api.reducer` |
| Mutations hang / no invalidation | Middleware missing | `.concat(api.middleware)` |
| Polling never starts | No `setupListeners` | Call with `store.dispatch` |
| Stale after tab focus | `refetchOnFocus: false` | Enable in setup or endpoint |
| Typo `setupLinsteners` | Misspelled import call | `setupListeners` |

---

## Gotchas

> [!WARNING]
> **Cache is in-memory** — full page refresh clears it unless you add persistence.

> [!WARNING]
> **Don’t replace default middleware with a bare array** — spread/concat so thunk + checks stay.

---

## When NOT to use

- **No Redux yet, one API** — `ApiProvider` is enough for demos; real apps still want one store.
- **Non-HTTP local UI state** — plain slices, not RTK Query.

---

## Related

[[Redux/Redux createApi]] [[Redux/RTQ Toolkit]] [[Redux/RTQ/Middleware]] [[Redux toolkit]]
