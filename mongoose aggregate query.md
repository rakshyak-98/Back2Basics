```js
Order.aggregate([
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
])
.then(result => console.log(result))
.catch(error => console.error(error));
```

## Populate single object instead of array
To get a **single object** instead of an array for the `$lookup` results in MongoDB aggregation, you can use the `$lookup` stage followed by the `$unwind` stage. The `$unwind` stage deconstructs the array from `$lookup` into individual objects.
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

### Populate single value instead of object
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
      universityName: "$universityId.name",
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