<!-- note-strategy: operational -->
[[Redux]] [[Redux/redux middleware]] [[Redux/Redux State sync with localstorage]]

# Middleware

> Run code around every action — logging, thunk extras, or `createListenerMiddleware` side effects without sagas.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Middleware is a pipeline: each layer sees `action`, may dispatch more, then calls `next`. Listeners are RTK’s lightweight “on this action, run effect.”

```txt
dispatch → listener/thunk/logger → reducers → subscribers
createListenerMiddleware: match action → effect(listenerApi)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **getDefaultMiddleware** | Thunk + immutability + serializable | “Extend; don’t replace blindly.” |
| **prepend vs concat** | Order in chain | “Listeners often `prepend`.” |
| **matcher / actionCreator** | When listener runs | “Exactly one of type/creator/matcher/predicate.” |
| **extraArgument** | Inject API client into thunks | “`thunk: { extraArgument }`.” |

## Standard config / commands

```ts
const listenerMiddleware = createListenerMiddleware()
listenerMiddleware.startListening({
  actionCreator: todoAdded,
  effect: async (action, listenerApi) => {
    listenerApi.cancelActiveListeners()
    await syncTodo(action.payload)
  },
})

export const store = configureStore({
  reducer: { todos: todosReducer },
  middleware: (gDM) =>
    gDM({
      thunk: { extraArgument: { api: myApi } },
    })
      .prepend(listenerMiddleware.middleware)
      .concat(logger),
})
```

| Knob | Why it matters |
|------|----------------|
| `isAnyOf(...)` | One listener, many actions |
| `listenerApi.getState` | Post-reduce state |
| Dynamic `startListening` | Returns unsubscribe |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Listener never fires | Wrong matcher | Use `actionCreator` or `isAnyOf` |
| Serializable errors | Listener before checks | `prepend` listener middleware |
| Effect sees stale state | Closed over vars | `listenerApi.getState()` |
| Thunk missing client | No extraArgument | Pass via thunk options |
| Saga envy | Complex workflows | Prefer listeners; saga only if needed |

---

## Gotchas

> [!WARNING]
> **Provide exactly one match option** — `type` *or* `actionCreator` *or* `matcher` *or* `predicate`.

> [!WARNING]
> **`api` param name clash** — listener API ≠ RTK Query `api`; import Query api separately.

---

## When NOT to use

- **Simple UI sync** — do it in the event handler.
- **HTTP cache** — [[Redux/Redux createApi]], not custom middleware.

---

## Related

[[Redux/redux middleware]] [[Redux/Redux State sync with localstorage]] [[Redux/redux store architecture]] [[Redux/Redux Thunk]]
