[[mysql]] [[database application]] [[mysql connection]] [[mysql query]] [[database migration]] [[mysql pool connection]]

# sequalizer

> Sequelize — Node.js ORM for MySQL, PostgreSQL, and others — maps models to tables with migrations, associations, and driver-level connection pools.

## Interview Relevance
ORM interviews test N+1 awareness, transaction boundaries, and when to drop to raw SQL. Filename in this vault is the historical typo `sequalizer` for Sequelize.

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

## Real-World Applications
Node services talking to MySQL with model CRUD for simple domains and `sequelize.query` for reporting SQL.

## Pros/Cons or Trade-offs
- **Pro:** Fast CRUD, portable dialects, built-in pool and migrations.
- **Con:** N+1 via careless `include`; leaky abstractions on advanced SQL.
- **Trade-off:** ORM productivity vs explicit SQL clarity for hot paths.

## Comparison
vs query builders (Knex) / raw drivers: Sequelize adds models and lifecycle hooks at the cost of magic. vs other ORMs (Prisma, TypeORM): similar pitfalls, different APIs.

## Mistakes to Avoid
- Loading nested `include` trees that explode into N+1.
- Letting migration history diverge from production schema.
- Ignoring pool sizing when horizontally scaling Node processes.
