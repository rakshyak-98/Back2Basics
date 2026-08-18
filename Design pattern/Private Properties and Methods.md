[[Design pattern]] [[Design pattern/OOPS]]

# Private Properties and Methods

> Private members hide internal state; privileged methods are public functions that close over private variables in JavaScript's closure model.

## Mental model

**Say it in one breath:** Without native `private` in older JavaScript, use closures so only exposed methods can read or write hidden fields.

```javascript
function Gadget() {
  this.name = "iPod";
  this.stretch = function () {
    return "iPad";
  };
}
var toy = new Gadget();
toy.stretch(); // public method
```

```javascript
function Gadget() {
  var name = "iPod";
  this.getName = function () {
    return name;
  };
}
var toy = new Gadget();
toy.name;      // undefined — private
toy.getName(); // "iPod"
```

### Privileged methods

Public methods that access private members through closure.

> [!WARNING]
> Returning a private object or array by reference lets callers mutate internal state — return copies or frozen snapshots instead.

## Standard config / commands

```javascript
// Modern JS — native private fields
class Account {
  #balance = 0;
  deposit(amount) { this.#balance += amount; }
}
```

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| External code mutates internal array | Return by reference | Return `[...arr]` or `Object.freeze` |
| `undefined` on "private" field | Field on `this` | Use closure or `#` private fields |
| Subclass cannot access parent private | Language rules | Use `protected` or explicit getters |

## Gotchas

> [!WARNING]
> **Closure per instance** — each object carries its own function copies; fine for small objects, costly at scale.

## When NOT to use

- **Over-hiding in simple data objects** — plain properties plus conventions may suffice.

## Related

[[Design pattern/OOPS]] [[Design pattern/Singleton]] [[Design pattern/Static Members]]
