[[javascript]] [[IIFC]] [[prototype]] [[polyfills]] [[promise]] [[Callback]]

# self-defining functions

> Self-defining (lazy) function — first call installs a faster replacement implementation, later calls skip setup.

```txt
        self-defining func ──┬── Interview
               ├── Sources
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers probe **self-defining functions** to see if you understand what …

## Sources
- [Wikipedia — self-defining functions](https://en.wikipedia.org/wiki/self-defining_functions) — overview

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

## Mistakes to Avoid
- **Mistake:** **`const request = () => …` can’t reassign**
- **Mistake:** **Exported binding in ESM**
- **Mistake:** **Rarely worth it now**
- **Mistake:** **Always takes slow path:** check Held old reference
- **Mistake:** **Init runs twice:** check Two aliases / copies
- **Mistake:** **Race on first calls:** check Parallel first invokes
- **Mistake:** **Hard to test:** check Hidden redefine

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Self-defining (lazy) function — first call installs a faster replacement impleme…).
- **Con / when not:** **Hot paths with clear branches**
- **Con / when not:** **React render** — never redefine during render.
- **Con / when not:** **Security-sensitive initialize**

## Comparison
- vs [[IIFC]]: know when each applies


### Use cases
- In production APIs and tooling, **self-defining functions** shows up whenever…
