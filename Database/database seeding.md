[[migration]] [[mysql]] [[postgres essential]] [[Database design]] [[OLTP]]

# Database seeding

> **Initial or repeatable reference data** loaded into schema after migrations — dev fixtures, prod lookup tables, demo tenants. Not a substitute for migrations or prod data backup.

## Mental model

**Migrations** change structure; **seeds** insert rows. Seeds run in **known order**, ideally **idempotent** (safe to re-run in dev/CI). Prod seeds = small, static reference data (roles, countries); **never** fake PII at scale in prod.

```
migrate up ──► schema ready ──► seed (ordered scripts) ──► app can boot
                                      │
                                      └── CI: fresh DB + migrate + seed each run
```

Danger zone: seeding **production** with destructive `TRUNCATE` or non-idempotent inserts → duplicate keys or wiped tables.

## Standard config / commands

### Idempotent SQL pattern

```sql
INSERT INTO roles (id, name) VALUES (1, 'admin'), (2, 'user')
ON CONFLICT (id) DO NOTHING;
-- MySQL: INSERT IGNORE or ON DUPLICATE KEY UPDATE name=VALUES(name)
```

### Node (Knex / Sequelize)

```javascript
// knex/seeds/001_roles.js
exports.seed = async (knex) => {
  await knex('roles').insert([
    { id: 1, name: 'admin' },
    { id: 2, name: 'user' },
  ]).onConflict('id').ignore();
};
```

```bash
npx knex migrate:latest && npx knex seed:run
```

### Rails

```bash
rails db:seed              # db/seeds.rb
rails db:setup             # create + schema + seed
FIXTURES=roles rails db:seed # if split
```

### Prisma

```bash
npx prisma migrate deploy
npx prisma db seed   # "prisma.seed" in package.json → ts node prisma/seed.ts
```

```typescript
// prisma/seed.ts — use upsert for idempotency
await prisma.role.upsert({
  where: { id: 1 },
  update: {},
  create: { id: 1, name: 'admin' },
});
```

### Prod vs dev separation

| Env | Seed content |
|-----|--------------|
| dev/CI | Users, sample orders, feature flags |
| staging | Anonymized subset or synthetic |
| prod | Reference tables only; via reviewed migration or one-off job |

Use env guard:
```javascript
if (process.env.NODE_ENV === 'production' && !process.env.ALLOW_PROD_SEED) {
  throw new Error('Refusing prod seed');
}
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Duplicate key on seed re-run | Non-idempotent inserts | Upsert / ON CONFLICT |
| FK violation during seed | Order wrong (parent after child) | Number seeds; disable FK checks only in dev if must |
| Empty dev DB after clone | Seeds not run in onboarding doc | Document `migrate && seed` in README |
| Prod data corrupted | Ran dev seed against prod DSN | Restore backup; strict env separation |
| Slow CI | Full seed every test | Transaction rollback per test; minimal fixtures |
| Hash/bcrypt users differ | Random salt each run | Fixed salt in test only; deterministic passwords in dev |

## Gotchas

> [!WARNING]
> **`db:seed` in prod deploy pipeline** — most teams use migrations for reference data changes; seeds for dev only.

> [!WARNING]
> **Auto-increment IDs in seeds** — hard-coded ids break when sequences diverge; prefer natural keys or upsert by business key.

> [!WARNING]
> **Large blob seed files in git** — use generation script or S3 import.

> [!WARNING]
> **Seeding before migrations** — tables missing; enforce order in CI script.

## When NOT to use

- **Schema changes** — use [[migration]].
- **Restoring prod after incident** — PITR/backup restore, not seed script.
- **Analytics sample data at scale** — ETL to [[OLAP]] warehouse, not OLTP seed.

## Related

[[migration]] · [[mysql]] · [[postgres essential]] · [[Database design]] · [[OLTP]] · [[database application]]
