<!-- note-strategy: operational -->
[[npm]]

# moment

> moment — ("2026-03-24") // parse from string

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** moment — ("2026-03-24") // parse from string

**Parsing**
```js
moment("2026-03-24")                    // parse from string
moment(new Date())                      // parse from JS Date
moment("2026-03-24", "YYYY-MM-DD")      // parse with explicit format (safer)
```
**Formatting**
```js
moment().format("YYYY-MM-DD")           // "2026-03-24"
moment().format("MMMM DD")             // "March 24"
```
**Manipulation**
```js
moment().add(1, "days")                 // tomorrow
moment().subtract(1, "days")           // yesterday
moment().add(1, "months")              // next month
```
**Comparison**
```js
moment(a).isSame(moment(b), "day")      // same day check
moment(a).isBefore(moment(b), "day")    // before check
moment(a).isAfter(moment(b), "day")     // after check
moment(a).isSameOrBefore(b, "day")      // same or before
diff(b, "days")                         // difference in days
```
**Converting back to JS Date**
```js
moment().toDate()                       // convert back to native Date


---

## Standard config / commands

```bash
# version + config path
# dry-run when available
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Retry storm | backoff / jitter | Cap retries; circuit break |
| Config drift | plan/apply or lockfile | Single source of truth |
| Poison message | DLQ | Quarantine and alert |

---

## Gotchas

> [!WARNING]
> Make retries safe or you will duplicate side effects.

---

## When NOT to use

- Avoid the tool if a simpler built-in covers the job.

---

## Related

[[npm]]
