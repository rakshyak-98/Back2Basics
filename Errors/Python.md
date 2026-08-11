[[Errors]]

# Python

> Python — the StaleElementReferenceError occurs when the web element you are trying to interact with is no longer present in the DOM, or the reference to it is

---

## Mental model

**Say it in one breath:** Python — plain job, how I run it, how I know it’s broken.


### `StaleElementReferenceError`
The `StaleElementReferenceError` occurs when the web element you are trying to interact with is no longer present in the DOM, or the reference to it is no longer valid (e.g., the DOM has been refreshed or changed).
This can happen when navigating through different pages or elements within a page (such as opening new folders in Google Drive) because the previously found element is no longer available

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Python** | Core idea of this note | “I can explain Python without jargon.” |
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

[[Errors]]
