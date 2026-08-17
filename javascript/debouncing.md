[[throttle]] [[user triggered event]] [[event listener]] [[Optimizing performance]] [[React]] [[referential equality]]

# Debouncing

> Delay function execution until **input stops** for N ms — coalesce burst calls into one — **UI search, resize, autocomplete**.

```txt
        Debouncing ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers probe **Debouncing** to see if you understand what it does opera…

## Sources
- [CSS-Tricks — Debouncing and Throttling](https://css-tricks.com/debouncing-throttling-explained-examples/) — overview
- [Wikipedia — debouncing](https://en.wikipedia.org/wiki/debouncing) — overview

## Key Concepts
- **Each invocation:** Each invocation **resets a timer**
- **versus [[throttle]]:** versus [[throttle]]: throttle fires at most once per window **during** contin…


- **Core:** Each invocation **resets a timer**

## Technical Details
- Each invocation **resets a timer**.
- Only after `delay` ms of silence does `func` run with the **latest** argument…

```txt
keystroke t → timer 300ms
keystroke e → reset timer 300ms
keystroke h → reset timer 300ms
(stop)      → fire search("teh")
```

- versus [[throttle]]: throttle fires at most once per window **during** contin…

| Use debounce | Use throttle |
|--------------|--------------|
| Search input | Scroll handler |
| Window resize layout | Button spam guard (sometimes) |
| Auto-save draft | Live progress bar |

```javascript
function debounce(func, delay) {
  let timer;
  return function (...args) {
    clearTimeout(timer);
    timer = setTimeout(() => func.apply(this, args), delay);
  };
}
```

### Leading + trailing (lodash-style)

```javascript
function debounce(func, wait, { leading = false } = {}) {
  let timer, invoked = false;
  return function (...args) {
    if (leading && !timer) func.apply(this, args);
    clearTimeout(timer);
    timer = setTimeout(() => {
      if (!leading || invoked) func.apply(this, args);
      timer = null;
      invoked = true;
    }, wait);
  };
}
```

### React usage

```tsx
const debouncedSearch = useMemo(
  () => debounce((q: string) => fetchResults(q), 300),
  []
);
useEffect(() => () => debouncedSearch.cancel?.(), [debouncedSearch]); // if using lodash
```

- Search box: **300 ms** typical; resize: **150–250 ms**.

## Mistakes to Avoid
- **Mistake:** **New debounce every render**
- **Mistake:** **Debounce submit**
- **Mistake:** **Never fires:** check Delay too long
- **Mistake:** **Fires too often:** check Debounce not applied
- **Mistake:** **Stale closure:** check Old state in handler
- **Mistake:** **Memory leak on unmount:** check Pending timer
- **Mistake:** **First keystroke lag:** check Trailing-only

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Delay function execution until **input stops** for N ms — coalesce burst calls i…).
- **Con / when not:** **Must execute every event**
- **Con / when not:** **Server-side rate limiting substitute**
- **Con / when not:** **Critical safety actions**

## Comparison
- vs [[throttle]]: Throttle guarantees periodic runs; debounce collapses a burs…


### Use cases
- In production APIs and tooling, **debouncing** shows up whenever teams ship N…
