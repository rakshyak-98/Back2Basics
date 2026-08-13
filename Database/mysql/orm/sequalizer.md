[[mysql]] [[database application]] [[mysql connection]] [[mysql query]]

# sequalizer

> Sequelize—Node.js ORM for MySQL, PostgreSQL, and others—maps models to tables with migrations, associations, and connection pooling via underlying drivers.

## Model example

```javascript
const User = sequelize.define('User', {
  email: { type: DataTypes.STRING, unique: true },
}, { tableName: 'users' });

await User.create({ email: 'a@b.com' });
```

## Pool configuration

```javascript
const sequelize = new Sequelize('mydb', 'user', 'pass', {
  host: 'localhost',
  dialect: 'mysql',
  pool: { max: 10, min: 0, acquire: 30000, idle: 10000 },
});
```

## Pitfalls

- N+1 queries with `include` misuse
- Raw SQL still needed for complex reports
- Migrations via `sequelize-cli` — keep in sync with [[database migration]]

Filename note: vault path uses `sequalizer` (typo for Sequelize).

## Sources

- Sequelize Documentation — [https://sequelize.org/docs/v6/](https://sequelize.org/docs/v6/)
- Sequelize — [Connection Pool](https://sequelize.org/docs/v6/other-topics/connection-pool/)
