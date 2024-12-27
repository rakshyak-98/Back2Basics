[mongodb aggregation](https://www.mongodb.com/docs/v4.4/reference/operator/aggregation/cond/)

> [!WARNING] On some systems, a password provided directly in a connection string or using `--uri` may be visible to system status programs such as `ps` that may be invoked by other users. 

```js
{ $cond: { if: <boolean-expression>, then: <true-case>, else: <false-case> } }
```

```js
{ $cond: [ <boolean-expression>, <true-case>, <false-case> ] }
```

```js
db.collection.aggregate([{ $project: {name: 1, age: 1, _id: 0}}])
db.collection.aggregate([
	{ $group: { _id: "$category", total: {$sum: "$price"}}}
])
db.collection.aggregate([{ $sort: {age: -1}}])
db.collection.aggregate([{ $match: { status: "active" }}])
db.orders.aggregate([
	{
		$lookup: {
			from: "customers",
			localField: "customerId",
			foreignField: "_id",
			as: "customerDetails"
		}
	}
])
db.collection.aggregate([
	{ $addFields: { totalPrice: { $multiply: ["$price", "$quantity"]}}}
])
db.collection.aggregate([{ $unwind: "$items" }])
```

```js
db.collection.aggregate([{ $search: {text: { query: "mongodb", path: "title" }}}])
```

```js
// Handling Dates
db.collection.aggregate([
	{ $project: {formatDate: {$dateToString: {format: "%Y-%m-%d", date: "$createdAt" }}}}
])
```

```js
db.collection.aggregate([
	{
		$project: {
			priceCategory: {
				$cond: {if : {$gt: ["$price", 100]}, then: "High", else: "Low" }
			}
		}
	}
])
```

```js
db.collection.aggregate([{ $skip: 10 }, { $limit: 5 }])
```

```js
// data sampling Randomly select documents
db.collection.aggregate([{ $sample: { size: 3 }}])
```

```js
// $merge Write aggregation result into a collection.
db.collection.aggregate([
	{ $group: { _id: "$category", total: { $sum: "$price" }}},
	{ $merge: "summary" }
])
```

```js
// Run multiple aggregations in parallel
db.collection.aggregate([
	{
		$facet: {
			ageStats: [{ $group: {_id: null, avgAge: { $avg: "$age" }}}],
			locationCounts: [{ $group: {_id: "$location", count: { $sum: 1 }}}]
		}
	}
])
```

```js
db.collection.aggregate([
	{$project: {nameUpperCase: {$toUpper: "$name" }}}
])
```