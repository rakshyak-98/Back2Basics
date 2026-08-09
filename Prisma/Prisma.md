[[Prisma]]

# Prisma

> Prisma — the Prisma client is generated as a set of TypeScript or JavaScript files and is located in the node_modules directory.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Prisma — plain job, how I run it, how I know it’s broken.


[Prisma doc Manifesto](https://www.prisma.io/blog/prisma-orm-manifesto?ref=dailydev)
The Prisma client is generated as a set of TypeScript or JavaScript files and is located in the `node_modules` directory.
- Default location `./node_modules/@prisma/client` this folder contains the generated code that Prisma uses to interact with the database.
- You do not directly edit this files; they are managed by Prisma
```shell
npx prisma generate; # generat the prisma client
```
- Read the `schema.prisma` file.
- Regenerate the Prisma Client files.

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Prisma** | Core idea of this note | “I can explain Prisma without jargon.” |
| **mental model** | How it works in one line | “Explain it without jargon first.” |
| **failure mode** | How it breaks | “Say what you check first.” |

---

## Standard config / commands

```bash
# reproduce with minimal input
# compare working vs broken env
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Unexpected result | inputs / versions | Reproduce minimal case |
| Works on one machine | env drift | Diff config and versions |
| Silent failure | logs / metrics | Add checks and alerts |

---

## Gotchas

> [!WARNING]
> Prefer simple words you can say in an interview.

---

## When NOT to use

- Skip it when a simpler existing tool already fits.

---

## Related

[[Prisma]]
