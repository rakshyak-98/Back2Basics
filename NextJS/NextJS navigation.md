### Why you _can’t_ use `router.push(url, '_blank')`
- `router.push()` only updates the current SPA state
- It doesn’t (and shouldn't) deal with browser tabs, windows, or targets
- It is **not like `window.location.href = ...`** (doesn't reload)