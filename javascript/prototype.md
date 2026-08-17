[[javascript]] [[hoisting]] [[mixin]] [[Classes]]

# prototype

> Objects inherit via a prototype chain — property lookup walks `__proto__` until found or `null`.





## Interview Relevance
Interviewers use **prototype** to check whether you can explain the mechanism in plain words and apply it under failure. Expect follow-ups on **own vs inherited**, **prototype**, **[[Prototype]]**.

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

## Real-World Applications
In production APIs and tooling, **prototype** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **`obj.__proto__`** — legacy accessor; prefer `Object.getPrototypeOf`; **Arrays/objects as prototype props** — shared across instances.

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (Objects inherit via a prototype chain — property lookup walks `__proto__` until …).
- **Con / when not:** **Deep classic OOP trees** — prefer composition.
- **Con / when not:** **Changing proto at runtime** — engines deoptimize.

## Comparison
vs [[hoisting]]: know when each applies — do not treat them as interchangeable. vs [[mixin]]: know when each applies — do not treat them as interchangeable. vs [[Classes]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid
- **`obj.__proto__`** — legacy accessor; prefer `Object.getPrototypeOf`.
- **Arrays/objects as prototype props** — shared across instances.
- **method undefined:** check Forgot `prototype` / `new`; fix: Use `new` or class
- **Unexpected shared state:** check Mutable value on prototype; fix: Put state on `this`
- **Broken instanceof:** check Wrong prototype; fix: Fix inheritance link
- **Perf weirdness:** check Mutating [[Prototype]]; fix: Create with right proto once
