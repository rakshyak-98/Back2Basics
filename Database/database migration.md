[[Database]] [[Alter table]] [[mysql data migrations]] [[ACID]]

# database migration

> One-line: versioned, reversible schema changes applied in order — single source of truth for DDL; never edit applied migrations.

## Mental model

Migrations are timestamped scripts with **up** (apply) and **down** (rollback) steps. A tracking table (`schema_migrations`, `flyway_schema_history`, `_prisma_migrations`) records what's applied so each environment converges to the same shape.

```
Repo migrations/          Database
├── 001_create_users.sql  → migrations table: 001 ✓
├── 002_add_email.sql     → pending until migrate up
└── 003_index_orders.sql
```

Workflow: **generate → define → run → track**. Lack of migrations → schema drift between dev/staging/prod and undebuggable deploy failures.

## Standard config / commands

### SQL-style up/down

```sql
-- 002_add_email.up.sql
ALTER TABLE users ADD COLUMN email VARCHAR(255);

-- 002_add_email.down.sql
ALTER TABLE users DROP COLUMN email;
```

### Node / ORM examples

```bash
npm run migrate up          # Knex, Sequelize CLI patterns
npx prisma migrate deploy   # production apply
npx prisma migrate dev      # dev: apply + regenerate client
```

```javascript
// Knex migration export
export async function up(knex) {
  await knex.schema.alterTable('users', (t) => {
    t.string('email');
  });
}
export async function down(knex) {
  await knex.schema.alterTable('users', (t) => {
    t.dropColumn('email');
  });
}
```

### Go / golang-migrate

```bash
migrate -path db/migrations -database "$DATABASE_URL" up
migrate -path db/migrations -database "$DATABASE_URL" down 1
```

### Flyway

```bash
flyway migrate
flyway info
```

### Safety checks before prod

```bash
# dry-run on staging snapshot
# measure lock time on largest table
# ensure app backward compatible (old code + new schema)
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Migration partially applied | Tool-specific history table | Repair row; manual complete or rollback; restore backup worst case |
| `duplicate column` on re-run | Migration not idempotent | Fix forward-only new migration; don't re-run edited file |
| Down fails | Destructive down (DROP with data) | Restore from backup; write compensating up migration |
| Prod deploy blocked | Long DDL lock | Online schema change tool; expand-contract pattern |
| Drift: DB ≠ repo | Manual hotfix in prod | Export diff; create migration to match; ban manual prod DDL |
| Different checksum | Edited old migration file | Never edit applied; new migration to fix |

## Gotchas

> [!WARNING]
> **Never edit migrations after merge to main** — teammates/CI already applied; add new file instead.

> [!WARNING]
> **Data migrations in same txn as DDL** — huge table UPDATE locks; batch in application job.

> [!WARNING]
> **Down untested** — rollback in incident will fail; test down on staging regularly.

> [!WARNING]
> **Seeding ≠ migrations** — seed data is separate ([[database seeding]]).

## When NOT to use

- **Throwaway local DB** — `schema:drop` / recreate OK in dev only.
- **Blue/green with dual schema** — advanced; still track changes but deploy strategy differs.

## Related

[[migration]] [[Alter table]] [[mysql data migrations]] [[database seeding]] [[Database mistakes]]
