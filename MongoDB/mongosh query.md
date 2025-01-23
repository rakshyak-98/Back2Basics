### search query
```js
{ $regex: search, $options: "i" }

```

### Find the type reference 
```js
const mongoose = require('mongoose');

// Replace 'YourModel' with your Mongoose model
YourModel.find({ category: { $type: 'objectId' } })

YourModel.find({
  category: { 
    $type: 'objectId'  // Matches fields of type ObjectId
  },
  $expr: { 
    $not: { $isArray: "$category" }  // Ensures category is not an array
  }
})
```
### `$expr`
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
### `$elementMatch`

```js
{ "numbers": { "$elemMatch": { "$gt": 5, "$lt": 10 } } }
```
- Array `[3,6,11]` matches because `6` satisfies both `$gt` and `$lt`.

query operator used to match one or more elements of an array that satisfy all the specified conditions in a single query.
- matches individual elements of an array.
- ensures all conditions are met by the same element in the array.
- can be used in query filters and projections.

### Sub-documents query element match
```js
db.collection.find({ "tasks": { "$elemMatch": { "task": "coding", "hours": { "$gt": 3 } } } })
```

##### Projection example
```js
db.collection.find({}, { "tasks": { "$elemMatch": { "hours": { "$gt": 3 } } } })
db.collection.find({}, { tasks: { $elemMatch: { priority: "high" } } })
```

---
### Date difference
```js
agg = [
  {
    '$addFields': {
      dateDifferenceInMilliseconds: { '$subtract': [ '$endDate', '$startDate' ] }
    }
  },
  {
    '$project': {
      dateDifferenceInDays: { '$divide': [ '$dateDifferenceInMilliseconds', 86400000 ] },
      startDate: 1,
      endDate: 1
    }
  },
  { '$match': { dateDifferenceInDays: { '$gt': 1 } } }
]

db.collection.aggrigate(agg);
```

## Populate reference

### Formatting date in query
```js
{
	$project: {
		programTitle: "$program.programTitle",
		programType: "$program.programType",
		status: "$status",
		appliedOn: {
			$dateToString: {
				format: "%B %d %Y",
				date: "$createdAt",
			},
		},
		universityName: "$program.university.name",
	},
}
```