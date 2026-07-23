[[Database/mysql/mysql pool connection]] [[Database/postgres/psql keywords]]

# Prisma query

> Type-safe DB access via generated client — `findMany`, relations, filters, and `include` for joins.

## Mental model

Prisma Client maps models in `schema.prisma` to SQL. **Relational loads** use `include` (eager) or nested `select`. Filters use object API (`where`, `orderBy`, `cursor`). Raw SQL escapes hatch via `$queryRaw`. Connection pooling: use PgBouncer-compatible settings for serverless.

```
schema.prisma → prisma generate → PrismaClient → SQL
```

## Standard config / commands

### Fetch with relations

```ts
const users = await prisma.user.findMany({
  where: { active: true },
  include: {
    posts: { select: { id: true, title: true } },
    profile: true,
  },
  orderBy: { createdAt: 'desc' },
  take: 20,
});
```

### Filter patterns

```ts
await prisma.user.findFirst({
  where: {
    email: { equals: email, mode: 'insensitive' },
    OR: [{ role: 'ADMIN' }, { tenantId }],
  },
});
```

### Pagination (cursor)

```ts
await prisma.post.findMany({
  take: 10,
  skip: 1,
  cursor: { id: lastId },
});
```

### Generate after schema change

```bash
npx prisma migrate dev
npx prisma generate
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `Unknown arg include` | Relation in schema? | Add `@relation`; regenerate client |
| N+1 queries | Query log | Use `include` or `select` in one query |
| `P2002` unique violation | Constraint | Upsert or handle conflict |
| Connection pool timeout | Serverless | Data proxy / PgBouncer; lower concurrency |
| Stale client types | Forgot generate | Run `prisma generate` in CI |

## Gotchas

> [!WARNING]
> **`include` everything** — fetches huge graphs; always `select` fields you need.
>
> **Case sensitivity** — PostgreSQL `mode: 'insensitive'` only on supported fields.
>
> **Migrations on prod** — `migrate deploy` in CI, not `db push`.

## When NOT to use

- Don't use Prisma for heavy analytics aggregations — raw SQL or OLAP store.
- Don't `include` deep trees in list endpoints — pagination + separate detail fetch.

## Related

[[Database/connection pooling]] [[Database/mysql/mysql pool connection]] [[Database/postgres/psql keywords]]
