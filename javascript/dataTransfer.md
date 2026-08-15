[[javascript]] [[event listener]] [[Callback]] [[mime type]]

# dataTransfer

> `dataTransfer` — drag-and-drop / clipboard payload bag: set data on dragstart, read on drop (types + files).

## Interview Relevance

Interviewers probe **dataTransfer** to see if you understand what it does operationally and when it is the wrong tool — not just the definition.

## Sources

- [Wikipedia — dataTransfer](https://en.wikipedia.org/wiki/dataTransfer) — overview

## Key Concepts

## Technical Details

```txt
dragstart: setData / files
   ↓
dragover: preventDefault (to allow drop)
   ↓
drop: getData / files
```

| Field | Role |
|-------|------|
| `setData(type, str)` | App payload (`text/plain`, custom) |
| `files` | FileList from OS drag |
| `dropEffect` / `effectAllowed` | Copy vs move UX |
| `items` | Modern typed items API |

```js
el.addEventListener('dragstart', (e) => {
  e.dataTransfer.setData('text/plain', el.dataset.id)
  e.dataTransfer.effectAllowed = 'move'
})

zone.addEventListener('dragover', (e) => e.preventDefault())
zone.addEventListener('drop', (e) => {
  e.preventDefault()
  const id = e.dataTransfer.getData('text/plain')
  const file = e.dataTransfer.files?.[0]
})
```

| Knob | Why it matters |
|------|----------------|
| `preventDefault` on dragover | Without it, drop won’t fire |
| Custom MIME | `application/x-myapp` for internal |
| `readAsDataURL` separately | Files need FileReader/fetch |

## Real-World Applications

In production APIs and tooling, **dataTransfer** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **Don’t put secrets in drag data** — any drop target can read on drop; **`text/uri-list` vs `text/plain`** — browsers differ; set both if needed.

## Pros/Cons or Trade-offs

- **Pro:** Solves the job described above when used in the right layer (`dataTransfer` — drag-and-drop / clipboard payload bag: set data on dragstart, r…).
- **Con / when not:** **Complex application DnD** — pointer events + state may be simpler than HTML5 DnD.
- **Con / when not:** **Large binary pipelines** — upload APIs, not drag strings.
- **Con / when not:** **Mobile** — HTML5 DnD support is weak; use touch UX.

## Comparison

vs [[event listener]]: know when each applies — do not treat them as interchangeable. vs [[Callback]]: know when each applies — do not treat them as interchangeable. vs [[mime type]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid

- **Don’t put secrets in drag data** — any drop target can read on drop.
- **`text/uri-list` vs `text/plain`** — browsers differ; set both if needed.
- **React synthetic DnD** — still need `preventDefault` on dragover.
- **Drop never fires:** check Missing dragover preventDefault; fix: Add it
- **`getData` empty mid-drag:** check Read too early; fix: Only on `drop`/`paste`
- **Files empty:** check Not a file drag / browser; fix: Check `items`; permissions
- **Cross-origin iframe:** check Restricted; fix: Same-origin or postMessage
- **Safari quirks:** check Custom types; fix: Also set `text/plain`
