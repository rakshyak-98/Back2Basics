## Create custom function in mongoose schema

#### Instance method ( Custom method for a single document)
- use `schema.methods` to define methods for individual documents.
```js
const mongoose = require("mongoose");

const userSchema = new mongoose.Schema({
    username: String,
    email: String,
    password: String,
    role: { type: String, enum: ["admin", "manager", "auditor"], required: true }
});

// Custom method for checking role
userSchema.methods.isAdmin = function () {
    return this.role === "admin";
};

const User = mongoose.model("User", userSchema);

const user = new User({ username: "Alice", role: "admin" });
console.log(user.isAdmin()); // true

```

#### Static methods ( Custom methods for the model )
- use `schema.static` to define methods accessible on the model itself.
```js
userSchema.statics.findByRole = function (role) {
    return this.find({ role });
};

const User = mongoose.model("User", userSchema);

// Example Usage
User.findByRole("manager").then(users => console.log(users));

```

#### Virtuals (Computed fields without storing data)
- use `schema.virtual` to create properties that don't get stored in the database.
```js
userSchema.virtual("displayName").get(function () {
    return `${this.username} (${this.role})`;
});

const user = new User({ username: "Bob", role: "manager" });
console.log(user.displayName); // Bob (manager)

```

#### Middle ware (pre/post Hooks for Lifecycle Events)
- you can modify data before saving.
```js
userSchema.pre("save", function (next) {
    console.log(`Saving user: ${this.username}`);
    next();
});

```