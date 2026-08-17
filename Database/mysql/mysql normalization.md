[[SQL normalization]] [[mysql table]] [[Database design]] [[key Constraint]]

# mysql normalization

> Applying normal forms in MySQL schema design—separate entities into tables linked by foreign keys so updates do not leave inconsistent duplicates.

```txt
        mysql normalizatio ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Normalization questions want 3NF intuition, FK links in MySQL, and deliberate…

## Sources
- Codd normalization principles — deep-dive
- [[SQL normalization]] vault note — overview
- [MySQL Reference Manual — Foreign Keys](https://dev.mysql.com/doc/refman/en/create-table-foreign-keys.html) — overview

## Key Concepts
- **Separate entities:** avoid repeating `customer_name` on every order row.
- **FK links:** InnoDB foreign keys enforce relationships ([[key Constraint]]).
- **Denormalize deliberately:** cached columns need triggers, batch jobs, or app events.

## Technical Details
- Practical 3NF example

```sql
CREATE TABLE customers (id BIGINT PRIMARY KEY, name VARCHAR(200));
CREATE TABLE orders (
  id BIGINT PRIMARY KEY,
  customer_id BIGINT NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES customers(id)
);
```

- Denormalize deliberately: cache columns (`order_count` on `users`) need refre…

## Mistakes to Avoid
- **Mistake:** Stopping at “we normalized” without indexes on FK columns
- **Mistake:** Denormalizing for hypothetical reads without measuring
- **Mistake:** Duplicating mutable fields across tables with no single source o…

## Pros/Cons or Trade-offs
- **Pro:** Updates change one place; FKs prevent orphan rows; storage and clarity improve.
- **Con:** More joins on read paths; denormalized caches drift without explicit refresh.

## Comparison
- vs [[SQL normalization]]: theory and normal forms live there


### Use cases
- Refactoring a wide “god table” into customers/orders/items
