[[npm]]

# npm error

> npm error — [baseline-browser-mapping] The data in this module is over two months old. To ensure accurate Baseline data, please update: npm i…

---

## How it works

```text
[baseline-browser-mapping] The data in this module is over two months old.  To ensure accurate Baseline data, please update: `npm i baseline-browser-mapping@latest -D`
```
- `baseline-browser-mapping` -> This package maintains a mapping of browser versions that support features in the Web Platform Baseline.
```text
FATAL ERROR: Reached heap limit Allocation failed - JavaScript heap out of memory
```
```bash
NODE_OPTIONS="--max-old-space-size=4096" npm run build
```
Because **Node.js intentionally limits the amount of memory (heap) a JavaScript process can use**.
Without a limit, a buggy application could consume all available RAM and make the entire system unstable.
### What happens internally
```text
npm run build
       ↓
npm starts Node.js
       ↓
Node starts V8 (JavaScript engine)
       ↓
V8 allocates a heap with a maximum size
       ↓
Your application stores objects in the heap
       ↓
Heap becomes full


---

## Standard config / commands

```bash
# version + config path
# dry-run when available
```

---

## Gotchas

> [!WARNING]
> Make retries safe or you will duplicate side effects.

---

## When NOT to use

- Avoid the tool if a simpler built-in covers the job.

---

## Rollback

1. …

## Escalation

…

## Related

[[npm]]

## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| Retry storm | backoff / jitter | Cap retries; circuit break |
| Config drift | plan/apply or lockfile | Single source of truth |
| Poison message | DLQ | Quarantine and alert |

---


## Steps

1. …


## Verification

```bash
# …
```


## Sources

- [Wikipedia — npm error](https://en.wikipedia.org/wiki/npm_error)
