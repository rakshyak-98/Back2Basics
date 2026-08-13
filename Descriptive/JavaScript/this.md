[[Javascript]] [[JavaScript/Call stack]] [[JavaScript/execution context]]

# this

> `this` is the call-site receiver in JS — how you invoke the function decides what `this` is (unless bound/arrow).

---

## How it works

```txt
obj.fn()     → this = obj
fn()         → undefined (strict) / global
fn.call(x)   → this = x
new Fn()     → this = new object
() => this   → lexical outer this
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Call site** | How it’s invoked | “Not where it’s defined.” |
| **bind** | Freeze this | “Callbacks keep object.” |
| **Arrow** | Lexical this | “No own this.” |
| **strict mode** | Bare call → undefined | “Avoid accidental global.” |

---


## Configuration and commands

```js
const obj = {
  n: 1,
  f() { return this.n },
  a: () => this, // window/undefined — not obj
}
obj.f() // 1
const g = obj.f; g() // undefined (strict)
obj.f.bind({ n: 2 })() // 2
```

| Knob | Why it matters |
|------|----------------|
| class fields arrows | Auto-bind methods |
| bind in React | Legacy class handlers |
| strict | Default in modules |

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| `this` undefined | detached method | bind / arrow wrapper |
| Wrong object | nested callback | arrow or bind |
| Arrow on prototype | expected dynamic this | use method syntax |
| DOM handler loses this | class method pass | bind or arrow field |

---


## Gotchas

> [!WARNING]
> **Arrows on prototypes** — share one lexical `this` (usually wrong).

> [!WARNING]
> **Thinking `this` = “instance” in plain functions** — only with `new` or method call.

---


## When not to use

- **Pure functions** — pass arguments; avoid `this`.
- **Most modern React** — function components + hooks.


## Related

[[JavaScript/Call stack]] [[JavaScript/execution context]] [[JavaScript/constructor function]]

## Sources

- [Wikipedia — this](https://en.wikipedia.org/wiki/this)
