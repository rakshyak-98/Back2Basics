[[RTQ]]

# matcher

> matcher — in Redux Toolkit, multiple matchers for the same event do run sequentially, but splitting them into separate matchers here provides no benefit…

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** matcher — plain job, how I run it, how I know it’s broken.


In Redux Toolkit, multiple matchers for the same event **do run sequentially**, but splitting them into separate matchers here provides **no benefit** because:
1. Both matchers react to the **same event**
2. They don't depend on each other's result
3. There's no side effect or ordering logic between them
The sequential execution only matters when the **second matcher depends on state changed by the first**, for example:
```js
// This makes sense split — second reads what first wrote
.addMatcher(event, (state, action) => {
  state.locations = action.payload?.data;        // sets locations
})
.addMatcher(event, (state, action) => {
  state.selectedHotel = state.locations?.[0];    // reads locations ← depends on above
})
```
But in your code both matchers read directly from `action.payload`, not from each other, so **combining them is identical in behavior:**
```js
.addMatcher(
  api.endpoints.getHotelDetailsWebBooking.matchFulfilled,

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **matcher** | Core idea of this note | “I can explain matcher without jargon.” |
| **mental model** | How it works in one line | “Explain it without jargon first.” |
| **failure mode** | How it breaks | “Say what you check first.” |

---

## Standard config / commands

```bash
# reproduce with minimal input
# compare working vs broken env
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Unexpected result | inputs / versions | Reproduce minimal case |
| Works on one machine | env drift | Diff config and versions |
| Silent failure | logs / metrics | Add checks and alerts |

---

## Gotchas

> [!WARNING]
> Prefer simple words you can say in an interview.

---

## When NOT to use

- Skip it when a simpler existing tool already fits.

---

## Related

[[RTQ]]
