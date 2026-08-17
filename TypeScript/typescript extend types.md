[[typescript types]] [[typescript]] [[ambient modules]] [[Triple-Slash Directives]] [[class-transformer]]

# typescript extend types

> Grow existing shapes with `extends`, intersections (`&`), interface merging, and module augmentation — types compose; they do not replace runtime inheritance.

```txt
        typescript extend  ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers ask how you extend types to see if you know interfaces merge but…

## Sources
- [TypeScript Handbook — Object Types (extending)](https://www.typescriptlang.org/docs/handbook/2/objects.html) — overview
- [TypeScript Handbook — Declaration Merging](https://www.typescriptlang.org/docs/handbook/declaration-merging.html) — deep-dive
- [TypeScript Handbook — Modules — augmentation](https://www.typescriptlang.org/docs/handbook/declaration-files/templates/module-augmentation-d-ts.html) — deep-dive

## Key Concepts
- **`interface extends`:** inheritance-like composition with clear hierarchies.
- **Intersection `&`:** combine type aliases; conflicting properties can become `never`.
- **Declaration merging:** identical interface names stack members.
- **Module augmentation:** patch Express `Request`, etc., inside a module file (`export {}`).
- **Generic constraints:** `T extends SomeShape` bounds type parameters.


- **Core:** Extending types means building larger contracts from smaller ones: interface …

## Technical Details
```txt
interface A { x: number }
interface A { y: string }  // merges → {x,y}

type C = A & { z: boolean }
```

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

| Mechanism | Effect |
|-----------|--------|
| `interface extends` | Inheritance-like |
| Intersection `&` | Combine aliases |
| Declaration merge | Same name stacks |
| Module augmentation | Patch lib types |

| Knob | Why it matters |
|------|----------------|
| Merge conflicts | Incompatible fields error |
| `extends` constraint | Generic bounds |
| Augmentation scope | File must be a module |

| Symptom | Check | Fix |
|---------|-------|-----|
| Subsequent property declarations… | Merge clash | Rename or compatible types |
| Augmentation ignored | Script vs module | Add `export {}` |
| Excess fields lost | Widened too early | Keep generics with `extends` |
| Circular extends | A↔B | Break with indirection |

## Mistakes to Avoid
- **Mistake:** Expecting `type` aliases to declaration-merge
- **Mistake:** Open-ended monkey-patching of every library type
- **Mistake:** Intersecting incompatible property types and wondering why you g…
- **Mistake:** Replacing runtime class design with type-only hierarchies and as…

## Pros/Cons or Trade-offs
- **Pro:** Compose and patch types without forking libraries.
- **Con:** Augmentations break when upstream library types change.
- **Con:** Deep `extends` chains become hard to reason about — prefer small compositions.

## Comparison
- vs [[typescript types]]: core unions/generics live there; extension/merging patterns live here.
- vs [[ambient modules]]: ambient introduces types for untyped modules
- vs runtime class inheritance: type `extends` does not create prototype chains at runtime.


### Use cases
- Express apps augment `Request` with `userId` after authentication middleware

- **Example:** Module augmentation silently ignored because the file was a scri…
