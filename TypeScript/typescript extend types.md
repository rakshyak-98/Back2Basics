<!-- note-strategy: operational -->
[[TypeScript]] [[typescript types]] [[typescript]]

# typescript extend types

> Extending types — `extends`, intersection (`&`), interface merging, and module augmentation to grow existing shapes.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Interfaces can `extends` and merge by name. Type aliases use `&` / mapped types. Augment third-party modules with `declare module` carefully.

```txt
interface A { x: number }
interface A { y: string }  // merges → {x,y}

type C = A & { z: boolean }
```

| Mechanism | Effect |
|-----------|--------|
| `interface extends` | Inheritance-like |
| Intersection `&` | Combine aliases |
| Declaration merge | Same name stacks |
| Module augmentation | Patch lib types |

---

## Standard config / commands

```ts
interface Animal { name: string }
interface Dog extends Animal { bark(): void }

type WithId<T> = T & { id: string }

declare module 'express-serve-static-core' {
  interface Request {
    userId?: string
  }
}
```

| Knob | Why it matters |
|------|----------------|
| Merge conflicts | Identical incompatible fields error |
| `extends` constraint | Generic bounds |
| Augmentation scope | Must be module (import/export) |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Subsequent property declarations… | Merge clash | Rename / compatible types |
| Augmentation ignored | Script vs module | Add `export {}` |
| Excess fields lost | Widened too early | `extends` + generics |
| Circular extends | A↔B | Break with indirection |

---

## Gotchas

> [!WARNING]
> **`type` aliases don’t merge** — only interfaces.

> [!WARNING]
> **Augmenting libs** — version upgrades can break your patches.

> [!WARNING]
> **Intersection of conflicting props** — can become `never`.

---

## When NOT to use

- **Open-ended monkey patches** — wrap instead.
- **Deep extends chains** — compose smaller types.
- **Replacing runtime class inheritance** — types ≠ runtime.

---

## Related

[[typescript types]] [[ambient modules]] [[Triple-Slash Directives]]
