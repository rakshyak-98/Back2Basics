### **Choosing the Right Solution**  
The choice of design pattern depends on:  
1. **Access patterns**: How the data is read and written.  
2. **Scalability needs**: Whether horizontal scaling is a priority.  
3. **Data size and structure**: Document size limits and data relationships.  
4. **Flexibility**: Requirements for frequent schema changes.  

---
### 1. **Embedding (Denormalization)**  
- **Description**:  
  Store related data in a single document.  
  Example: Embed `order` and `items` into one document.  
  ```json
  {
    "order_id": 1,
    "customer": { "name": "Alice", "email": "alice@example.com" },
    "items": [
      { "product": "Laptop", "quantity": 1 },
      { "product": "Mouse", "quantity": 2 }
    ]
  }
  ```
- **Use Case**:  
  - When related data is frequently queried together.  
  - Example: E-commerce orders and items.
- **Analysis**:  
  - **Advantages**:  
    - Faster reads (no joins).  
    - Simpler query logic.  
  - **Disadvantages**:  
    - Document size limits (16MB).  
    - Updating embedded data can be costly.

---

### 2. **Referencing (Normalization)**  
- **Description**:  
  Store related data in separate collections and reference by `_id`.  
  Example: Separate `orders` and `customers`.  
  ```json
  // Orders Collection
  {
    "order_id": 1,
    "customer_id": 101,
    "items": [201, 202]
  }
  // Customers Collection
  {
    "customer_id": 101,
    "name": "Alice",
    "email": "alice@example.com"
  }
  ```
- **Use Case**:  
  - When data relationships are many-to-many or frequently updated.  
  - Example: Large catalogs, social media.
- **Analysis**:  
  - **Advantages**:  
    - Smaller documents.  
    - Easier updates for referenced data.  
  - **Disadvantages**:  
    - Slower queries requiring multiple lookups.  
    - Increased application complexity for joins.

---

### 3. **Bucket Pattern**  
- **Description**:  
  Group related data into buckets to reduce the number of documents.  
  Example: Time-series data.  
  ```json
  {
    "sensor_id": "A1",
    "date": "2025-01-07",
    "readings": [
      { "time": "10:00", "value": 23 },
      { "time": "11:00", "value": 24 }
    ]
  }
  ```
- **Use Case**:  
  - High-frequency, time-based data like IoT sensor readings.  
- **Analysis**:  
  - **Advantages**:  
    - Reduces query count.  
    - Efficient for grouped reads.  
  - **Disadvantages**:  
    - Difficult to update individual entries.  
    - Buckets can grow too large.

---

### 4. **Outlier Pattern**  
- **Description**:  
  Separate outliers into a different collection to handle size constraints.  
  Example: For orders with unusually high item counts.  
  ```json
  // Regular Collection
  { "order_id": 1, "items": [...] }
  // Outlier Collection
  { "order_id": 1, "extra_items": [...] }
  ```
- **Use Case**:  
  - When a small percentage of documents exceed size limits.  
- **Analysis**:  
  - **Advantages**:  
    - Avoids document size issues.  
    - Retains efficient queries for most data.  
  - **Disadvantages**:  
    - Increased complexity to handle outliers.

---

### 5. **Tree Structure (Parent-Child Relationship)**  
- **Description**:  
  Store hierarchical data as a tree.  
  Example: Employee management structure.  
  ```json
  {
    "employee_id": 1,
    "name": "Alice",
    "manager_id": null,
    "subordinates": [2, 3]
  }
  ```
- **Use Case**:  
  - Organizational charts, category hierarchies.  
- **Analysis**:  
  - **Advantages**:  
    - Captures hierarchy in one document.  
    - Reduces query complexity for parent-child relationships.  
  - **Disadvantages**:  
    - Expensive for deeply nested updates.  
    - Difficult to query entire subtrees.

---

### 6. **Polymorphic Pattern**  
- **Description**:  
  Store multiple types of related data in the same collection.  
  Example: A `media` collection with `video` and `audio` types.  
  ```json
  {
    "media_id": 1,
    "type": "video",
    "title": "Sample Video",
    "duration": 120
  }
  ```
- **Use Case**:  
  - When different types share common fields but also have unique attributes.  
- **Analysis**:  
  - **Advantages**:  
    - Flexible schema.  
    - Simplifies queries for shared attributes.  
  - **Disadvantages**:  
    - Schema validation can be challenging.  
    - Increased complexity for type-specific queries.

---

### 7. **Pre-aggregated Data Pattern**  
- **Description**:  
  Store pre-aggregated data for faster analytics.  
  Example: Daily sales totals.  
  ```json
  {
    "date": "2025-01-07",
    "total_sales": 5000
  }
  ```
- **Use Case**:  
  - Dashboards and reporting systems.  
- **Analysis**:  
  - **Advantages**:  
    - Faster analytics queries.  
    - Reduces computational load during peak times.  
  - **Disadvantages**:  
    - Requires careful updates to keep aggregates accurate.  
    - Inflexible for ad-hoc queries.

---

### 8. **Aggregation Framework**  
- **Description**:  
  Use MongoDB’s aggregation pipelines to compute complex queries.  
  Example: Group sales by product category.  
  ```json
  db.sales.aggregate([
    { $group: { _id: "$category", total: { $sum: "$amount" } } }
  ])
  ```
- **Use Case**:  
  - Real-time analytics or complex reporting.  
- **Analysis**:  
  - **Advantages**:  
    - Powerful and flexible querying.  
    - No need for external computation.  
  - **Disadvantages**:  
    - Can become computationally expensive.  
    - Not suitable for extremely large datasets without sharding.

---
