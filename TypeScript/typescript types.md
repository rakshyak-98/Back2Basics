<!-- note-strategy: operational -->
[[TypeScript]] [[typescript]] [[tsconfig]]

# typescript types

> Types — unions, generics, utility types, and narrowing; describe values without existing at runtime.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Prefer unions + narrowing over deep inheritance. Generics parameterize shapes. Utility types (`Partial`, `Pick`, `Omit`, `Record`) transform existing types.

```txt
value ──typeof/guard──► narrowed type
Generic<T> ──reuse──► concrete
```

| Tool | Job |
|------|-----|
| Union / `never` | Exhaustiveness |
| `interface` vs `type` | Merging vs aliases |
| `satisfies` | Check without widen |
| Mapped / conditional | Advanced transforms |

---

## Standard config / commands

```ts
type Result<T> = { ok: true; value: T } | { ok: false; error: string }

function unwrap<T>(r: Result<T>): T {
  if (!r.ok) throw new Error(r.error)
  return r.value
}

type User = { id: string; email: string; role: 'admin' | 'user' }
type PublicUser = Omit<User, 'email'>
```

| Knob | Why it matters |
|------|----------------|
| `unknown` | Safe top type |
| `readonly` / `as const` | Literal inference |
| Discriminant field | Reliable switches |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Type too wide `string` | Lost literals | `as const` / `satisfies` |
| Property missing after Omit | Wrong key | Fix keys; use Pick |
| Generic infer `unknown` | Poor constraint | Add `extends` |
| Excess property errors | Fresh object literal | Variable first or widen |

---

## Gotchas

> [!WARNING]
> **Structural typing** — extra fields allowed via variables.

> [!WARNING]
> **`enum` vs union** — unions usually clearer for JSON APIs.

> [!WARNING]
> **Utility types are shallow** — deep partial needs custom.

---

## When NOT to use

- **Runtime schema** — Zod.
- **Complex conditional types for business rules** — keep readable.
- **`any` to ship** — quarantine in adapters.

---

## Related

[[typescript extend types]] [[typescript]] [[class-transformer]]
