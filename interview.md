# Indexing

> One-line: what / why for **Indexing** — source TBD.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

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

## Standard config / commands

…

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| … | … | … |

## Gotchas

> [!WARNING]
> …

## When NOT to use

…

## Related

[[…]]
