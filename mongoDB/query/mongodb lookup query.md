> [!INFO] `preserveNullAndEmptyArrays` in `$unwind`
> - is optional parameter is MongoDB's `$unwind` stage.
> - it controls whether documents that have `null` or empty arrays in the specified field should be preserved or removed from the aggregation result.

```js
[
    // Join orders with users based on userId field
    {
        $lookup: {
            from: 'users',          // Reference to the 'users' collection
            localField: 'userId',   // Field in 'orders' collection
            foreignField: '_id',    // Field in 'users' collection
            as: 'userDetails'       // The result will be an array in this field
        }
    },
    // Project the data, renaming the 'userDetails' array fields
    {
        $project: {
            orderId: 1,
            amount: 1,
            'userDetails.name': 1,  // Include 'name' from the populated user
            'userDetails._id': 0    // Optionally exclude '_id' from userDetails
        }
    }
]
```

```js
[
  {
    $lookup: {
      localField: "universityId",
      foreignField: "_id",
      from: "users",
      as: "university",
    }
  },
  {
    $match: {
      $expr :{$gt: [{$size: "$university"}, 0]}  
    }
  },
  {
    $project: {
      university: 1
    }
  }
]
```

### Lookup multiple filed
```js
[
  {
    "$lookup": {
      "from": "programs",
      "localField": "program",
      "foreignField": "_id",
      "as": "program"
    }
  },
  {
    "$lookup": {
      "from": "courses",
      "localField": "course",
      "foreignField": "_id",
      "as": "course"
    }
  },
  {
    "$lookup": {
      "from": "teachers",
      "localField": "teacher",
      "foreignField": "_id",
      "as": "teacher"
    }
  },
]
```
## Populate single object instead of array
you can use the `$lookup` stage followed by the `$unwind` stage.

> [!INFO] The `$unwind` stage deconstructs the array from `$lookup` into individual objects.

```js
db.posts.aggregate([
    // Lookup to join 'users' collection with 'posts'
    {
        $lookup: {
            from: "users",              // Reference to 'users' collection
            localField: "authorId",     // Field in 'posts' collection
            foreignField: "_id",        // _id in 'users' collection
            as: "authorDetails"         // Output array of matched users
        }
    },
    // Unwind the 'authorDetails' array to convert it into a single object
    {
        $unwind: {
            path: "$authorDetails",     // Field to unwind
            preserveNullAndEmptyArrays: true // Retain posts even if no match is found
        }
    },
    // Lookup to join 'categories' collection with 'posts'
    {
        $lookup: {
            from: "categories",         // Reference to 'categories' collection
            localField: "categoryId",   // Field in 'posts' collection
            foreignField: "_id",        // _id in 'categories' collection
            as: "categoryDetails"       // Output array of matched categories
        }
    },
    // Unwind the 'categoryDetails' array to convert it into a single object
    {
        $unwind: {
            path: "$categoryDetails",   // Field to unwind
            preserveNullAndEmptyArrays: true // Retain posts even if no match is found
        }
    },
    // Project to shape the result, showing only relevant fields
    {
        $project: {
            title: 1,
            content: 1,
            authorDetails: 1,           // Include author details as an object
            categoryDetails: 1          // Include category details as an object
        }
    }
]);

```

### Populate single field value instead of object
```js
[
  {
    $lookup: {
      from: "users",
      as: "universityId",
      localField: 'universityId',
      foreignField: '_id'
    }
  },
  {
    $unwind: {
      path: "$universityId",
      preserveNullAndEmptyArrays: true
    }
  },
  {
    $project: {
      universityName: "$universityId.name", // populating a single value
    }
  }
]
```

```js
db.posts.aggregate([
    // Lookup to join 'users' collection with 'posts'
    {
        $lookup: {
            from: "users",
            let: { authorId: "$authorId" }, // Pass the local field as a variable
            pipeline: [
                { $match: { $expr: { $eq: ["$_id", "$$authorId"] } } }, // Match the author
                { $project: { _id: 0, name: 1 } } // Include only the 'name' field
            ],
            as: "authorDetails"
        }
    },
    // Unwind the 'authorDetails' array to get a single object
    {
        $unwind: {
            path: "$authorDetails",
            preserveNullAndEmptyArrays: true
        }
    },
    // Project the final shape of the result
    {
        $project: {
            authorName: "$authorDetails.name", // Rename field
        }
    }
]);

```

### Why does a MongoDB supports a `pipeline`?
it is used to perform more complex joins, Instead of just a simple match `localField` <-> `foreignField`
- you can filter, project, and transform the joined documents before returning them.
- you can project only the required ones.
- aggregation operations on joined data -> user `$match`  `$project` `$group` `$sort` inside a lookup.

```js
[
  {
    "$lookup": {
      "from": "programs",
      "let": { "programId": "$program" },
      "pipeline": [
        { "$match": { "$expr": { "$eq": ["$_id", "$$programId"] } } },
        { "$match": { "status": "active" } },
        { "$project": { "_id": 1, "programName": 1 } }
      ],
      "as": "program"
    }
  }
]

```
- `$expr` allows matching using a **variable** from `$let`.

> [!INFO] If you use the `pipeline` property in `$lookup`, you do not need to specify `localField` or `foreignField`.
> - instead you use `$let` to pass values from the main collection and `$expr` inside the `pipeline` to dynamically match fields.

```js
{
  "$lookup": {
    "from": "programs",
    "let": { "programId": "$program" },  
    "pipeline": [
      {
        "$match": {
          "$expr": { "$eq": ["$_id", "$$programId"] }
        }
      },
      {
        "$match": { "status": "active" }  // Additional filtering
      },
      {
        "$project": { "_id": 1, "programName": 1 } // Keep only required fields
      }
    ],
    "as": "programDetails"
  }
}

```