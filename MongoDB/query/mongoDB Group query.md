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