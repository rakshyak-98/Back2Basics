[[Prisma query]] [[Database/Database]] [[Database/migration]]

# Prisma

> Next-generation Node ORM — model schema in `schema.prisma`, generate a type-safe client, and migrate the database from that source of truth.

```txt
        Prisma ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers ask schema → `prisma generate` → client usage, migrate vs push, …

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

- Client is regenerated from schema

## Mistakes to Avoid
- **Mistake:** Editing files inside `@prisma/client` by hand
- **Mistake:** Using `db push` as the only production migration strategy
- **Mistake:** Forgetting to regenerate in CI after schema changes

## Pros/Cons or Trade-offs
- **Pro:** Excellent DX and type safety for common CRUD.
- **Con:** Complex SQL/analytics may still need raw queries or another tool.

## Comparison
- vs [[Prisma query]]: this note is the system; query note covers `findMany` patterns.
- vs bare `pg`/`mysql2`: more boilerplate, more control.


### Use cases
- Node APIs get typed queries and relation includes without hand-maintaining SQ…

- **Example:** Add a field to schema → migrate → generate → TypeScript compile …
