Below is **MySQL normalization rules**, **short**, **structured**, **interview-oriented**.

---

## Database Normalization

Goal: **reduce redundancy, avoid anomalies, ensure data consistency**

---

## 1NF – First Normal Form

Rule:

- Atomic values (no arrays, lists)
    
- No repeating groups
    
- Each row uniquely identifiable (PK)
    

Bad:

- `phones = "123,456"`
    

Good:

- Separate table or rows
    

Use when:

- Data is stored in tabular relational form
    

---

## 2NF – Second Normal Form

Rule:

- Must be in 1NF
    
- No **partial dependency** on composite primary key
    

Meaning:

- Non-key column must depend on **full primary key**, not part of it
    

Example issue:

- PK = `(order_id, product_id)`
    
- `product_name` depends only on `product_id`
    

Fix:

- Move product data to `products` table
    

---

## 3NF – Third Normal Form

Rule:
- Must be in 2NF
- No **transitive dependency**

Meaning:
- Non-key column must not depend on another non-key column

Example issue:
- `user_id → city → state`

Fix:
- Separate `city/state` mapping table
    
---

## BCNF – Boyce-Codd Normal Form

Rule:
- Stronger 3NF
- Every determinant must be a **candidate key**
    

When needed:
- Multiple candidate keys
- Functional dependency anomalies still exist in 3NF

Rare but important for correctness

---

## 4NF – Fourth Normal Form

Rule:
- No **multi-valued dependencies**

Example issue:
- One user has multiple skills AND multiple hobbies stored together
    

Fix:
- Separate independent multi-valued attributes

## 5NF – Fifth Normal Form

Rule:
- No **join dependency**
- Decompose until lossless join only

Used when:
- Extremely complex relationships
- Rare in real systems
---

## Normalization vs Performance

Reality:
- 3NF is enough for **most systems**
- BCNF/4NF only when correctness demands it
    
- Denormalization is common for:
    - Read-heavy systems
    - Analytics
    - Reporting
---

## Interview-Ready Summary

- 1NF: atomic values
- 2NF: no partial dependency
- 3NF: no transitive dependency
- BCNF: determinant = candidate key
- 4NF: no multi-valued dependency
- 5NF: no join dependency
---

## Common Edge Cases

- Over-normalization → too many joins
- Indexing required after normalization
- Denormalization acceptable with controlled writes
- ORM-generated schemas often violate 3NF
---

## One-Line Answer (if rushed)

> MySQL normalization means structuring tables to eliminate redundancy and anomalies, typically up to 3NF, while higher forms are applied only when data correctness requires it.

If you want:
- Normalization **with examples**
- Real-world **ecommerce schema**
- When **not** to normalize
