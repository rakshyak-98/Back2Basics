[[javascript]] [[event listener]] [[Callback]] [[mime type]]

# dataTransfer

> `dataTransfer` — drag-and-drop / clipboard payload bag: set data on dragstart, read on drop (types + files).

```txt
        dataTransfer ──┬── Why it matters
               ├── Sources
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers probe **dataTransfer** to see if you understand what it does ope…

## Sources
- [Wikipedia — dataTransfer](https://en.wikipedia.org/wiki/dataTransfer) — overview

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

## Mistakes to Avoid
- **Mistake:** **Don’t put secrets in drag data**
- **Mistake:** **`text/uri-list` vs `text/plain`**
- **Mistake:** **React synthetic DnD** — still need `preventDefault` on dragover
- **Mistake:** **Drop never fires:** check Missing dragover preventDefault
- **Mistake:** **`getData` empty mid-drag:** check Read too early
- **Mistake:** **Files empty:** check Not a file drag / browser
- **Mistake:** **Cross-origin iframe:** check Restricted
- **Mistake:** **Safari quirks:** check Custom types; fix: Also set `text/plain`

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (`dataTransfer` — drag-and-drop / clipboard payload bag: set data on dragstart, r…).
- **Con / when not:** **Complex application DnD**
- **Con / when not:** **Large binary pipelines**
- **Con / when not:** **Mobile** — HTML5 DnD support is weak; use touch UX.

## Comparison
- vs [[event listener]]: know when each applies


### Use cases
- In production APIs and tooling, **dataTransfer** shows up whenever teams ship…
