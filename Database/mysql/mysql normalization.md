[[SQL normalization]] [[mysql table]] [[Database design]] [[key Constraint]]

# mysql normalization

> Applying normal forms in MySQL schema design—separate entities into tables linked by foreign keys so updates do not leave inconsistent duplicates.

## Practical 3NF example

Instead of storing `customer_name` on every `order` row:

```sql
CREATE TABLE customers (id BIGINT PRIMARY KEY, name VARCHAR(200));
CREATE TABLE orders (
  id BIGINT PRIMARY KEY,
  customer_id BIGINT NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES customers(id)
);
```

## Denormalize deliberately

Cache columns (`order_count` on `users`) need refresh rules—triggers, batch jobs, or application events.

## Sources

- Codd normalization principles
- [[SQL normalization]] vault note
- MySQL Reference Manual — [Foreign Keys](https://dev.mysql.com/doc/refman/en/create-table-foreign-keys.html)
