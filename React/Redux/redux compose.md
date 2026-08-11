[[Redux]] [[Redux/redux middleware]] [[Redux toolkit]] [[Redux/Redux createSlice]]

# redux compose

> **Right-to-left** function composition — chain store enhancers (`applyMiddleware`, DevTools) into one `createStore` argument — **Redux core API**.

---

## Mental model

```txt
compose(f, g, h)(store)  ===  f(g(h(store)))
```

Redux uses compose to merge **enhancers** — functions that wrap `createStore`:

```txt
createStore(reducer, preloadedState, enhancer)
enhancer = compose(applyMiddleware(thunk), devToolsExtension())
```

Modern apps use **`configureStore`** from RTK ([[Redux toolkit]]) which applies middleware + DevTools internally — raw `compose` appears in legacy tutorials and custom store setup.

| Piece | Role |
|-------|------|
| `applyMiddleware` | Inserts middleware chain |
| DevTools extension | Time-travel debug wrapper |
| `compose` | Combines enhancers right → left |

---

## Standard config / commands

### Legacy manual store (know for interviews / migrations)

```javascript
import { createStore, compose, applyMiddleware } from "redux";
import { thunk } from "redux-thunk";

const composeEnhancers =
  window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__?.() ?? compose;

const store = createStore(
  rootReducer,
  composeEnhancers(applyMiddleware(thunk))
);
```

### Redux Toolkit (preferred — no manual compose)

```typescript
import { configureStore } from "@reduxjs/toolkit";

export const store = configureStore({
  reducer: rootReducer,
  middleware: (getDefault) => getDefault().concat(customMiddleware),
  devTools: process.env.NODE_ENV !== "production",
});
```

RTK's `getDefaultMiddleware` already includes thunk + invariant checks in dev.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| DevTools not connected | Wrong compose enhancer | Use `__REDUX_DEVTOOLS_EXTENSION_COMPOSE__` |
| Middleware never runs | Order in compose | Middleware enhancer innermost (applied last in chain) |
| `undefined is not a function` | compose on non-enhancers | Each arg must be `(createStore) => (reducer, pre) => store` |
| Double middleware | compose + configureStore | Pick RTK only |
| Prod bundle includes DevTools | Guard with NODE_ENV | `devTools: false` in prod |

---

## Gotchas

> [!WARNING]
> **Right-to-left order** — easy to invert middleware vs DevTools when copying snippets.

> [!WARNING]
> **`compose` from Redux vs lodash/fp** — same name, different imports; use Redux's for enhancers.

---

## When NOT to use

- **New greenfield apps** — `configureStore` handles composition.
- **Non-Redux function piping** — use plain functions or `pipe` utilities elsewhere.

---

## Related

[[Redux]] · [[Redux/redux middleware]] · [[Redux toolkit]] · [[Redux/Redux concept and data flow]]
