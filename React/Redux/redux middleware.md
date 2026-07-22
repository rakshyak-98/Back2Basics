[[Redux]] [[Redux/Redux Thunk]] [[Redux/Redux createAsyncThunk]] [[Redux concept and data flow]]

# redux middleware

> Functions **`dispatch → action → middleware chain → reducer`** — intercept, async, logging — **Redux middleware contract**.

---

## Mental model

```txt
dispatch(action)
   ↓
middleware₁ (can call next(action), delay, swallow)
   ↓
middleware₂
   ↓
reducer → new state
```

Signature:

```javascript
store => next => action => { /* ... */ return next(action); }
```

Middleware powers **async** ([[Redux/Redux Thunk]], RTK Query), **analytics**, **crash reporting**, and **router sync**. It must stay **predictable** — side effects belong here or in listeners, not in reducers ([[Redux/redux reducers]]).

RTK default middleware (dev): `redux-thunk` + serializable/immutable invariant checks.

---

## Standard config / commands

### Custom logging middleware

```typescript
import type { Middleware } from "@reduxjs/toolkit";

export const logger: Middleware = (store) => (next) => (action) => {
  console.log("dispatching", action);
  const result = next(action);
  console.log("next state", store.getState());
  return result;
};

export const store = configureStore({
  reducer: rootReducer,
  middleware: (getDefault) => getDefault().concat(logger),
});
```

### Thunk (async in action creator)

```typescript
export const fetchUser = (id: string) => async (dispatch, getState) => {
  dispatch(setLoading(true));
  try {
    const user = await api.getUser(id);
    dispatch(setUser(user));
  } finally {
    dispatch(setLoading(false));
  }
};
```

Prefer **`createAsyncThunk`** ([[Redux/Redux createAsyncThunk]]) for pending/fulfilled/rejected lifecycle.

### Middleware that blocks

```typescript
const crashReporter: Middleware = () => (next) => (action) => {
  try {
    return next(action);
  } catch (err) {
    report(err);
    throw err;
  }
};
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Action never hits reducer | Forgot `next(action)` | Return `next(action)` unless intentionally blocking |
| Async never runs | Not using thunk middleware | RTK `getDefaultMiddleware` includes thunk |
| Infinite dispatch loop | Middleware dispatches same type | Add guard / compare action type |
| Dev slow | invariant middleware | Normal in dev; disable only if needed |
| RTK Query not caching | Query middleware missing | Include `api.middleware` in concat |

---

## Gotchas

> [!WARNING]
> **Mutating action in middleware** — breaks time-travel; treat actions as read-only.

> [!WARNING]
> **Heavy work synchronous in middleware** — blocks dispatch pipeline; defer with queue/microtask.

---

## When NOT to use

- **Simple sync state** — middleware adds noise without async/logging need.
- **Fetch in middleware instead of RTK Query** — reinventing cache/invalidation ([[Redux/RTQ/RTQ tags]]).
- **Business logic in reducer** — reducers stay pure; async in middleware/thunk.

---

## Related

[[Redux]] · [[Redux/redux compose]] · [[Redux/Redux Thunk]] · [[Redux/Redux createAsyncThunk]] · [[Redux/RTQ/Middleware]]
