[[javascript]] [[event listener]]

# dataTransfer

> `dataTransfer` — drag-and-drop / clipboard payload bag: set data on dragstart, read on drop (types + files).

## Mental model

**Say it in one breath:** On drag (or copy), you write MIME-typed strings/files into `event.dataTransfer`; the drop target reads them. Browsers restrict reads until drop/paste for security.

```txt
dragstart: setData / files
   ↓
dragover: preventDefault (to allow drop)
   ↓
drop: getData / files
```

| Field | Role |
| --- | --- |
| `setData(type, str)` | App payload (`text/plain`, custom) |
| `files` | FileList from OS drag |
| `dropEffect` / `effectAllowed` | Copy vs move UX |
| `items` | Modern typed items API |

## Standard config / commands

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

| `preventDefault` on dragover | Without it, drop won’t fire |
| --- | --- |
| Custom MIME | `application/x-myapp` for internal |
| `readAsDataURL` separately | Files need FileReader/fetch |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Drop never fires | Missing dragover preventDefault | Add it |
| `getData` empty mid-drag | Read too early | Only on `drop`/`paste` |
| Files empty | Not a file drag / browser | Check `items`; permissions |
| Cross-origin iframe | Restricted | Same-origin or postMessage |
| Safari quirks | Custom types | Also set `text/plain` |

## Gotchas

> [!WARNING]
> **Don’t put secrets in drag data** — any drop target can read on drop.

> [!WARNING]
> **`text/uri-list` vs `text/plain`** — browsers differ; set both if needed.

> [!WARNING]
> **React synthetic DnD** — still need `preventDefault` on dragover.

## When NOT to use

- **Complex application DnD** — pointer events + state may be simpler than HTML5 DnD.
- **Large binary pipelines** — upload APIs, not drag strings.
- **Mobile** — HTML5 DnD support is weak; use touch UX.

## Related

[[event listener]] [[Callback]] [[mime type]]
