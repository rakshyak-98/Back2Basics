[[throttle]] [[user triggered event]] [[event listener]] [[Optimizing performance]] [[React]]

# Debouncing

> Delay function execution until **input stops** for N ms — coalesce burst calls into one — **UI search, resize, autocomplete**.

---

## Mental model

Each invocation **resets a timer**. Only after `delay` ms of silence does `func` run with the **latest** arguments.

```txt
keystroke t → timer 300ms
keystroke e → reset timer 300ms
keystroke h → reset timer 300ms
(stop)      → fire search("teh")
```

vs [[throttle]]: throttle fires at most once per window **during** continuous events (scroll).

| Use debounce | Use throttle |
|--------------|--------------|
| Search input | Scroll handler |
| Window resize layout | Button spam guard (sometimes) |
| Auto-save draft | Live progress bar |

---

## Standard config / commands

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

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Never fires | Delay too long | Reduce ms; add leading edge |
| Fires too often | Debounce not applied | Wrap stable function ref (`useMemo`) |
| Stale closure | Old state in handler | Pass refs or recreate debounce on deps |
| Memory leak on unmount | Pending timer | `clearTimeout` in cleanup |
| First keystroke lag | Trailing-only | `leading: true` for instant first char |

---

## Gotchas

> [!WARNING]
> **New debounce every render** — defeats purpose; memoize or use `useCallback` + ref pattern.

> [!WARNING]
> **Debounce submit** — user expects immediate click; debounce input only, not form submit.

---

## When NOT to use

- **Must execute every event** — gaming input, drawing apps — use throttle or raw handler.
- **Server-side rate limiting substitute** — debounce is client UX only; enforce limits on API.
- **Critical safety actions** — e-stop, payment confirm — never debounce.

---

## Related

[[throttle]] · [[user triggered event]] · [[event listener]] · [[referential equality]] · [[React]]
