[[javascript]] [[IIFC]] [[prototype]]

# self-defining functions

> Self-defining (lazy) function — first call installs a faster replacement implementation, later calls skip setup.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Detect capability once (feature detect / init), then reassign the function name to a slim version so every later call pays less.

```txt
call #1: detect → redefine fn → run
call #2+: slim fn only
```

| Use | Example |
|-----|---------|
| Feature detect | XHR vs fetch path |
| One-time init | Wire listeners once |
| Polyfill branch | Old API vs new |

---

## Standard config / commands

```js
function request(url) {
  if (typeof fetch === 'function') {
    request = (u) => fetch(u)
  } else {
    request = (u) => Promise.reject(new Error('no fetch'))
  }
  return request(url)
}
```

| Knob | Why it matters |
|------|----------------|
| Reassign same binding | Callers must use the name, not a copied ref |
| Keep signature stable | Don’t surprise callers |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Always takes slow path | Held old reference | Always call via live binding |
| Init runs twice | Two aliases / copies | Single exported function |
| Race on first calls | Parallel first invokes | Guard with flag / mutex |
| Hard to test | Hidden redefine | Inject strategy instead |

---

## Gotchas

> [!WARNING]
> **`const request = () => …` can’t reassign** — use `let` or object property.

> [!WARNING]
> **Exported binding in ESM** — live bindings work; destructured copies don’t update.

> [!WARNING]
> **Rarely worth it now** — feature detect at module load is clearer.

---

## When NOT to use

- **Hot paths with clear branches** — ordinary `if` is fine and debuggable.
- **React render** — never redefine during render.
- **Security-sensitive init** — explicit setup function.

---

## Related

[[IIFC]] [[polyfills]] [[promise]] [[Callback]]
