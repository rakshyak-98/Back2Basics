`lean()` 
Avoid the overhead of Mongoose wrapper functions and features.
- used in Mongoose ORM to optimize performance for read-heavy opeartions.
- can not use methods like `.save()` or `.validate()` on lean query results.
- read-only use, not suitable for operations requiring updates or additional mongoose methods.

> [!NOTE] as `populate()` normally returns Mongoose documents. When combined with `lean()`, it ensures even the populated fields are returned as plain JavaScript objects.

### Validate schema
```js
const validateDoc = new ApplicationSchema(
	{
		student: new Types.ObjectId(studentId),
		status,
	},
	{ new: true }
);
console.log(validateDoc);

await validateDoc.validate({ pathsToSkip: ["program"] });
const application = await ApplicationSchema.updateOne(
	{
		_id: new Types.ObjectId(applicationId),
		student: new Types.ObjectId(studentId),
	},
	{ $set: { status } },
	{ new: true }
);
res.json({
	success: {
		message: "Application updated successfully",
		data: application,
	},
});
```

## Custom sequences for categories (100xxx, 200xxx etc.)
- To generate category-based sequences, you need a separate counter per category.
```js
const CounterSchema = new mongoose.Schema({
  category: String,
  seq: { type: Number, default: 1000 }
});

const Counter = mongoose.model('Counter', CounterSchema);

const productSchema = new mongoose.Schema({
  _id: mongoose.Schema.Types.ObjectId,
  productId: Number,
  category: String,
  name: String,
  price: Number
});

productSchema.pre('save', async function(next) {
  if (!this.productId) {
    const counter = await Counter.findOneAndUpdate(
      { category: this.category },
      { $inc: { seq: 1 } },
      { new: true, upsert: true }
    );
    this.productId = parseInt(`${this.category}${counter.seq}`);
  }
  next();
});

const Product = mongoose.model('Product', productSchema);

```

## Mongoose plugin Solution for sequence
[[Mongoose plugin]]

```js
const mongoose = require('mongoose');
const AutoIncrement = require('mongoose-sequence')(mongoose);

const productSchema = new mongoose.Schema({
  _id: mongoose.Schema.Types.ObjectId,
  productId: Number,
  category: String,
  name: String,
  price: Number
});

productSchema.plugin(AutoIncrement, { 
  inc_field: 'productId', 
  start_seq: 1001 
});

const Product = mongoose.model('Product', productSchema);

```