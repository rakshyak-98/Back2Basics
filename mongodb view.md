> [!INFO] Views reflect changes made to the underlying collection.
- the view is defined using an aggregation pipeline for flexible transformations. 
- avoids repeating aggregation logic for recurring queries.

### Limitations
- No indexing views cannot have indexes. Queries on views depend on the indexes of the source collection.
- read-only you can't update data through views.
- Complex pipelines in views may slow down queries.

```js
db.createView(
	"orderSummaryView",
	"orders",
	[
		{$group: {_id: "$customerId", totalSpent: {$sum: "$amount" }}},
		{$sort: {totalSpend: -1}}
	]
)
```

- use indexes on the source collection to optimize view performance.
- limit the complexity of aggregation pipelines to avoid performance degradation.
- user views for read-heavy workloads where dynamic updates to the project are needed.