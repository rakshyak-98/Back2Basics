[[Redux]] [[Redux/Immutability in Redux]] [[Redux/Redux createSlice]] [[javascript/Packages/Immer]]

# Redux Error (common fixes)

> Recurring Redux / RTK / Immer failures in dev and prod — MapSet, serializable checks, mutations — **Redux Toolkit docs + Immer**.

---

## Mental model

Redux expects:

```txt
State tree     → plain objects/arrays (serializable)
Updates        → immutable (RTK uses Immer drafts in createSlice)
Middleware dev → catches mutations + non-serializable values
```

Errors usually mean you violated one of those rules or forgot an Immer plugin.

---

## Standard config / commands

### Immer MapSet plugin

```txt
Error: [Immer] The plugin for 'MapSet' has not been loaded...
```

When using `Map` / `Set` in state or drafts:

```typescript
import { configureStore } from "@reduxjs/toolkit";
import { enableMapSet } from "immer";

enableMapSet(); // call once before store creation

export const store = configureStore({ reducer: rootReducer });
```

Prefer **plain objects** over Map/Set in Redux state when possible — simpler DevTools and persist.

### Serializable check warning

```txt
A non-serializable value was detected in an action/state
```

Common culprits: `Date`, `Error`, `Map`, DOM nodes, axios response objects.

```typescript
configureStore({
  reducer: rootReducer,
  middleware: (getDefault) =>
    getDefault({
      serializableCheck: {
        ignoredActions: ["persist/PERSIST"], // redux-persist
        ignoredPaths: ["register.date"],
      },
    }),
});
```

Fix properly: store **ISO strings** / ids, not class instances.

### Accidental mutation outside Immer

```javascript
// BAD in plain reducer
state.items.push(x);

// GOOD in createSlice (Immer)
state.items.push(x); // OK inside createSlice reducer only
```

See [[Redux/Immutability in Redux]].

### Hydration mismatch with persist

Ensure [[Redux/redux persist]] whitelist excludes non-serializable slices; call `enableMapSet` before rehydrate if using Map.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| MapSet Immer error | Map/Set in slice | `enableMapSet()` or plain object |
| Console serializable flood | RTK Query meta | Ignore paths or strip in transform |
| State unchanged after dispatch | Mutated nested object outside Immer | Return new object or use createSlice |
| DevTools empty actions | Middleware stripped | Don't disable default middleware |
| Infinite loop dispatch | Middleware dispatching same action | Guard conditions in middleware |

---

## Gotchas

> [!WARNING]
> **Ignoring all serializable checks** — hides bugs until persist/export fails in prod.

> [!WARNING]
> **Storing fetch `Response` in state** — store parsed JSON only.

---

## When NOT to use

- **Bypassing Immer with deep clone everywhere** — use `createSlice` correctly instead.
- **Map/Set for convenience** — normalized `{ byId, allIds }` pattern scales better with RTK.

---

## Related

[[Redux]] · [[Redux/Immutability in Redux]] · [[Redux/Redux createSlice]] · [[javascript/Packages/Immer]] · [[Redux/redux middleware]]
