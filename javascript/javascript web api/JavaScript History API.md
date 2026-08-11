[[javascript]] [[event listener]]

# JavaScript History API

> History API — push/replace URL + state in the session history stack without full reloads (SPA routing).

---

## Mental model

**Say it in one breath:** `history.pushState` / `replaceState` change the URL and stash a state object; Back/Forward fires `popstate`. The browser does **not** keep a full app snapshot of every visit unless you put it in `state` (and size is limited).

```txt
pushState → stack grows
replaceState → mutate current entry
Back/Forward → popstate (state from entry)
```

| Piece | Role |
|-------|------|
| `history.state` | Data for current entry |
| `pushState(state, '', url)` | New entry |
| `popstate` | User navigated history |

---

## Standard config / commands

```js
history.pushState({ page: 1 }, '', '/page1')
history.replaceState({ page: 2 }, '', '/page2')

window.addEventListener('popstate', (e) => {
  render(e.state)
})
```

| Knob | Why it matters |
|------|----------------|
| Same-origin URL | Cross-origin push throws |
| State size | Browsers cap ~640KB–few MB |
| Title arg | Ignored in modern browsers |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Back doesn’t restore UI | Only listened to clicks | Handle `popstate` |
| Full reload on nav | Used `location.href` | `pushState` + client router |
| State `null` | Never passed / lost | Always pass serializable state |
| SecurityError | Cross-origin URL | Same origin only |
| Duplicate entries | push on every render | `replaceState` for query tweaks |

---

## Gotchas

> [!WARNING]
> **`popstate` does not fire on `pushState`** — only on Back/Forward (and some browser UI).

> [!WARNING]
> **State must be structured-cloneable** — no functions/DOM nodes.

> [!WARNING]
> **Refresh loads from server** — deep links need server fallback to `index.html`.

---

## When NOT to use

- **Full document navigations** — normal links are fine.
- **Storing huge caches** — IndexedDB / Cache API.
- **Auth tokens in history.state** — security smell; use memory/httpOnly cookies.

---

## Related

[[event listener]] [[Session Storage]] [[ServiceWorker]] [[javascript]]
