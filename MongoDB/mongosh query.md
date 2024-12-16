To fetch documents where the `reportingManager` field contains more than one `ObjectId`, you can use the `$expr` operator to check the length of the array. Here's the query:

```javascript
db.collectionName.find({
  $expr: { $gt: [{ $size: "$reportingManager" }, 1] }
})
```

### Explanation:
1. **`$size`**: Calculates the size of the `reportingManager` array for each document.
2. **`$gt`**: Checks if the size is greater than 1.
3. **`$expr`**: Allows evaluating these expressions within the query.

---

To remove keys (fields) from a document in MongoDB, you can use the `$unset` operator. Here's the query to remove one or more keys from a document:

### Example:

```javascript
db.collectionName.update(
  { _id: ObjectId("documentId") }, // Filter condition
  { $unset: { key1: "", key2: "" } } // Fields to remove
)
```

### Explanation:

- **`$unset`**: This operator removes the specified fields from the document.
- **`key1`, `key2`**: Replace these with the actual field names you want to remove. You can remove multiple fields by adding more key-value pairs (keys as field names and values as empty strings).

---
