[[javascript]] [[event listener]] [[Session Storage]] [[ServiceWorker]]

# JavaScript History API

> History API — push/replace URL + state in the session history stack without full reloads (SPA routing).

```txt
        JavaScript History ──┬── Interview
               ├── Sources
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers probe **JavaScript History API** to see if you understand what i…

## Sources
- [MDN — History API](https://developer.mozilla.org/en-US/docs/Web/API/History_API) — deep-dive
- [Wikipedia — JavaScript History API](https://en.wikipedia.org/wiki/JavaScript_History_API) — overview

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

## Mistakes to Avoid
- **Mistake:** **`popstate` does not fire on `pushState`**
- **Mistake:** **State must be structured-cloneable** — no functions/DOM nodes
- **Mistake:** **Refresh loads from server**
- **Mistake:** **Back doesn’t restore UI:** check Only listened to clicks
- **Mistake:** **Full reload on nav:** check Used `location.href`
- **Mistake:** **State `null`:** check Never passed / lost
- **Mistake:** **SecurityError:** check Cross-origin URL; fix: Same origin only
- **Mistake:** **Duplicate entries:** check push on every render

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (History API — push/replace URL + state in the session history stack without full…).
- **Con / when not:** **Full document navigations** — normal links are fine.
- **Con / when not:** **Storing huge caches** — IndexedDB / Cache API.
- **Con / when not:** **authentication tokens in history.state**

## Comparison
- vs [[event listener]]: know when each applies


### Use cases
- In production APIs and tooling, **JavaScript History API** shows up whenever …
