[[typescript]] [[typescript extend types]] [[tsconfig]] [[class-transformer]] [[typescript error]]

# typescript types

> Unions, generics, utility types, and narrowing describe values at compile time — they disappear at runtime, so they guide the checker rather than enforce data on the wire.





## Interview Relevance
Interviewers drill TypeScript types to see if you can narrow unions, use generics without sliding to `any`, prefer `unknown`, and know structural typing and shallow utility types (`Partial`, `Omit`).

## Sources
- [TypeScript Handbook — Everyday Types](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html) — overview
- [TypeScript Handbook — Narrowing](https://www.typescriptlang.org/docs/handbook/2/narrowing.html) — deep-dive
- [TypeScript Handbook — Utility Types](https://www.typescriptlang.org/docs/handbook/utility-types.html) — deep-dive

## Core Definition
TypeScript’s type system lets you name shapes (`type` / `interface`), compose them (unions, intersections, generics, mapped/conditional types), and narrow them in control flow — all erased when JavaScript is emitted.

## Key Concepts
- **Union / `never`:** model alternatives; `never` helps exhaustiveness checks.
- **`interface` vs `type`:** interfaces merge; type aliases are flexible combinations.
- **Generics:** reuse logic across shapes with constraints (`extends`).
- **Narrowing:** `typeof`, equality, and custom guards refine unions in a branch.
- **`satisfies`:** check a value against a type without widening inference.
- **Utility types:** `Pick`, `Omit`, `Partial`, `Readonly` — usually shallow.

## Technical Details
```txt
value ──typeof/guard──► narrowed type
Generic<T> ──reuse──► concrete
```

```ts
type Result<T> = { ok: true; value: T } | { ok: false; error: string }

function unwrap<T>(r: Result<T>): T {
  if (!r.ok) throw new Error(r.error)
  return r.value
}

type User = { id: string; email: string; role: 'admin' | 'user' }
type PublicUser = Omit<User, 'email'>
```

| Tool | Job |
|------|-----|
| Union / `never` | Exhaustiveness |
| `interface` vs `type` | Merging vs aliases |
| `satisfies` | Check without widen |
| Mapped / conditional | Advanced transforms |

| Knob | Why it matters |
|------|----------------|
| `unknown` | Safe top type |
| `readonly` / `as const` | Literal inference |
| Discriminant field | Reliable switches |

| Symptom | Check | Fix |
|---------|-------|-----|
| Type too wide `string` | Lost literals | `as const` / `satisfies` |
| Property missing after `Omit` | Wrong key | Fix keys; use `Pick` |
| Generic infers `unknown` | Poor constraint | Add `extends` |
| Excess property errors | Fresh object literal | Assign via variable or widen intentionally |

## Real-World Applications
API result types as discriminated unions (`ok: true | false`); DTO views via `Omit`/`Pick`; generic repository helpers constrained with `extends`.

**Example:** A configuration object inferred as `string` for a status field — use `as const` or `satisfies` so `"admin" | "user"` stays narrow.

## Pros/Cons or Trade-offs
- **Pro:** Express rich contracts and catch mismatches before runtime.
- **Con:** Deep conditional types can become unreadable — favor clarity.
- **Con:** Utility types are shallow; “deep partial” needs a custom mapped type.

## Comparison
- vs [[typescript extend types]]: this note covers core type tools; that one covers `extends`, intersections, and augmentation.
- vs runtime schemas (Zod): types do not validate JSON; schemas do.
- vs `enum`: string unions are usually clearer for JSON APIs.

## Mistakes to Avoid
- Using `any` to escape the checker — quarantine adapters; prefer `unknown`.
- Expecting structural typing to reject extra fields on variables the way fresh literals do.
- Encoding business rules in impenetrable conditional types.
- Assuming `Partial<T>` deep-partials nested objects.
