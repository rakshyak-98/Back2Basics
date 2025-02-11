## How to extend schema
### Using `discriminator()` allow multiple model types withing a single collection

- Example Base `User` Schema with `Admin` and `Manager` Variants 
```js
const mongoose = require("mongoose");

const userSchema = new mongoose.Schema({
    name: String,
    email: String,
    role: { type: String, required: true, enum: ["admin", "manager"] }
});

// Base Model
const User = mongoose.model("User", userSchema);

// Admin Schema (inherits User)
const Admin = User.discriminator("Admin", new mongoose.Schema({
    adminLevel: Number
}));

// Manager Schema (inherits User)
const Manager = User.discriminator("Manager", new mongoose.Schema({
    department: String
}));

const admin = new Admin({ name: "Alice", email: "alice@example.com", role: "admin", adminLevel: 2 });
admin.save();

const manager = new Manager({ name: "Bob", email: "bob@example.com", role: "manager", department: "HR" });
manager.save();

```

> [!INFO] Best for storing all roles in one collection while keeping role-specific fields.

### Using mongoose plugins (Reusable fields & methods)
[[Mongoose plugin]], [[mongoose methods]]
```js
function timestampPlugin(schema) {
    schema.add({ createdAt: { type: Date, default: Date.now } });
}

const userSchema = new mongoose.Schema({ name: String });
userSchema.plugin(timestampPlugin);

const User = mongoose.model("User", userSchema);

```

### Enforce a constant `role` value for each discriminator model
- disable modification using `immutable: true` or schema validation
```js
const Manager = User.discriminator("Manager", new mongoose.Schema({ permissions: [{ resource: String, actions: [String] }] }));

Manager.schema.path("role").default("Manager").immutable(true);
```