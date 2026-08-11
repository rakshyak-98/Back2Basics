[[interview.md]]

# Indexing

> Indexing — what is functional dependency means ?

---

## Mental model

**Say it in one breath:** Indexing — plain job, how I run it, how I know it’s broken.


```js
Object.getPrototypeOf(value).constructor.name; // Get type of any value
```
What is functional dependency means ?
- value can be determined by the value of another attribute.
- refers to the relationship between attributes (columns) within a relation (table).
- single-level index
- multilevel indexes
	- B+ tree have become a commonly accepted default structure for generating indexes on demand in most relational DBMS.
- logical indexes
- bitmap indexes
- popular indexing scheme called [[ISAM]] (indexed sequential access method).
- only create index for performance critical queries.

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Indexing** | Core idea of this note | “I can explain Indexing without jargon.” |
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

[[interview.md]]
