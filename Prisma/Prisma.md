[[Prisma query]] [[Database/Database]] [[Database/migration]]

# Prisma

> Next-generation Node ORM — model schema in `schema.prisma`, generate a type-safe client, and migrate the database from that source of truth.





## Interview Relevance
Interviewers ask schema → `prisma generate` → client usage, migrate vs push, and where generated code lives (`@prisma/client`).

## Sources
- [Prisma — ORM manifesto](https://www.prisma.io/blog/prisma-orm-manifesto) — overview
- [Prisma docs — Client](https://www.prisma.io/docs/orm/prisma-client) — deep-dive

## Key Concepts
- **Schema first:** models/relations in `schema.prisma`.
- **Generated client:** TypeScript/JS under `node_modules/@prisma/client` — do not hand-edit.
- **`prisma generate`:** rebuild client after schema changes.
- **Migrate:** versioned SQL for environments; `db push` for prototypes.

## Technical Details
```bash
npx prisma generate
npx prisma migrate dev --name init
npx prisma studio
```

```prisma
model User {
  id    Int    @id @default(autoincrement())
  email String @unique
  posts Post[]
}
```

Client is regenerated from schema — treat schema + migrations as the reviewable contract.

## Real-World Applications
Node APIs get typed queries and relation includes without hand-maintaining SQL strings for CRUD.

**Example:** Add a field to schema → migrate → generate → TypeScript compile errors guide call-site updates.

## Pros/Cons or Trade-offs
- **Pro:** Excellent DX and type safety for common CRUD.
- **Con:** Complex SQL/analytics may still need raw queries or another tool.

## Comparison
- vs [[Prisma query]]: this note is the system; query note covers `findMany` patterns.
- vs bare `pg`/`mysql2`: more boilerplate, more control.

## Mistakes to Avoid
- Editing files inside `@prisma/client` by hand.
- Using `db push` as the only production migration strategy.
- Forgetting to regenerate in CI after schema changes.
