<!-- note-strategy: operational -->
[[javascript]] [[hoisting]] [[mixin]]

# prototype

> Objects inherit via a prototype chain — property lookup walks `__proto__` until found or `null`.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** `obj.foo` checks own props, then `Object.getPrototypeOf(obj)`, and so on. `class` syntax is sugar over constructor + `.prototype`.

```txt
instance → C.prototype → Object.prototype → null
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **own vs inherited** | On object vs chain | “`hasOwnProperty` / `Object.hasOwn`.” |
| **prototype** | Shared methods object | “One function, many instances.” |
| **[[Prototype]]** | Internal link | “Not the same as `.prototype` on functions.” |

## Standard config / commands

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

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| method undefined | Forgot `prototype` / `new` | Use `new` or class |
| Unexpected shared state | Mutable value on prototype | Put state on `this` |
| Broken instanceof | Wrong prototype | Fix inheritance link |
| Perf weirdness | Mutating [[Prototype]] | Create with right proto once |

---

## Gotchas

> [!WARNING]
> **`obj.__proto__`** — legacy accessor; prefer `Object.getPrototypeOf`.

> [!WARNING]
> **Arrays/objects as prototype props** — shared across instances.

---

## When NOT to use

- **Deep classic OOP trees** — prefer composition.
- **Changing proto at runtime** — engines deoptimize.

---

## Related

[[hoisting]] [[mixin]] [[Classes]]
