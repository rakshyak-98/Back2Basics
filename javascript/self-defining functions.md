[[javascript]] [[IIFC]] [[prototype]] [[polyfills]] [[promise]] [[Callback]]

# self-defining functions

> Self-defining (lazy) function — first call installs a faster replacement implementation, later calls skip setup.

## Interview Relevance

Interviewers probe **self-defining functions** to see if you understand what it does operationally and when it is the wrong tool — not just the definition.

## Sources

- [Wikipedia — self-defining functions](https://en.wikipedia.org/wiki/self-defining_functions) — overview

## Key Concepts

## Technical Details

```txt
call #1: detect → redefine fn → run
call #2+: slim fn only
```

| Use | Example |
|-----|---------|
| Feature detect | XHR vs fetch path |
| One-time init | Wire listeners once |
| Polyfill branch | Old API vs new |

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

## Real-World Applications

In production APIs and tooling, **self-defining functions** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **`const request = () => …` can’t reassign** — use `let` or object property; **Exported binding in ESM** — live bindings work; destructured copies don’t update.

## Pros/Cons or Trade-offs

- **Pro:** Solves the job described above when used in the right layer (Self-defining (lazy) function — first call installs a faster replacement impleme…).
- **Con / when not:** **Hot paths with clear branches** — ordinary `if` is fine and debuggable.
- **Con / when not:** **React render** — never redefine during render.
- **Con / when not:** **Security-sensitive initialize** — explicit setup function.

## Comparison

vs [[IIFC]]: know when each applies — do not treat them as interchangeable. vs [[prototype]]: know when each applies — do not treat them as interchangeable. vs [[polyfills]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid

- **`const request = () => …` can’t reassign** — use `let` or object property.
- **Exported binding in ESM** — live bindings work; destructured copies don’t update.
- **Rarely worth it now** — feature detect at module load is clearer.
- **Always takes slow path:** check Held old reference; fix: Always call via live binding
- **Init runs twice:** check Two aliases / copies; fix: Single exported function
- **Race on first calls:** check Parallel first invokes; fix: Guard with flag / mutex
- **Hard to test:** check Hidden redefine; fix: Inject strategy instead
