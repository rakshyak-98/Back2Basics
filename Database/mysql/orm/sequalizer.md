[[mysql]] [[database application]] [[mysql connection]] [[mysql query]] [[database migration]] [[mysql pool connection]]

# sequalizer

> Sequelize — Node.js ORM for MySQL, PostgreSQL, and others — maps models to tables with migrations, associations, and driver-level connection pools.

```txt
        sequalizer ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** ORM reviews test N+1 awareness, transaction boundaries, and when to drop t…

## Sources
- [Sequelize docs v6](https://sequelize.org/docs/v6/) — overview
- [Connection Pool](https://sequelize.org/docs/v6/other-topics/connection-pool/) — deep-dive

## Key Concepts
- **Models ↔ tables:** Attributes become columns; associations become FKs/joins.
- **Query API vs raw:** Convenience until complex SQL or performance bites.
- **Pool:** Configured on the Sequelize instance ([[mysql pool connection]]).
- **Migrations:** `sequelize-cli` must stay aligned with [[database migration]] practice.

## Technical Details
```javascript
const User = sequelize.define('User', {
  email: { type: DataTypes.STRING, unique: true },
}, { tableName: 'users' });

await User.create({ email: 'a@b.com' });

const sequelize = new Sequelize('mydb', 'user', 'pass', {
  host: 'localhost',
  dialect: 'mysql',
  pool: { max: 10, min: 0, acquire: 30000, idle: 10000 },
});
```

## Mistakes to Avoid
- **Mistake:** Loading nested `include` trees that explode into N+1
- **Mistake:** Letting migration history diverge from production schema
- **Mistake:** Ignoring pool sizing when horizontally scaling Node processes

## Pros/Cons or Trade-offs
- **Pro:** Fast CRUD, portable dialects, built-in pool and migrations.
- **Con:** N+1 via careless `include`; leaky abstractions on advanced SQL.
- **Trade-off:** ORM productivity vs explicit SQL clarity for hot paths.

## Comparison
- vs query builders (Knex) / raw drivers: Sequelize adds models and lifecycle h…


### Use cases
- Node services talking to MySQL with model CRUD for simple domains and `sequel…
