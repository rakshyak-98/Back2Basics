[[javascript]] [[hoisting]] [[mixin]] [[Classes]]

# prototype

> Objects inherit via a prototype chain — property lookup walks `__proto__` until found or `null`.

```txt
        prototype ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers use **prototype** to check whether you can explain the mechanism…

## Sources
- [MDN — Inheritance and the prototype chain](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Inheritance_and_the_prototype_chain) — deep-dive
- [Wikipedia — prototype](https://en.wikipedia.org/wiki/prototype) — overview

## Key Concepts
- **own vs inherited:** On object vs chain — `hasOwnProperty` / `Object.hasOwn`.
- **prototype:** Shared methods object — One function, many instances.
- **[[Prototype]]:** Internal link — Not the same as `.prototype` on functions.

## Technical Details
```txt
instance → C.prototype → Object.prototype → null
```

```js
function Dog(name) { this.name = name }
Dog.prototype.bark = function () { return 'woof' }
const d = new Dog('Rex')

class Cat {
  meow() { return 'mew' }
}
Object.getPrototypeOf(d) === Dog.prototype
```

| Knob | Why it matters |
|------|----------------|
| `Object.create(proto)` | Pure delegation |
| `Object.setPrototypeOf` | Slow/mutable — avoid hot paths |
| `static` | On constructor, not instances |

## Mistakes to Avoid
- **Mistake:** **`obj.__proto__`**
- **Mistake:** **Arrays/objects as prototype props** — shared across instances
- **Mistake:** **method undefined:** check Forgot `prototype` / `new`
- **Mistake:** **Unexpected shared state:** check Mutable value on prototype
- **Mistake:** **Broken instanceof:** check Wrong prototype
- **Mistake:** **Perf weirdness:** check Mutating [[Prototype]]

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Objects inherit via a prototype chain — property lookup walks `__proto__` until …).
- **Con / when not:** **Deep classic OOP trees** — prefer composition.
- **Con / when not:** **Changing proto at runtime** — engines deoptimize.

## Comparison
- vs [[hoisting]]: know when each applies


### Use cases
- In production APIs and tooling, **prototype** shows up whenever teams ship No…
