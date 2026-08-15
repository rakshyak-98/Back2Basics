[[javascript]] [[event listener]] [[Session Storage]] [[ServiceWorker]]

# JavaScript History API

> History API — push/replace URL + state in the session history stack without full reloads (SPA routing).

## Interview Relevance

Interviewers probe **JavaScript History API** to see if you understand what it does operationally and when it is the wrong tool — not just the definition.

## Sources

- [MDN — History API](https://developer.mozilla.org/en-US/docs/Web/API/History_API) — deep-dive
- [Wikipedia — JavaScript History API](https://en.wikipedia.org/wiki/JavaScript_History_API) — overview

## Key Concepts

## Technical Details

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

## Real-World Applications

In production APIs and tooling, **JavaScript History API** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **`popstate` does not fire on `pushState`** — only on Back/Forward (and some browser UI); **State must be structured-cloneable** — no functions/DOM nodes.

## Pros/Cons or Trade-offs

- **Pro:** Solves the job described above when used in the right layer (History API — push/replace URL + state in the session history stack without full…).
- **Con / when not:** **Full document navigations** — normal links are fine.
- **Con / when not:** **Storing huge caches** — IndexedDB / Cache API.
- **Con / when not:** **authentication tokens in history.state** — security smell; use memory/httpOnly cookies.

## Comparison

vs [[event listener]]: know when each applies — do not treat them as interchangeable. vs [[Session Storage]]: know when each applies — do not treat them as interchangeable. vs [[ServiceWorker]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid

- **`popstate` does not fire on `pushState`** — only on Back/Forward (and some browser UI).
- **State must be structured-cloneable** — no functions/DOM nodes.
- **Refresh loads from server** — deep links need server fallback to `index.html`.
- **Back doesn’t restore UI:** check Only listened to clicks; fix: Handle `popstate`
- **Full reload on nav:** check Used `location.href`; fix: `pushState` + client router
- **State `null`:** check Never passed / lost; fix: Always pass serializable state
- **SecurityError:** check Cross-origin URL; fix: Same origin only
- **Duplicate entries:** check push on every render; fix: `replaceState` for query tweaks
