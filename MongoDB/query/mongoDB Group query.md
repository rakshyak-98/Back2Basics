### Grouping related fields
```js
{
	$group: {
		_id: "$student",
		programs: { $addToSet: "$result" },
		totalFees: { $sum: "$result.applicationFee" },
		quantity: { $count: {} },
	},
},
```

#### Group on two keys
```shell
[
  {
    "$group": {
      "_id": {
        "student": "$student",
        "otherKey": "$someOtherField"
      },
      "applications": { "$push": "$program" }
    }
  }
]

```
- to group based on two keys, you need to structure `_id` as an object containing both fields in the `$group` stage.

### If you need both count and grouping
```js
[
  { $match: { role: "UNIVERSITY" } },
  {
    $facet: {
      totalCount: [{ $count: "totalResults" }],
      groupedData: [{ $group: { _id: "$country" } }]
    }
  }
]

```
- `$facet` allow multiple operations in parallel:
this approach is useful when you need both the total count and the grouped results without making two separate queries.

- if you want both the grouped data and the total count in one query.
```js
[
  { $match: { role: "UNIVERSITY" } },
  {
    $facet: {
      totalCount: [
        { $group: { _id: "$country" } },
        { $count: "totalGroups" }
      ],
      groupedData: [{ $group: { _id: "$country" } }]
    }
  }
]

```