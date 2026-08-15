[[Prisma]] [[Database/Data access patterns]]

# Prisma query

> Type-safe database access via the generated client — `findMany`, filters, pagination, and nested `include`/`select` for relations.

## Interview Relevance

Interviewers look for N+1 awareness (`include` vs separate queries), `select` for payload shape, and transactions for multi-step writes.

## Sources

- [Prisma — CRUD](https://www.prisma.io/docs/orm/prisma-client/queries/crud) — deep-dive
- [Prisma — Relation queries](https://www.prisma.io/docs/orm/prisma-client/queries/relation-queries) — overview

## Key Concepts

- **Filters:** `where`, `orderBy`, `take`/`skip`.
- **`include` vs `select`:** whole relations vs precise fields.
- **Nested writes:** create/connect relations in one call when appropriate.
- **Transactions:** `$transaction` for all-or-nothing multi-query flows.

## Technical Details

```ts
const users = await prisma.user.findMany({
  where: { email: { endsWith: "@example.com" } },
  include: { posts: true },
  take: 20,
});

await prisma.$transaction([
  prisma.account.update({ where: { id: a }, data: { balance: { decrement: 10 } } }),
  prisma.account.update({ where: { id: b }, data: { balance: { increment: 10 } } }),
]);
```

| Pitfall | Fix |
|---------|-----|
| Over-fetch | `select` only needed fields |
| N+1 in loops | `include` or batched queries |
| Partial failure | interactive/sequential `$transaction` |

## Real-World Applications

Admin list pages with filters + related counts; checkout flows wrapped in transactions.

**Example:** Loop `findUnique` per id from a list — replace with `findMany({ where: { id: { in: ids } } })`.

## Pros/Cons or Trade-offs

- **Pro:** Readable queries with compile-time field checks.
- **Con:** Huge nested includes can become accidental cartesian products — inspect SQL.

## Comparison

- vs raw SQL: Prisma wins CRUD speed; raw wins bespoke reports.
- vs [[Prisma]]: client generation enables these typed calls.

## Mistakes to Avoid

- Blind `include` trees on hot paths.
- Catching and ignoring failed transactions.
- Assuming client-side filtering is as cheap as `where`.
