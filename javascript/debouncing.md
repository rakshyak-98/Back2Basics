[[throttle]] [[user triggered event]] [[event listener]] [[Optimizing performance]] [[React]] [[referential equality]]

# Debouncing

> Delay function execution until **input stops** for N ms — coalesce burst calls into one — **UI search, resize, autocomplete**.

## Interview Relevance

Interviewers probe **Debouncing** to see if you understand what it does operationally and when it is the wrong tool — not just the definition.

## Sources

- [CSS-Tricks — Debouncing and Throttling](https://css-tricks.com/debouncing-throttling-explained-examples/) — overview
- [Wikipedia — debouncing](https://en.wikipedia.org/wiki/debouncing) — overview

## Core Definition

Each invocation **resets a timer**. Only after `delay` ms of silence does `func` run with the **latest** arguments.

## Key Concepts

- Each invocation **resets a timer**. Only after `delay` ms of silence does `func` run with the **latest** arguments.
- versus [[throttle]]: throttle fires at most once per window **during** continuous events (scroll).

## Technical Details

Each invocation **resets a timer**. Only after `delay` ms of silence does `func` run with the **latest** arguments.

```txt
keystroke t → timer 300ms
keystroke e → reset timer 300ms
keystroke h → reset timer 300ms
(stop)      → fire search("teh")
```

versus [[throttle]]: throttle fires at most once per window **during** continuous events (scroll).

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

Search box: **300 ms** typical; resize: **150–250 ms**.

## Real-World Applications

In production APIs and tooling, **debouncing** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **New debounce every render** — defeats purpose; memoize or use `useCallback` + ref pattern; **Debounce submit** — user expects immediate click; debounce input only, not form submit.

## Pros/Cons or Trade-offs

- **Pro:** Solves the job described above when used in the right layer (Delay function execution until **input stops** for N ms — coalesce burst calls i…).
- **Con / when not:** **Must execute every event** — gaming input, drawing apps — use throttle or raw handler.
- **Con / when not:** **Server-side rate limiting substitute** — debounce is client UX only; enforce limits on API.
- **Con / when not:** **Critical safety actions** — e-stop, payment confirm — never debounce.

## Comparison

vs [[throttle]]: Throttle guarantees periodic runs; debounce collapses a burst into one trailing call. vs [[user triggered event]]: know when each applies — do not treat them as interchangeable. vs [[event listener]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid

- **New debounce every render** — defeats purpose; memoize or use `useCallback` + ref pattern.
- **Debounce submit** — user expects immediate click; debounce input only, not form submit.
- **Never fires:** check Delay too long; fix: Reduce ms; add leading edge
- **Fires too often:** check Debounce not applied; fix: Wrap stable function ref (`useMemo`)
- **Stale closure:** check Old state in handler; fix: Pass refs or recreate debounce on deps
- **Memory leak on unmount:** check Pending timer; fix: `clearTimeout` in cleanup
- **First keystroke lag:** check Trailing-only; fix: `leading: true` for instant first char
