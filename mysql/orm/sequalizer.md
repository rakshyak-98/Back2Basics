## Hooks

```js
const { Model, DataTypes } = require('sequelize');

class Product extends Model {}

Product.init({
  name: DataTypes.STRING,
  price: DataTypes.FLOAT,
  slug: DataTypes.STRING
}, { 
  sequelize, 
  modelName: 'product' 
});

// Using addHook for specific events
Product.addHook('beforeValidate', (product, options) => {
  if (product.name) {
    // Automatically creating a URL-friendly slug
    product.slug = product.name.toLowerCase().replace(/ /g, '-');
  }
});
```

> [!NOTE]
> **`individualHooks: true`**: When performing updates or deletes on multiple rows (e.g., `User.update({ status: 'active' }, { where: { id: 1 } })`), standard hooks won't run. Developers often forget they must pass `{ individualHooks: true }` in the options to trigger them.

> [!WARNING]
> Putting heavy business logic (like sending emails or generating PDFs) inside hooks. This couples your database layer to your service layer. If a migration runs or a seed script executes, you might accidentally trigger thousands of emails.

**Ensure that plain text passwords never touch database storage**
```js
const { Model, DataTypes } = require('sequelize');
const bcrypt = require('bcrypt');

class User extends Model {}

User.init({
  username: DataTypes.STRING,
  password: {
    type: DataTypes.STRING,
    allowNull: false
  }
}, {
  sequelize,
  modelName: 'user',
  hooks: {
    beforeSave: async (user, options) => {
      // 'changed' is a Sequelize method to check if the field was modified
      if (user.changed('password')) {
        const saltRounds = 10;
        user.password = await bcrypt.hash(user.password, saltRounds);
      }
    }
  }
});
```

- **Double Hashing**: If you have a hash logic in `beforeCreate` AND `beforeUpdate`, and you don't check if the field has changed, you might hash the already-hashed string during a profile update. This makes the password impossible to verify during login.