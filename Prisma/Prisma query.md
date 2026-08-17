[[Prisma]] [[Database/Data access patterns]]

# Prisma query

> Type-safe database access via the generated client — `findMany`, filters, pagination, and nested `include`/`select` for relations.

```txt
        Prisma query ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers look for N+1 awareness (`include` vs separate queries), `select`…

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

## Mistakes to Avoid
- **Mistake:** Blind `include` trees on hot paths
- **Mistake:** Catching and ignoring failed transactions
- **Mistake:** Assuming client-side filtering is as cheap as `where`

## Pros/Cons or Trade-offs
- **Pro:** Readable queries with compile-time field checks.
- **Con:** Huge nested includes can become accidental cartesian products — inspect SQL.

## Comparison
- vs raw SQL: Prisma wins CRUD speed; raw wins bespoke reports.
- vs [[Prisma]]: client generation enables these typed calls.


### Use cases
- Admin list pages with filters + related counts

- **Example:** Loop `findUnique` per id from a list
