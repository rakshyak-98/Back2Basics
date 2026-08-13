<!-- note-strategy: operational -->
[[Redux]] [[Redux/redux persist]] [[Redux/redux middleware]]

# Redux State sync with localStorage

> Persist a slice across reloads — hydrate on store create, write on change via middleware.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Read localStorage into `preloadedState` once; on matching actions, write the slice back. Prefer `listenerMiddleware` over saving every action.

```txt
boot → JSON.parse → preloadedState
action → reducer → listener → localStorage.setItem
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **preloadedState** | Seed store at create | “Hydrate before first render.” |
| **listenerMiddleware** | Run side effects on actions | “Save only auth login/logout.” |
| **Two-way sync** | Storage ↔ slice | “Init read; change write.” |

## Standard config / commands

```ts
const raw = localStorage.getItem('auth')
const preloadedState = raw ? { auth: JSON.parse(raw) } : undefined

const listener = createListenerMiddleware()
listener.startListening({
  matcher: isAnyOf(setCredentials, logout),
  effect: (_a, api) => {
    localStorage.setItem('auth', JSON.stringify(api.getState().auth))
  },
})

export const store = configureStore({
  reducer: { auth: authReducer },
  preloadedState,
  middleware: (gDM) => gDM().prepend(listener.middleware),
})
```

| Knob | Why it matters |
|------|----------------|
| Narrow matcher | Avoid writing on every keystroke |
| `prepend` listener | Runs before serializable checks when needed |
| Try/catch parse | Corrupt JSON must not crash boot |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Always empty after refresh | Forgot `preloadedState` | Pass hydrated object to `configureStore` |
| Writes on every action | Broad middleware | Match specific actions / `isAnyOf` |
| Crash on boot | Bad JSON | try/catch; clear key |
| Stale write after reset | Closed over old state | Read `api.getState()` inside effect |
| Multi-tab drift | Only one-way | `storage` event or [[Redux/redux persist]] |

---

## Gotchas

> [!WARNING]
> **Don’t store tokens in localStorage if XSS is in scope** — prefer httpOnly cookies / session strategy.

> [!WARNING]
> **Static `startListening` needs no `stopListening`** — only dynamic listeners return unsubscribe.

---

## When NOT to use

- **Full application persistence** — use [[Redux/redux persist]] with whitelist/blacklist.
- **Server-secret state** — never put secrets in localStorage.

---

## Related

[[Redux/redux persist]] [[Redux/redux middleware]] [[Redux/redux store architecture]] [[Redux toolkit]]
