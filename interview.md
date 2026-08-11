[[interview.md]]

# Indexing

> Indexing — what is functional dependency means ?

---

## Mental model

**Say it in one breath:** Indexing — what is functional dependency means ?

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


---

## Related

[[interview.md]]
