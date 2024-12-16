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
